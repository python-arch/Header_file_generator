from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QComboBox,QFileDialog
from PyQt5.QtGui import QPixmap
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import openpyxl
class HeaderGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Header Generator")
        self.layout = QVBoxLayout()

        self.init_ui()

    def init_ui(self):
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

        self.load_excel_button = QPushButton("Load Excel File")
        self.load_excel_button.clicked.connect(self.load_excel_file)
        self.layout.addWidget(self.load_excel_button)

        self.layout.addWidget(self.brand_label)
        self.layout.addWidget(self.brand_entry)
        self.layout.addWidget(self.product_label)
        self.layout.addWidget(self.product_entry)
        self.layout.addWidget(self.model_label)
        self.layout.addWidget(self.model_entry)
        self.layout.addWidget(self.image_label)

        self.setLayout(self.layout)

    def load_image(self):
        image_path = os.path.join(os.path.dirname(__file__), './header.png')
        original_pixmap = QPixmap(image_path)
        resized_pixmap = original_pixmap.scaledToWidth(200)  # Adjust the width as needed
        self.image_label.setPixmap(resized_pixmap)
    def load_excel_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)")
        if file_path:
            self.process_excel_file(file_path)
    def process_excel_file(self, file_path):
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            device_id, x509_cert, private_key,device_name = row
            self.generate_and_send_header(device_id, x509_cert, private_key)
            
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

#define IOT_CONFIG_IOTHUB_FQDN "rd-iothub.azure-devices.net"

#ifdef IOT_CONFIG_USE_X509_CERT

#define IOT_DEVICE_X509_CERT "{x509_cert}"

#define IOT_DEVICE_PRIVATE_KEY "{private_key}"

#endif // IOT_CONFIG_USE_X509_CERT
//******************************************************************************************************************************
#endif"""  # Add your header content here
        brand_folder = os.path.join(os.path.dirname(__file__), brand)
        if not os.path.exists(brand_folder):
            os.makedirs(brand_folder)

        device_folder = os.path.join(brand_folder, device_id)
        if not os.path.exists(device_folder):
            os.makedirs(device_folder)
        header_file_path = os.path.join(device_folder, "IOT_configs.h")
        with open(header_file_path, "w") as header_file:
            header_file.write(header_content)

if __name__ == '__main__':
    app = QApplication([])
    window = HeaderGeneratorApp()
    window.show()
    app.exec_()
