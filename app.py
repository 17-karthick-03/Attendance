# -*- coding: utf-8 -*-
from flask import Flask, render_template, make_response, url_for, request, session
import minimalmodbus
import threading
import time
import datetime
import re
from weasyprint import HTML, CSS
import google.generativeai as genai
from dotenv import load_dotenv
import os
import smtplib
import ssl
from email.mime.text import MIMEText

# Load the API key from the .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

app = Flask(__name__)
# A secret key is required for sessions. A long, random string is best.
app.secret_key = os.urandom(24)

# --- Configure Gemini API ---
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("Warning: GEMINI_API_KEY not found. AI features will be disabled.")
    model = None

# --- Modbus Setup ---
try:
    instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
    instrument.serial.baudrate = 4800
    instrument.serial.bytesize = 8
    instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout = 2
    instrument.mode = minimalmodbus.MODE_RTU
except Exception as e:
    print(f"Modbus connection error: {e}")
    instrument = None
    
# --- Cached sensor data and locks ---
sensor_cache = {}
cache_lock = threading.Lock()
monitoring_state = {"crop": None, "last_email_sent": None}
monitoring_lock = threading.Lock()

# --- Ideal NPK values for common hydroponic crops (simplified ranges) ---
# Values are in mg/kg
IDEAL_CROP_CONDITIONS = {
    "tomato": {"nitrogen": (90, 110), "phosphorus": (70, 90), "potassium": (100, 120)},
    "lettuce": {"nitrogen": (80, 100), "phosphorus": (50, 70), "potassium": (80, 100)},
    "pepper": {"nitrogen": (80, 100), "phosphorus": (60, 80), "potassium": (90, 110)},
    "cucumber": {"nitrogen": (100, 120), "phosphorus": (70, 90), "potassium": (110, 130)},
    "spinach": {"nitrogen": (90, 110), "phosphorus": (60, 80), "potassium": (80, 100)},
}

def read_sensor_data():
    """Read actual values from RS485 soil sensor."""
    if not instrument:
        return None
    try:
        moisture = instrument.read_register(0, 0) / 10.0
        temperature = instrument.read_register(1, 0) / 10.0
        ph = instrument.read_register(3, 0) / 10.0
        nitrogen = instrument.read_register(4, 0)
        phosphorus = instrument.read_register(5, 0)
        potassium = instrument.read_register(6, 0)

        return {
            "moisture": round(moisture, 1),
            "temperature": round(temperature, 1),
            "ph": round(ph, 1),
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "potassium": potassium,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        print(f"❌ Error reading sensor: {e}")
        return None

def send_notification_email(recipient, subject, body):
    """Sends a formatted email via SMTP."""
    if not all([EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT]):
        print("SMTP credentials are not configured. Cannot send email.")
        return False
    
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = recipient

        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def monitoring_thread(interval_s=30):
    """Background thread: updates sensor data and checks for monitoring alerts."""
    while True:
        data = read_sensor_data()
        
        if data:
            with cache_lock:
                sensor_cache.clear()
                sensor_cache.update(data)
                current_data = dict(sensor_cache)
        else:
            current_data = None
            print("Skipping monitoring check due to sensor read error.")
            
        if current_data:
            with monitoring_lock:
                crop_to_monitor = monitoring_state.get("crop")
            
            if crop_to_monitor and crop_to_monitor in IDEAL_CROP_CONDITIONS:
                ideal_levels = IDEAL_CROP_CONDITIONS[crop_to_monitor]
                alerts = []
                
                # Check nutrient levels
                for nutrient, ideal_range in ideal_levels.items():
                    current_level = current_data.get(nutrient)
                    if current_level is not None and not (ideal_range[0] <= current_level <= ideal_range[1]):
                        adjustment = "increase" if current_level < ideal_range[0] else "decrease"
                        alerts.append(f"Current {nutrient.capitalize()} level is {current_level} mg/kg. "
                                      f"It needs to be {adjustment} to the ideal range of {ideal_range[0]}-{ideal_range[1]} mg/kg.")
                
                if alerts:
                    with monitoring_lock:
                        last_sent = monitoring_state.get("last_email_sent")
                        # Send email only if a day has passed since the last one
                        if not last_sent or (datetime.datetime.now() - last_sent).total_seconds() > 86400:
                            subject = f"Hydroponics Alert: {crop_to_monitor.capitalize()} Nutrient Levels Off"
                            body = "Hello,\n\nThe following issues were detected in your nutrient solution:\n\n"
                            body += "\n".join(alerts)
                            body += "\n\n"
                            body += "To correct this, you can adjust your nutrient solution according to the guidance above and your product's instructions. A new email will be sent after 24 hours if the issue persists."
                            
                            if send_notification_email("17.karthick.03@gmail.com", subject, body):
                                monitoring_state["last_email_sent"] = datetime.datetime.now()
                                print(f"Sent email alert for {crop_to_monitor}.")
                            else:
                                print(f"Failed to send email alert for {crop_to_monitor}.")

        time.sleep(interval_s)

# Start the background monitoring thread
t_monitor = threading.Thread(target=monitoring_thread, args=(30,), daemon=True)
t_monitor.start()

# --- All existing Flask routes ---
pdf_css = """
@page { size: A4; margin: 18mm; }
body { font-family: 'Helvetica', Arial, sans-serif; color: #0f172a; }
.header { display:flex; justify-content:space-between; align-items:center; margin-bottom: 12mm; }
.title { font-size: 20px; font-weight:700; color:#0f172a; }
.sub { color:#475569; font-size:11px; }
.grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
.card { background: linear-gradient(180deg,#ffffff,#f7fafc); border-radius:8px; padding:10px; border:1px solid #e6edf3; display:flex; justify-content:space-between; align-items:center; }
.param { font-weight:600; color:#0f172a; font-size:13px; }
.value { background: linear-gradient(135deg,#e6fffa,#cffafe); padding:6px 10px; border-radius:6px; font-weight:700; color:#064e3b; font-size:13px; }
.footer { margin-top: 14mm; font-size:11px; color:#475569; }
"""

@app.route('/')
def index():
    with cache_lock:
        data = dict(sensor_cache) if sensor_cache else read_sensor_data()
    return render_template('index.html', data=data)

@app.route('/refresh')
def refresh():
    newdata = read_sensor_data()
    with cache_lock:
        if newdata:
            sensor_cache.clear()
            sensor_cache.update(newdata)
    return render_template('index.html', data=newdata)

@app.route('/download_pdf')
def download_pdf():
    with cache_lock:
        data = dict(sensor_cache) if sensor_cache else read_sensor_data()
    now = datetime.datetime.now()
    rendered = render_template('pdf_template.html', data=data, now=now)
    pdf = HTML(string=rendered, base_url=request.url_root).write_pdf(stylesheets=[CSS(string=pdf_css)])
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    filename = f"Soil_Sensor_Report_{timestamp_str}.pdf"
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@app.route('/analysis')
def analysis():
    recommendation = "AI feature is not available. Please check your API key."
    initial_data_summary = ""
    with cache_lock:
        data = dict(sensor_cache) if sensor_cache else read_sensor_data()
    initial_data_summary = (
        f"**My Soil Parameter Values:**\n"
        f"Moisture: {data['moisture'] if data else 'N/A'}%\n"
        f"Temperature: {data['temperature'] if data else 'N/A'}°C\n"
        f"pH Level: {data['ph'] if data else 'N/A'}\n"
        f"Nitrogen (N): {data['nitrogen'] if data else 'N/A'} mg/kg\n"
        f"Phosphorus (P): {data['phosphorus'] if data else 'N/A'} mg/kg\n"
        f"Potassium (K): {data['potassium'] if data else 'N/A'} mg/kg\n\n"
    )
    if model and data:
        prompt = (
            f"As a virtual crop expert for home terrace gardening in Chennai, Tamil Nadu, India, "
            f"provide a highly structured recommendation. "
            f"The response must follow a clear and direct format, without any additional explanations or advice."
            f"\n\nHere is the sensor data from your soil:\n"
            f"Moisture: {data['moisture']}%\n"
            f"Temperature: {data['temperature']}°C\n"
            f"pH Level: {data['ph']}\n"
            f"Nitrogen (N): {data['nitrogen']} mg/kg\n"
            f"Phosphorus (P): {data['phosphorus']} mg/kg\n"
            f"Potassium (K): {data['potassium']} mg/kg\n\n"
            f"Based on this data, please provide a list of 3-4 suitable crops for a home terrace garden. "
            f"For each recommended crop, list its ideal required parameter values, and state if it is suitable to plant now. "
            f"The output must follow this exact format:"
            f"\n\n"
            f"**Recommended Crops for Terrace Gardening:**\n"
            f"\n"
            f"1. [Crop Name]\n"
            f"   - Required Moisture: [Value]%\n"
            f"   - Required Temperature: [Value]°C\n"
            f"   - Required pH: [Value]\n"
            f"   - Required Nitrogen (N): [Value] mg/kg\n"
            f"   - Required Phosphorus (P): [Value] mg/kg\n"
            f"   - Required Potassium (K): [Value] mg/kg\n"
            f"   - This is suitable to plant now.\n"
            f"\n"
            f"2. [Next Crop Name]\n"
            f"   - Required Moisture: [Value]%\n"
            f"   - Required Temperature: [Value]°C\n"
            f"   - Required pH: [Value]\n"
            f"   - Required Nitrogen (N): [Value] mg/kg\n"
            f"   - Required Phosphorus (P): [Value] mg/kg\n"
            f"   - Required Potassium (K): [Value] mg/kg\n"
            f"   - This is suitable to plant now.\n"
        )
        try:
            response = model.generate_content(prompt)
            ai_recommendation = response.text.replace('*', '')
            recommendation = initial_data_summary + ai_recommendation
        except Exception as e:
            recommendation = initial_data_summary + f"An error occurred while generating the recommendation: {e}"
    return render_template('analysis.html', data=data, recommendation=recommendation)

@app.route('/download_analysis_pdf')
def download_analysis_pdf():
    recommendation = "AI feature is not available. Please check your API key."
    with cache_lock:
        data = dict(sensor_cache) if sensor_cache else read_sensor_data()
    if model and data:
        prompt = (
            f"As a virtual crop expert for home terrace gardening in Chennai, Tamil Nadu, India, "
            f"provide a highly structured recommendation. "
            f"The response must follow a clear and direct format, without any additional explanations or advice."
            f"\n\nHere is the sensor data from your soil:\n"
            f"Moisture: {data['moisture']}%\n"
            f"Temperature: {data['temperature']}°C\n"
            f"pH Level: {data['ph']}\n"
            f"Nitrogen (N): {data['nitrogen']} mg/kg\n"
            f"Phosphorus (P): {data['phosphorus']} mg/kg\n"
            f"Potassium (K): {data['potassium']} mg/kg\n\n"
            f"Based on this data, please provide a list of 5-6 suitable crops for a home terrace garden. "
            f"For each recommended crop, list its ideal required parameter values, and state if it is suitable to plant now. "
            f"The output must follow this exact format:"
            f"\n\n"
            f"**Recommended Crops for Terrace Gardening:**\n"
            f"\n"
            f"1. [Crop Name]\n"
            f"   - Required Moisture: [Value]%\n"
            f"   - Required Temperature: [Value]°C\n"
            f"   - Required pH: [Value]\n"
            f"   - Required Nitrogen (N): [Value] mg/kg\n"
            f"   - Required Phosphorus (P): [Value] mg/kg\n"
            f"   - Required Potassium (K): [Value] mg/kg\n"
            f"   - This is suitable to plant now.\n"
            f"\n"
            f"2. [Next Crop Name]\n"
            f"   - Required Moisture: [Value]%\n"
            f"   - Required Temperature: [Value]°C\n"
            f"   - Required pH: [Value]\n"
            f"   - Required Nitrogen (N): [Value] mg/kg\n"
            f"   - Required Phosphorus (P): [Value] mg/kg\n"
            f"   - Required Potassium (K): [Value] mg/kg\n"
            f"   - This is suitable to plant now.\n"
        )
        try:
            response = model.generate_content(prompt)
            recommendation = response.text
        except Exception as e:
            recommendation = f"An error occurred while generating the recommendation: {e}"
    recommendation = recommendation.replace('*', '')
    now = datetime.datetime.now()
    rendered_html = render_template('analysis_pdf_template.html', data=data, recommendation=recommendation, now=now)
    pdf = HTML(string=rendered_html, base_url=request.url_root).write_pdf(stylesheets=[CSS(string=pdf_css)])
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    filename = f"AI_Soil_Analysis_{timestamp_str}.pdf"
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@app.route('/user_specific_crop')
def user_specific_crop():
    with cache_lock:
        data = dict(sensor_cache) if sensor_cache else read_sensor_data()
    return render_template('user_specific_crop.html', data=data, analysis_result=None)

@app.route('/analyze_user_crop', methods=['POST'])
def analyze_user_crop():
    crop_name = request.form.get('crop_name')
    if not crop_name:
        with cache_lock:
            data = dict(sensor_cache) if sensor_cache else read_sensor_data()
        return render_template('user_specific_crop.html', data=data, analysis_result="Please enter a crop name.")
    analysis_result = "AI feature is not available. Please check your API key."
    if model:
        with cache_lock:
            data = dict(sensor_cache) if sensor_cache else read_sensor_data()
        if data:
            prompt = (
                f"You are a virtual soil expert for home gardening in Chennai, Tamil Nadu, India. "
                f"A user wants to know if '{crop_name}' is suitable for their soil. "
                f"Analyze the following sensor data and provide a concise, actionable analysis. "
                f"\n\n--- Sensor Data ---\n"
                f"Moisture: {data['moisture']}%\n"
                f"Temperature: {data['temperature']}°C\n"
                f"pH Level: {data['ph']}\n"
                f"Nitrogen (N): {data['nitrogen']} mg/kg\n"
                f"Phosphorus (P): {data['phosphorus']} mg/kg\n"
                f"Potassium (K): {data['potassium']} mg/kg\n"
                f"-------------------"
                f"\n\nBased on these conditions, is '{crop_name}' a good choice for this soil? "
                f"If the soil is suitable, state that it's a good choice. "
                f"If not, provide a bulleted list of specific, actionable steps the gardener should take to improve the soil for '{crop_name}'. "
                f"For example, 'Increase Nitrogen by adding compost' or 'Adjust pH with lime'."
            )
            try:
                response = model.generate_content(prompt)
                analysis_text = re.sub(r'^\s*[\*\-]\s*', '<li>', response.text.strip(), flags=re.MULTILINE)
                analysis_text = "<ul>" + analysis_text + "</li></ul>"
                analysis_text = analysis_text.replace('\n', '</li>')
                analysis_text = analysis_text.replace('</li>\n', '</li>')
                analysis_text = re.sub(r'^\s*([A-Za-z\s]+):', r'<h2>\1:</h2>', analysis_text, flags=re.MULTILINE)
                analysis_result = analysis_text
                session['user_analysis'] = analysis_result
            except Exception as e:
                analysis_result = f"An error occurred while generating the analysis: {e}"
        else:
            analysis_result = "Cannot perform analysis. Sensor data is not available."
    return render_template('user_specific_crop.html', data=data, analysis_result=analysis_result)

@app.route('/download_user_analysis_pdf')
def download_user_analysis_pdf():
    analysis_result = session.get('user_analysis')
    if not analysis_result:
        return "No analysis data found. Please run an analysis first.", 400
    with cache_lock:
        data = dict(sensor_cache) if sensor_cache else read_sensor_data()
    now = datetime.datetime.now()
    rendered_html = render_template('user_analysis_pdf_template.html', data=data, analysis_result=analysis_result, now=now)
    pdf = HTML(string=rendered_html, base_url=request.url_root).write_pdf(stylesheets=[CSS(string=pdf_css)])
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    filename = f"User_Crop_Analysis_{timestamp_str}.pdf"
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

# --- New Flask routes for Mode 3 ---

@app.route('/continuous_monitoring')
def continuous_monitoring():
    """Renders the monitoring page with a form to start monitoring."""
    with cache_lock:
        data = dict(sensor_cache) if sensor_cache else read_sensor_data()
    with monitoring_lock:
        status = monitoring_state.get("crop")
    return render_template('monitoring.html', data=data, status=status, ideal_conditions=IDEAL_CROP_CONDITIONS)


@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    """Starts or stops the continuous monitoring for a specific crop."""
    crop_name = request.form.get('crop_name').lower()
    action = request.form.get('action')
    
    with monitoring_lock:
        if action == 'start':
            if crop_name in IDEAL_CROP_CONDITIONS:
                monitoring_state["crop"] = crop_name
                monitoring_state["last_email_sent"] = None
                message = f"Monitoring started for {crop_name.capitalize()}."
            else:
                message = f"Error: '{crop_name.capitalize()}' is not in the list of supported crops."
        elif action == 'stop':
            monitoring_state["crop"] = None
            monitoring_state["last_email_sent"] = None
            message = "Monitoring stopped."
        else:
            message = "Invalid action."
            
    with cache_lock:
        data = dict(sensor_cache) if sensor_cache else read_sensor_data()
    with monitoring_lock:
        status = monitoring_state.get("crop")
        
    return render_template('monitoring.html', data=data, status=status, message=message, ideal_conditions=IDEAL_CROP_CONDITIONS)

if __name__ == '__main__':
    # Listen on network (0.0.0.0). Change host to '192.168.4.1' if you host on that IP.
    app.run(host='0.0.0.0', port=5000, debug=True)
