import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import openpyxl

def generate_firebase_header(api_key, project_id):
    header_content = f"""
    // Firebase Header File

    // Define Firebase Realtime Database URL
    #define FIREBASE_URL "https://{project_id}.firebaseio.com"

    // Define Web API Key
    #define API_KEY "{api_key}"
    """

    with open("firebase_config.h", "w") as header_file:
        header_file.write(header_content)

def send_email(api_key, project_id, recipient_email):
    subject = "Firebase Header File"
    sender_email = "amra51548@gmail.com"  # Replace with your email
    sender_password = "ktjz syad vzfk wwdi"  # Replace with your email password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the firebase_config.h file
    file_path = os.path.join(os.path.dirname(__file__), 'firebase_config.h')
    attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
    attachment.add_header('Content-Disposition', 'attachment', filename='firebase_config.h')
    msg.attach(attachment)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

def generate_header_from_excel(file_path, recipient_email):
    # Load the Excel file
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # Get the API key and project ID from the Excel file
    api_key = sheet['A1'].value
    project_id = sheet['B1'].value

    if not api_key or not project_id or not recipient_email:
        print("API key, project ID, and recipient email are required.")
        return

    generate_firebase_header(api_key, project_id)
    send_email(api_key, project_id, recipient_email)
    print("Firebase header file sent via email successfully.")

# Example usage
file_path = 'path/to/your/excel/file.xlsx'
recipient_email = input("Enter recipient's email address: ")
generate_header_from_excel(file_path, recipient_email)
