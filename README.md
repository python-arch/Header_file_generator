# Header File Generator

This Repository introduces a simple script and GUI program to accept the parameters needed for the header file generated for the ESP32 microcontroller in the IOT project. 

**The project is still in the phase of the proof of concept :) , it will be updated frequently.**

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

## Authors

- [Abdelrahman El Sayed](https://github.com/python_arch)
