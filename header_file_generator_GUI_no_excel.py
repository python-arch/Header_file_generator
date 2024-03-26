from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QComboBox,QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import os
import openpyxl
import datetime
import subprocess
import shutil
import time
class HeaderGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tornado Flasher")
        self.layout = QVBoxLayout()

        self.init_ui()

    def init_ui(self):
        # UI for getting the data from user input
        self.brand_label = QLabel("Brand")
        self.brand_entry = QComboBox()
        self.brand_entry.addItem("TND")
        self.brand_entry.addItem("HT")

        self.product_label = QLabel("Product")
        self.product_entry = QComboBox()
        self.product_entry.addItem("Item1")
        self.product_entry.addItem("Item2")

        self.model_label = QLabel("Model")
        self.model_entry = QComboBox()
        self.model_entry.addItem("Item1")
        self.model_entry.addItem("Item2")
        

        self.image_label = QLabel()
        self.load_image()

        # handling the flashing of code
        self.compile_button = QPushButton("Compile and Upload", self)
        self.compile_button.clicked.connect(self.flash_device)

        self.next_button = QPushButton("Skip this device", self)
        self.next_button.clicked.connect(self.next_button_clicked)
        self.next_button.setEnabled(False)
        self.next_button.setHidden(True)
        
        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_entry)
        self.layout.addWidget(self.product_label)
        self.layout.addWidget(self.product_entry)
        self.layout.addWidget(self.model_label)
        self.layout.addWidget(self.model_entry)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.compile_button)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)

    def flash_device(self):
            id = self.process_single_device()
            QMessageBox.information(None, "Success", f"Device with id {id} was burnt successfully")
            
    def load_image(self):
        image_path = os.path.join(os.path.dirname(__file__), './header.png')
        original_pixmap = QPixmap(image_path)
        resized_pixmap = original_pixmap.scaledToWidth(200)  # Adjust the width as needed
        self.image_label.setPixmap(resized_pixmap)
        
    def process_single_device(self):
        brand = self.brand_entry.currentText()
        model  = self.model_entry.currentText()
        product = self.product_entry.currentText()
        
        # initialize IOT hub stuff
        iotHubName = "rd-iothub.azure-devices.net"
        resourceGroup = "AZ-EUW-RG-RDIOTHub-P"
        country = "EG"
        state = "C"
        organization = "Elaraby Group"

        # Get the current date and time
        currentDateTime = subprocess.check_output(['date', '+%Y-%m-%d_%H-%M-%S']).decode().strip()

        # Create a directory with the current date and time
        directoryName = "patch-" + currentDateTime
        os.makedirs(directoryName, exist_ok=True)
        os.chdir(directoryName)

        # Step 0: Azure Login
        subprocess.run(['az', 'login'])

        # Save the original directory
        originalDirectory = os.getcwd()
        # get mac address (1)
        print("Please connect ESP32 to the USB port...")
        while True:
            try:
                feedback = subprocess.check_output(['ls', '/dev/ttyUSB0']).decode().strip()
                if feedback:
                    print("Detected an ESP32 device")
                    mac = subprocess.check_output(['sudo', 'esptool', '--chip', 'esp32', '--port', '/dev/ttyUSB0', 'read_mac']).decode().strip()
                    print("Mac %s has been recorded." % mac)
                    print("You have 5 seconds to remove ESP32")
                    time.sleep(5)
            except subprocess.CalledProcessError:
                print('Device is not ready...')
            except KeyboardInterrupt:
                break
        deviceName = f"{brand}_{product}_{mac}"

        # Create folder for each device
        os.makedirs(deviceName, exist_ok=True)
        os.chdir(deviceName)

        # Generate X.509 Certificate and Private Key with 100 years validity for each device
        certPath = deviceName + "-cert.pem"
        keyPath = deviceName + "-key.pem"

        # Step 1: Generate X.509 Certificate and Private Key with 1000 years validity
        subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-keyout', keyPath, '-out', certPath,
                            '-days', '365242', '-nodes', '-subj', f'/C={country}/ST={state}/O={organization}/CN={device_id}'])

        # Step 2: Link Device ID with IoT Hub using X.509 authentication
        thumbprint = subprocess.check_output(['openssl', 'x509', '-in', certPath, '-noout', '-fingerprint']).decode().split('=')[-1].replace(':', '').strip()
        subprocess.run(['az', 'iot', 'hub', 'device-identity', 'create', '--hub-name', iotHubName, '--device-id', deviceName,
                            '--auth-method', 'x509_thumbprint', '--primary-thumbprint', thumbprint, '--secondary-thumbprint', thumbprint])

        # Step 3: Print device-specific configuration
        print("Device Name:", deviceName)
        print("Device Certificate Path:", certPath)
        print("Device Private Key Path:", keyPath)
        print("---------------------------------------")

        # Return to the original directory
        os.chdir(originalDirectory)
        certificates_directory = "./"
        for root, dirs, files in os.walk(certificates_directory):
            for file in files:
                if file.endswith("-cert.pem"):  # Check if it's a certificate file
                    device_id = file.replace("-cert.pem", "")
                    cert_path = os.path.join(root, file)
                    key_path = os.path.join(root, device_id + "-key.pem")

                    # Read certificate and private key content
                    with open(cert_path, 'r') as cert_file:
                        cert_content = cert_file.read()

                    with open(key_path, 'r') as key_file:
                        key_content = key_file.read()
        self.generate_and_send_header(device_id,cert_content,key_content)
        return device_id
                    
    def generate_and_send_header(self , device_id, x509_cert, private_key):
        brand = self.brand_entry.currentText()
        product = self.product_entry.currentText()
        model = self.model_entry.currentText()

        if not brand or not product or not model:
            QMessageBox.critical(None, "Error", "All fields are required.")
            return

        self.generate_header(brand, product, model , device_id , x509_cert , private_key)

        QMessageBox.information(None, "Success", "IOT_configs header file saved successfully")

    def generate_header(self, brand, product, model , device_id ,x509_cert , private_key):
        header_content = f"""
        /******************************************************************************************************************************
 File Name      : IOT_Azure_X509_Cert_User.h
 Description    : This file as Header for iot Azure X509 configuration
 Author         : Omar Sameh
 Tester         : Sherif Elgayar
 Device(s)      : ESP32S2
 Creation Date  : 1/1/2024
 Testing Date   : 
 @COPYRIGHT 2016 El-ARABY Research and development center.
 all rights reserved
*********************************************************************************************************************************/
#ifndef TORNADO_IOT_AZURE_X509_CERT_USER_H
#define TORNADO_IOT_AZURE_X509_CERT_USER_H

#define BRAND_NAME      "{brand}_"    // ElarabyGroup Brand Name
#define PRODUCT_NAME    "{product}_"     // ElarabyGroup Product Name

#define ElarabyGroup_Factory_WiFi_SSID         "omarsamehsyam"
#define ElarabyGroup_Factory_WiFi_Password     "omar1996"

#define IOT_CONFIG_IOTHUB_FQDN "{product}-{datetime.datetime.now().year}-iothub.azure-devices.net"

// ElarabyGroup Product IoT Device X.509 Cetificate
static const char* IOT_DEVICE_X509_CERTIFCATE = R"({x509_cert})";

// ElarabyGroup Product IoT Device Private Key
static const char* IOT_DEVICE_X509_PRIVATE_KEY = R"({private_key})";
//******************************************************************************************************************************
#endif"""  # Add your header content here
        brand_folder = os.path.join(os.path.dirname(__file__), brand)
        if not os.path.exists(brand_folder):
            os.makedirs(brand_folder)

        device_folder = os.path.join(brand_folder, device_id)
        if not os.path.exists(device_folder):
            os.makedirs(device_folder)
        header_file_path = os.path.join(device_folder, "Tornado_IOT_Azure_X509_Cert_User.h")
        with open(header_file_path, "w") as header_file:
            header_file.write(header_content)
        # Copy file from a certain path to the device folder
        source_file_path = "/Users/python/Projects/Header File Generator/sketch_mar17a/sketch_mar17a.ino"
        destination_file_path = os.path.join(device_folder, f"{device_id}.ino")
        shutil.copyfile(source_file_path, destination_file_path)
        self.compile_and_upload(device_folder, device_id , brand)

    def next_button_clicked(self, device_folder_name):
        self.next_button.setEnabled(False)
        self.next_button.setHidden(True)
    def compile_and_upload(self , device_folder ,device_folder_name , brand):
                if os.path.isdir(device_folder):
                    ino_file_path = os.path.join(device_folder, device_folder_name + ".ino")
                    if os.path.exists(ino_file_path):
                        # Compile and upload the .ino file using Arduino CLI
                        project_path = f"{brand}/{device_folder_name}"
                        # Name of the Arduino code file
                        code_file = f"{device_folder_name}.ino"
                        result= subprocess.run(["arduino-cli", "compile", "--fqbn", "esp32:esp32:esp32", os.path.join(project_path, code_file)])
                        if result.returncode == 0:
                            QMessageBox.information(self, "Success", f"Device {device_folder_name} was successfully flashed")
                        else:
                            error_message = result.stderr.decode("utf-8")
                            QMessageBox.critical(self, "Error", f"Failed to flash device {device_folder_name}\nError: {error_message}\nClick 'Next' to proceed")
                            self.next_button.setEnabled(True)
                            self.next_button.setHidden(False)
                            self.next_button.clicked.connect(lambda: self.next_button_clicked(device_folder_name))


if __name__ == '__main__':
    app = QApplication([])
    window = HeaderGeneratorApp()
    window.show()
    app.exec_()
