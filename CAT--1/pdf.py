import PyPDF2
import os

# Sample dataset
dataset = [
    {
        "Name": "142222104063",
        "dob": "2005-06-25"
    },
    {
        "Name": "142222104064",
        "dob": "2004-08-27"
    },
    {
        "Name": "142222104065",
        "dob": "2004-01-26"
    },
    {
        "Name": "142222104066",
        "dob": "2005-03-07"
    },
    {
        "Name": "142222104067",
        "dob": "2004-08-28"
    },
    {
        "Name": "142222104068",
        "dob": "2005-04-03"
    },
    {
        "Name": "142222104069",
        "dob": "2005-06-24"
    },
    {
        "Name": "142222104070",
        "dob": "2005-06-24"
    },
    {
        "Name": "142222104071",
        "dob": "2004-08-01"
    },
    {
        "Name": "142222104072",
        "dob": "2005-06-25"
    },
    {
        "Name": "142222104074",
        "dob": "2005-03-08"
    },
    {
        "Name": "142222104075",
        "dob": "2005-03-17"
    },
    {
        "Name": "142222104076",
        "dob": "2004-12-08"
    },
    {
        "Name": "142222104078",
        "dob": "2004-12-15"
    },
    {
        "Name": "142222104079",
        "dob": "2004-12-25"
    },
    {
        "Name": "142222104081",
        "dob": "2005-05-02"
    },
    {
        "Name": "142222104082",
        "dob": "2004-11-25"
    },
    {
        "Name": "142222104083",
        "dob": "2004-01-30"
    },
    {
        "Name": "142222104084",
        "dob": "2004-09-03"
    },
    {
        "Name": "142222104085",
        "dob": "2004-06-14"
    },
    {
        "Name": "142222104086",
        "dob": "2005-09-21"
    },
    {
        "Name": "142222104087",
        "dob": "2004-09-13"
    },
    {
        "Name": "142222104088",
        "dob": "2004-09-12"
    },
    {
        "Name": "142222104089",
        "dob": "2004-05-06"
    },
    {
        "Name": "142222104090",
        "dob": "2005-06-23"
    },
    {
        "Name": "142222104091",
        "dob": "2004-09-14"
    },
    {
        "Name": "142222104092",
        "dob": "2004-08-17"
    },
    {
        "Name": "142222104093",
        "dob": "2005-02-23"
    },
    {
        "Name": "142222104094",
        "dob": "2005-07-10"
    },
    {
        "Name": "142222104095",
        "dob": "2005-09-30"
    },
    {
        "Name": "142222104096",
        "dob": "2004-04-11"
    },
    {
        "Name": "142222104097",
        "dob": "2004-04-09"
    },
    {
        "Name": "142222104098",
        "dob": "2005-10-08"
    },
    {
        "Name": "142222104099",
        "dob": "2003-06-13"
    },
    {
        "Name": "142222104100",
        "dob": "2004-11-14"
    },
    {
        "Name": "142222104101",
        "dob": "2004-09-20"
    },
    {
        "Name": "142222104102",
        "dob": "2004-12-13"
    },
    {
        "Name": "142222104103",
        "dob": "2003-11-01"
    },
    {
        "Name": "142222104104",
        "dob": "2004-11-17"
    },
    {
        "Name": "142222104105",
        "dob": "2005-04-22"
    },
    {
        "Name": "142222104106",
        "dob": "2004-06-25"
    },
    {
        "Name": "142222104107",
        "dob": "2004-10-15"
    },
    {
        "Name": "142222104108",
        "dob": "2004-11-09"
    },
    {
        "Name": "142222104109",
        "dob": "2004-10-18"
    },
    {
        "Name": "142222104110",
        "dob": "2005-06-12"
    },
    {
        "Name": "142222104111",
        "dob": "2004-07-11"
    },
    {
        "Name": "142222104112",
        "dob": "2005-05-20"
    },
    {
        "Name": "142222104113",
        "dob": "2004-09-17"
    },
    {
        "Name": "142222104114",
        "dob": "2004-09-26"
    },
    {
        "Name": "142222104115",
        "dob": "2004-11-22"
    },
    {
        "Name": "142222104116",
        "dob": "2004-11-27"
    },
    {
        "Name": "142222104117",
        "dob": "2003-08-31"
    },
    {
        "Name": "142222104118",
        "dob": "2004-01-27"
    },
    {
        "Name": "142222104119",
        "dob": "2004-10-08"
    },
    {
        "Name": "142222104120",
        "dob": "2005-03-04"
    },
    {
        "Name": "142222104305",
        "dob": "2004-12-16"
    },
    {
        "Name": "142222104306",
        "dob": "2005-08-29"
    },
    {
        "Name": "142222104307",
        "dob": "2001-05-13"
    },
    {
        "Name": "93425",
        "dob": "2018-04-12"
    }
]

# Function to convert "YYYY-MM-DD" to "DDMMYYYY"
def convert_dob(dob):
    dob_parts = dob.split("-")
    return f"{dob_parts[2]}{dob_parts[1]}{dob_parts[0]}"

# Folder containing the PDF files
pdf_folder = "C:\\Users\\17_karthick_03\\Downloads\\SEM--5 Automation\\CAT 1"  # Replace with your folder path

# Iterate through each dataset entry and process the PDF
for entry in dataset:
    name = entry["Name"]
    dob = entry["dob"]
    password = convert_dob(dob)

    # Find the matching PDF file
    pdf_file = f"{name}_CAT1_Report.pdf"
    pdf_path = os.path.join(pdf_folder, pdf_file)

    if os.path.exists(pdf_path):
        # Open the original PDF
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()

            # Add all pages to the writer
            for page_num in range(len(reader.pages)):
                writer.add_page(reader.pages[page_num])

            # Set the password for the new PDF
            writer.encrypt(user_pwd=password, owner_pwd=None, use_128bit=True)

            # Save the new encrypted PDF
            encrypted_pdf_path = os.path.join(pdf_folder, f"{pdf_file}")
            with open(encrypted_pdf_path, "wb") as new_file:
                writer.write(new_file)

        print(f"Password set for {pdf_file}")
    else:
        print(f"File {pdf_file} not found!")
