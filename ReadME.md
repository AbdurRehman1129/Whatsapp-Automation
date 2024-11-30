
---

# WhatsApp Business Automation Script

This Python script automates interactions with WhatsApp Business (Work Profile) using ADB (Android Debug Bridge). It simplifies the process of opening the app, entering phone numbers, and interacting with UI elements such as buttons. The script is useful for managing large-scale phone number verifications or testing scenarios.

---

## Features

- Launches WhatsApp Business in a work profile.
- Automates tapping on buttons like **Agree and Continue**, **Next**, and **Yes**.
- Enters phone numbers into the designated input field.
- Handles cases where a **Wrong number?** prompt needs to be clicked.
- Handles error messages and dismisses them gracefully.
- Iterates through multiple phone numbers provided by the user.

---

## Prerequisites

### 1. Git Installation
   - **Windows**:  
     Download Git for Windows from [git-scm.com](https://git-scm.com/) and follow the installation steps. During installation, ensure to select "Git from the command line and also from 3rd-party software" in the PATH options.
   - **Linux**:  
     Install Git via your package manager:
     ```bash
     sudo apt update && sudo apt install git -y  # For Debian/Ubuntu
     sudo yum install git                       # For Red Hat-based distros
     ```
   - **macOS**:  
     Install Git using Homebrew:
     ```bash
     brew install git
     ```
   - Verify installation:
     ```bash
     git --version
     ```

### 2. ADB Installation
   - Download ADB from the official Android developer website: [ADB Download](https://developer.android.com/studio/releases/platform-tools).
   - Extract the downloaded archive and add the folder to your system's PATH environment variable.
   - Verify installation by running:
     ```bash
     adb --version
     ```
   - Enable **Developer Options** and **USB Debugging** on your Android device.

### 3. Python Installation
   - Install Python (3.6 or later) from the official website: [Python Download](https://www.python.org/).
   - Add Python to your system's PATH environment variable during installation.
   - Verify installation by running:
     ```bash
     python --version
     ```

### 4. Required Modules
   This script uses the following Python modules, which are built-in and require no additional installation:
   - `subprocess`: To execute ADB commands.
   - `time`: To handle delays between operations.
   - `xml.etree.ElementTree`: To parse XML files for UI element identification.

---

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/AbdurRehman1129/whatsapp-automation.git
   ```
2. Navigate to the project directory:
   ```bash
   cd whatsapp-automation
   ```
3. Ensure Python and ADB are installed and available in your PATH.

---

## Usage

1. Connect your Android device to your computer via USB.
2. Ensure the device is authorized for ADB debugging by running:
   ```bash
   adb devices
   ```
3. Run the script:
   ```bash
   python main.py
   ```
4. Follow the prompts:
   - Enter phone numbers separated by commas when prompted.

---

## Tutorial Video

For a step-by-step guide, check out the tutorial video:  


https://github.com/user-attachments/assets/456bacbd-dc09-49f3-a8f7-ddae873416de

---

## Notes

- The script uses ADB commands to interact with the device. Ensure the device remains connected throughout the process.
- The script assumes the screen resolution is compatible with the specified coordinates for button taps. Modify the coordinates if necessary for your device.
- The resource IDs used in the script (e.g., `com.whatsapp.w4b:id/registration_phone`) are specific to WhatsApp Business. Ensure these IDs are accurate for the version installed on your device.

---

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to submit a pull request or open an issue.

---

## Disclaimer

This script is intended for educational and testing purposes only. Use it responsibly and ensure compliance with WhatsApp's terms of service. The author is not responsible for any misuse or violations.

---

Happy Automating! 😊

--- 

Let me know if you'd like help creating a thumbnail or writing a script for your tutorial video!
