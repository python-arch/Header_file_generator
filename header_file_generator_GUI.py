from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def generate_firebase_header(cert , private_key , firmware_endpoint , folder , FQDN, Device_key, Green_PIN, Red_PIN, Blue_PIN):
    header_content = f"""
   /******************************************************************************************************************************
 File Name      : iot_configs.h
 Description    : This file as Header for iot configuration
 Author         : Omar Sameh
 Tester         :
 Device(s)      : ESP32S2
 Creation Date  : 1/1/2024
 Testing Date   :
 @COPYRIGHT 2016 El-ARABY Research and development center.
 all rights reserved
*********************************************************************************************************************************/
#ifndef IOT_CONFIGS_H
#define IOT_CONFIGS_H

//FOTA PRODUCT URL
#define FOTA_SERVER_URL "https://tornadofotaserver.000webhostapp.com/"
#define FOTA_SERVER_FIRMWARE_ENDPOINT "/upload.php?device={firmware_endpoint}"
#define FOTA_DEVICE_FOLDER "/uploads/{folder}/"

// Enable macro IOT_CONFIG_USE_X509_CERT to use an x509 certificate to authenticate the IoT device.
// The two main modes of authentication are through SAS tokens (automatically generated by the
// sample using the provided device symmetric key) or through x509 certificates. Please choose the
// appropriate option according to your device authentication mode.

//#define IOT_CONFIG_USE_X509_CERT

#ifdef IOT_CONFIG_USE_X509_CERT

/*
 * Please set the define IOT_CONFIG_DEVICE_CERT below with
 * the content of your device x509 certificate.
 *
 * Example:
 * #define IOT_CONFIG_DEVICE_CERT "-----BEGIN CERTIFICATE-----\r\n" \
 * "MIIBJDCBywIUfeHrebBVa2eZAbouBgACp9R3BncwCgYIKoZIzj0EAwIwETEPMA0G\r\n" \
 * "A1UEAwwGRFBTIENBMB4XDTIyMDMyMjazMTAzN1oXDTIzMDMyMjIzMTAzN1owGTEX\r\n" \
 * "MBUGA1UEAwwOY29udG9zby1kZXZpY2UwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNC\r\n" \
 * .......
 * "YmGzdaHTb6P1W+p+jmc+jJn1MAoGCXqGSM49BAMCA0gAMEUCIEnbEMsAdGFroMwl\r\n" \
 * "vTfQahwsxN3xink9z1gtirrjQlqDAiEAyU+6TUJcG6d9JF+uJqsLFpsbbF3IzGAw\r\n" \
 * "yC+koNRC0MU=\r\n" \
 * "-----END CERTIFICATE-----"
 *
 */
#define IOT_CONFIG_DEVICE_CERT "{cert}"


/*
 * Please set the define IOT_CONFIG_DEVICE_CERT_PRIVATE_KEY below with
 * the content of your device x509 private key.
 *
 * Example:
 *
 * #define IOT_CONFIG_DEVICE_CERT_PRIVATE_KEY "-----BEGIN EC PRIVATE KEY-----\r\n" \
 * "MHcCAQEEIKGXkMMiO9D7jYpUjUGTBn7gGzeKPeNzCP83wbfQfLd9obAoGCCqGSM49\r\n" \
 * "AwEHoUQDQgAEU6nQoYbjgJvBwaeD6MyAYmOSDg0QhEdyyV337qrlIbDEKvFsn1El\r\n" \
 * "yRabc4dNp2Jhs3Xh02+j9Vvqfo5nPoyZ9Q==\r\n" \
 * "-----END EC PRIVATE KEY-----"
 *
 * Note the type of key may different in your case. Such as BEGIN PRIVATE KEY
 * or BEGIN RSA PRIVATE KEY.
 *
 */
#define IOT_CONFIG_DEVICE_CERT_PRIVATE_KEY "{private_key}"

#endif // IOT_CONFIG_USE_X509_CERT

// Azure IoT
#define IOT_CONFIG_IOTHUB_FQDN "{FQDN}"

// Use device key if not using certificates
#ifndef IOT_CONFIG_USE_X509_CERT
#define IOT_CONFIG_DEVICE_KEY "{Device_key}"
#endif // IOT_CONFIG_USE_X509_CERT

// Publish 1 message every 2 seconds
#define TELEMETRY_FREQUENCY_MILLISECS 2000

#define AZURE_SDK_CLIENT_USER_AGENT "c%2F" AZ_SDK_VERSION_STRING "(ard;esp32)"

// Utility macros and defines
#define sizeofarray(a) (sizeof(a) / sizeof(a[0])) // Macro to get the size of an array
#define NTP_SERVERS "pool.ntp.org", "time.nist.gov" // NTP server addresses
#define MQTT_QOS1 1                 // MQTT Quality of Service level
#define DO_NOT_RETAIN_MSG 0         // MQTT retain message flag
#define SAS_TOKEN_DURATION_IN_MINUTES 60 // Duration of SAS token validity in minutes
#define UNIX_TIME_NOV_13_2017 1510592825   // Reference UNIX timestamp

#define PST_TIME_ZONE -8                       // Pacific Standard Time (PST) time zone
#define PST_TIME_ZONE_DAYLIGHT_SAVINGS_DIFF 1  // Daylight Saving Time (DST) difference

#define GMT_OFFSET_SECS (PST_TIME_ZONE * 3600)                               // GMT offset without DST
#define GMT_OFFSET_SECS_DST ((PST_TIME_ZONE + PST_TIME_ZONE_DAYLIGHT_SAVINGS_DIFF) * 3600) // GMT offset with DST

// Define the EEPROM addresses for storing data
#define EEPROM_ADDR_WIFI_SSID 0
#define EEPROM_ADDR_WIFI_PASSWORD (EEPROM_ADDR_WIFI_SSID + sizeof(ssid))
#define EEPROM_ADDR_ADMIN_USERNAME (EEPROM_ADDR_WIFI_PASSWORD + sizeof(password))
#define EEPROM_ADDR_ADMIN_PASSWORD (EEPROM_ADDR_ADMIN_USERNAME + sizeof(adminUsername))
#define EEPROM_ADDR_ADMIN_MOBILE (EEPROM_ADDR_ADMIN_PASSWORD + sizeof(adminPassword))

#define GREEN_LED_PIN {Green_PIN}   // Replace with the actual GPIO pin number for the green LED
#define RED_LED_PIN {Red_PIN}     // Replace with the actual GPIO pin number for the red LED
#define BLUE_LED_PIN {Blue_PIN}    // Replace with the actual GPIO pin number for the blue LED

// Twilio configuration for (OTP Code)
#define TWILIO_ACCOUNT_SID "AC3bb09af01fe7e803765415104cb35809"
#define TWILIO_AUTH_TOKEN "3758854dfcf330775231ff1763a23119"
#define TWILIO_PHONE_NUMBER "+14328472138"

#define TWILIO_API_URL "api.twilio.com"
#define TWILIO_API_PORT 443

// Google Map apiKey 
#define apiKey "680393823aa050"
#define thisPage "/geolocation/v1/geolocate?key="
#define Host "www.googleapis.com"

#endif
    """

    with open("IOT_configs.h", "w") as header_file:
        header_file.write(header_content)

def send_email(recipient_email):
    subject = "IOT_Configs Header File"
    sender_email = "amra51548@gmail.com"  # Replace with your email
    sender_password = "ktjz syad vzfk wwdi" 

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the firebase_config.h file
    file_path = os.path.join(os.path.dirname(__file__), 'IOT_configs.h')
    attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
    attachment.add_header('Content-Disposition', 'attachment', filename='firebase_config.h')
    msg.attach(attachment)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

def generate_header():
     device_cert_value = device_cert_entry.text()
     device_cert_private_key_value = device_cert_private_key_entry.text()
     firmware_endpoint_value = firmware_endpoint_entry.text()
     folder_endpoint_value = folder_entry.text()
     fqdn_value = fqdn_entry.text()
     device_key_value= device_key_entry.text()
     green_pin_value= Green_pin_entry.text()
     red_pin_value= Red_pin_entry.text()
     blue_pin_value= blue_pin_entry.text()
     recipient_email = email_entry.text()
     
    
     if not device_cert_value or not device_cert_private_key_value or not firmware_endpoint_value or not folder_endpoint_value or not fqdn_value or not device_key_value or not green_pin_value or not blue_pin_value or not red_pin_value:
        QMessageBox.critical(None, "Error", "IOT config data and recipient email are required.")
        return

     generate_firebase_header(device_cert_value , device_cert_private_key_value , firmware_endpoint_value , folder= folder_endpoint_value , FQDN= fqdn_value, Device_key = device_key_value, Green_PIN= green_pin_value, Red_PIN = red_pin_value, Blue_PIN= blue_pin_value)
     send_email(recipient_email)

     QMessageBox.information(None, "Success", "IOT_configs header file sent via email successfully.")

app = QApplication([])

# Create and place widgets
device_cert_label = QLabel("Device Certificate")
device_cert_entry = QLineEdit()

device_cert_private_key = QLabel("Device Certificate Private Key")
device_cert_private_key_entry = QLineEdit()

firmware_endpoint = QLabel("Firmware Endpoint (Device)") # device endpoint only
firmware_endpoint_entry = QLineEdit()

folder = QLabel("Folder endpoint (Device)")
folder_entry = QLineEdit()

fqdn = QLabel("IOT_Hub FQDN")
fqdn_entry = QLineEdit()

device_key = QLabel("Device Key")
device_key_entry= QLineEdit()

green_pin = QLabel("GREEN LED Pin")
Green_pin_entry= QLineEdit()

red_pin = QLabel("RED LED Pin")
Red_pin_entry= QLineEdit()

blue_pin = QLabel("BLUE LED Pin")
blue_pin_entry= QLineEdit()

email_label = QLabel("Recipient Email:")
email_entry = QLineEdit()

# Load and display a resized image using QPixmap
image_path = os.path.join(os.path.dirname(__file__), './header.png')
original_pixmap = QPixmap(image_path)
resized_pixmap = original_pixmap.scaledToWidth(200)  # Adjust the width as needed
image_label = QLabel()
image_label.setPixmap(resized_pixmap)

generate_button = QPushButton("Generate and Send Header")
generate_button.clicked.connect(generate_header)

# Arrange widgets in the layout
layout = QVBoxLayout()
layout.addWidget(device_cert_label)
layout.addWidget(device_cert_entry)
layout.addWidget(device_cert_private_key)
layout.addWidget(device_cert_private_key_entry)
layout.addWidget(firmware_endpoint)
layout.addWidget(firmware_endpoint_entry)
layout.addWidget(folder)
layout.addWidget(folder_entry)
layout.addWidget(fqdn)
layout.addWidget(fqdn_entry)
layout.addWidget(device_key)
layout.addWidget(device_key_entry)
layout.addWidget(green_pin)
layout.addWidget(Green_pin_entry)
layout.addWidget(red_pin)
layout.addWidget(Red_pin_entry)
layout.addWidget(blue_pin)
layout.addWidget(blue_pin_entry)
layout.addWidget(email_label)
layout.addWidget(email_entry)
layout.addWidget(image_label)  # Add the QLabel for the resized image
layout.addWidget(generate_button)

# Create the main window
window = QWidget()
window.setWindowTitle("Firebase Header Generator")
window.setLayout(layout)

# Run the GUI
window.show()
app.exec_()