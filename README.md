# Tornado Flusher

Tornado Flasher is a PyQt5 application for generating headers and uploading code to ESP32 devices. This application is designed to simplify the process of configuring IoT devices, specifically for Azure IoT Hub, by generating necessary header files and handling the compilation and uploading of Arduino code to ESP32 devices.

**The project is still in the phase of the proof of concept :) , it will be updated frequently.**

## Copyright

© 2016 El-ARABY Research and Development Center. All Rights Reserved.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them.

- Python 3.9+
- Pip (Python package installer)

### Installing

A step-by-step series of examples that tell you how to get a development env running.

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/your_repository.git
   ```

2. Navigate to the project directory:

   ```bash
   cd your_repository
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

5. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Script

Explain how to run the script or the GUI program.

#### Running the Script

If it's a command-line script:

```bash
python header_file_generator_xxx.py
```

#### Running the GUI Program

If it's a GUI program:

```bash
python header_file_generator_GUI.py
```

### Building an Executable

Explain how to use PyInstaller to build the script into an executable.

1. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Navigate to the project directory:

   ```bash
   cd your_repository
   ```

3. Build the executable:

   ```bash
   pyinstaller --onefile header_file_generator_GUI.py
   ```

This will create a `dist` directory containing the executable file.

To create a README file for your PyQt5 application, you can provide an overview of the application, its features, and how to use it. Here's an example README for your `HeaderGeneratorApp`:

---

# Tornado Flasher (No_EXCEL Version)

## Features
- **Brand, Product, and Model Selection**: Select the brand, product, and model of the IoT device.
- **Compile and Upload**: Compile and upload Arduino code to the selected device.
- **Azure IoT Hub Configuration**: Automatically configure devices with Azure IoT Hub using X.509 authentication.
- **Customizable Header Generation**: Generate custom header files for IoT device configuration.

## Installation
1. Clone the repository: `git clone https://github.com/python-arch/Header_file_generator.git`
2. Install the required dependencies
3. Run the application: `python main.py`

## Usage
1. Select the brand, product, and model of the IoT device from the dropdown menus.
2. Click the "Compile and Upload" button to flash the device.
3. Follow the on-screen instructions to complete the flashing process.
4. If an error occurs during flashing, click the "Skip this device" button to proceed to the next device.

## Authors

- [Abdelrahman El Sayed](https://github.com/python_arch)


