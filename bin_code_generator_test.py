import os
import subprocess

# Path to the Arduino IDE installation directory
arduino_path = "/Users/python/Downloads/Arduino.app/Contents/MacOS/"

# Path to the Arduino project directory containing the code
project_path = "/Users/python/Desktop/sketch_mar17a"

# Name of the Arduino code file
code_file = "sketch_mar17a.ino"

# # Compile the Arduino code to generate the binary files
# subprocess.run([os.path.join(arduino_path, "arduino"),
#                 "--verify",
#                 os.path.join(project_path, code_file)])

# Compile the Arduino code to generate the binary files
subprocess.run(["arduino-cli", "compile", "--fqbn", "esp32:esp32:esp32", os.path.join(project_path, code_file)])

# Replace "esp32:esp32:esp32" with the correct board configuration for your ESP32 board

# Flash the binary files onto the ESP32
# subprocess.run(["arduino-cli", "upload", "--port", "/dev/cu.SLAB_USBtoUART", "--fqbn", "esp32:esp32:esp32", os.path.join(project_path, code_file)])
