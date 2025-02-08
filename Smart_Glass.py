import numpy as np
import cv2
import pyttsx3

# === Load Model Weights and Architecture === #
weights = np.load("RP2040_weights.npy", allow_pickle=True)
architecture = np.load("RP2040_architecture.npy", allow_pickle=True)

# Rebuild the model manually
def build_model(weights, architecture):
    layers = []
    for i, layer_info in enumerate(architecture):
        layer_name, input_shape, output_shape, config = layer_info
        layer_weights = weights[i]

        if layer_name == "conv2d":  # Convolutional layer
            layers.append({
                "type": "conv",
                "weights": layer_weights,
                "config": config
            })
        elif layer_name == "dense":  # Dense (Fully Connected) layer
            layers.append({
                "type": "dense",
                "weights": layer_weights,
                "config": config
            })
    return layers

model_layers = build_model(weights, architecture)

# Function for running inference
def run_inference(model_layers, input_data):
    x = input_data
    for layer in model_layers:
        if layer["type"] == "conv":
            # Apply convolution (simplified with NumPy)
            x = np.dot(x, layer["weights"][0]) + layer["weights"][1]
            x = np.maximum(0, x)  # ReLU activation
        elif layer["type"] == "dense":
            # Apply dense layer
            x = np.dot(x, layer["weights"][0]) + layer["weights"][1]
            x = np.maximum(0, x)  # ReLU activation
    return x

# === Initialize Text-to-Speech === #
engine = pyttsx3.init()

# === Initialize Hand Detection === #
# Option 1: Haar Cascade (for detecting hand-like shapes)
hand_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "aGest.xml")  # Replace with your hand cascade file

# Option 2: Use Mediapipe for hand detection (if needed)
# import mediapipe as mp
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands()

# === Real-Time Detection === #
cap = cv2.VideoCapture(0)

# Define class labels (update this based on your dataset)
class_labels = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H",
    8: "I",
    9: "J",
    10: "K",
    11: "L",
    12: "M",
    13: "N",
    14: "O",
    15: "P",
    16: "Q",
    17: "R",
    18: "S",
    19: "T",
    20: "U",
    21: "V",
    22: "W",
    23: "X",
    24: "Y",
    25: "Z"
    # Add your class mappings here
}

print("Press 'q' to exit the program.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale for hand detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect hands
    hands_detected = hand_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    for (x, y, w, h) in hands_detected:
        # Draw rectangle around the detected hand
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Capture the region of interest (ROI)
        hand_roi = frame[y:y + h, x:x + w]

        # Preprocess the image (resize and normalize)
        input_image = cv2.resize(hand_roi, (224, 224))  # Resize to model input size
        input_image = input_image.astype("float32") / 255.0  # Normalize to [0, 1]
        input_image = np.expand_dims(input_image, axis=0)  # Add batch dimension

        # Run inference
        predictions = run_inference(model_layers, input_image)
        predicted_class = np.argmax(predictions)

        # Check if the predicted class is valid
        if predicted_class in class_labels:
            gesture = class_labels[predicted_class]
            print(f"Detected Gesture: {gesture}")

            # Speak the gesture aloud
            engine.say(gesture)
            engine.runAndWait()

    # Show the camera feed with detection boxes
    cv2.imshow("Smart Glass - Hand Gesture Detection", frame)

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
