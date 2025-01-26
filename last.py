import os
import re
import json
import argparse

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_setup(setup_name, setup_data):
    setups = load_setups()
    setups[setup_name] = setup_data
    with open("setups.json", "w", encoding="utf-8") as f:
        json.dump(setups, f, ensure_ascii=False, indent=4)
    print(f"Setup '{setup_name}' saved successfully!")

# Function to load all setups
def load_setups():
    if os.path.exists("setups.json"):
        with open("setups.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Function to load a specific setup
def load_setup_by_name(setup_name):
    setups = load_setups()
    if setup_name in setups:
        return setups[setup_name]
    else:
        print(f"Setup '{setup_name}' not found!")
        return None
def setup_coordinates():
    print("Please enter the coordinates for the following UI elements:")

    # Collect the coordinates
    setup_data = {
        "agree_button": input("Agree button coordinates (x,y): ").strip(),
        "number_input": input("Number Input field coordinates (x,y): ").strip(),
        "next_button": input("Next button coordinates (x,y): ").strip(),
        "yes_button": input("Yes button coordinates (x,y): ").strip(),
        "ok_button": input("OK button coordinates (x,y): ").strip(),
        "wrong_number_1": input("Wrong number (Waiting for) button coordinates (x,y): ").strip(),
        "wrong_number_2": input("Wrong number (You've tried) button coordinates (x,y): ").strip(),
        "wrong_number_3": input("Wrong number (Can't send) button coordinates (x,y): ").strip(),
        "continue_button": input("Continue button coordinates (x,y): ").strip()
    }

    setup_name = input("Enter a name for this setup: ").strip()
    save_setup(setup_name, setup_data)

def is_agree_button(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "com.whatsapp.w4b:id/eula_accept" in xml_content

def is_input_phone_field(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "com.whatsapp.w4b:id/registration_phone" in xml_content

def is_yes_button(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "android:id/button1" in xml_content and "Yes" in xml_content

def is_connecting_bar(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "Connecting..." in xml_content

def is_continue_button(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "com.whatsapp.w4b:id/primary_button" in xml_content and "CONTINUE" in xml_content

def is_sending_bar(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "Sending code" in xml_content

def is_one_hour(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "OK" in xml_content and "android:id/button1" in xml_content
def is_wrong_number(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    if "Waiting to automatically detect" in xml_content and "Wrong number?" in xml_content:
        return "Wrong Number 1"
    elif "You've tried to register" in xml_content and "Wrong number?" in xml_content:
        return "Wrong Number 2"
    elif "Can't send an SMS with your code because you've tried to register" in xml_content and "Wrong number?" in xml_content:
        return "Wrong Number 3"
    else:
        return None
    
def click_button(button,setup_data,device_id):
    agree_coords = tuple(map(int, setup_data["agree_button"].split(',')))
    number_coords = tuple(map(int, setup_data["number_input"].split(',')))
    next_coords = tuple(map(int, setup_data["next_button"].split(',')))
    yes_coords = tuple(map(int, setup_data["yes_button"].split(',')))
    ok_coords = tuple(map(int, setup_data["ok_button"].split(',')))
    wrong_1_coords = tuple(map(int, setup_data["wrong_number_1"].split(',')))
    wrong_2_coords = tuple(map(int, setup_data["wrong_number_2"].split(',')))
    wrong_3_coords = tuple(map(int, setup_data["wrong_number_3"].split(',')))
    continue_coords = tuple(map(int, setup_data["continue_button"].split(',')))

    if button == "agree_button":
        print("Clicking the agree button...")
        run_adb_command(f"adb -s {device_id} shell input tap {agree_coords[0]} {agree_coords[1]}")
    elif button == "number_input":
        print("Clicking the number input field...")
        run_adb_command(f"adb -s {device_id} shell input tap {number_coords[0]} {number_coords[1]}")
    elif button == "next_button":
        print("Clicking the Next button...")
        run_adb_command(f"adb -s {device_id} shell input tap {next_coords[0]} {next_coords[1]}")
    elif button == "yes_button":
        print("Clicking the Yes button...")
        run_adb_command(f"adb -s {device_id} shell input tap {yes_coords[0]} {yes_coords[1]}")
    elif button == "ok_button":
        print("Clicking the OK button...")
        run_adb_command(f"adb -s {device_id} shell input tap {ok_coords[0]} {ok_coords[1]}")
    elif button == "wrong_number_1":
        print("Clicking the Wrong Number...")
        run_adb_command(f"adb -s {device_id} shell input tap {wrong_1_coords[0]} {wrong_1_coords[1]}")
    elif button == "wrong_number_2":
        print("Clicking the Wrong Number...")
        run_adb_command(f"adb -s {device_id} shell input tap {wrong_2_coords[0]} {wrong_2_coords[1]}")
    elif button == "wrong_number_3":
        print("Clicking the Wrong Number...")
        run_adb_command(f"adb -s {device_id} shell input tap {wrong_3_coords[0]} {wrong_3_coords[1]}")
    elif button == "continue_button":
        print("Clicking the continue button...")
        run_adb_command(f"adb -s {device_id} shell input tap {continue_coords[0]} {continue_coords[1]}")

def run_adb_command(command):
    return os.system(f"{command} >nul 2>&1")  # Redirect stdout to null, keep stderr

def get_connected_devices():
    devices_output = os.popen("adb devices").read()
    devices = []
    if devices_output:
        for line in devices_output.split("\n")[1:]:
            if line.strip():
                parts = line.split("\t")
                if len(parts) == 2 and parts[1] == "device":
                    devices.append(parts[0])
    return devices

def check_work_profile(device_id):
    try:
        # Execute the ADB command for the specific device
        output = os.popen(f"adb -s {device_id} shell pm list users").read()
        
        # Search for the work profile in the output
        match = re.search(r'UserInfo\{(\d+):Work profile:\d+\}', output)
        
        if match:
            # Extract the work profile ID
            work_profile_id = match.group(1)
            return work_profile_id
        else:
            return None  # No work profile found
    
    except Exception as e:
        return f"Error: {str(e)}"

def open_whatsapp_business(device_id, work_profile_id=None):
    if work_profile_id:
        profile_prefix = f"--user {work_profile_id} "
    else:
        profile_prefix = ""

    # Use 'am start' instead of 'monkey' for better control
    command = f"adb -s {device_id} shell am start {profile_prefix}-n com.whatsapp.w4b/com.whatsapp.Main"
    result = run_adb_command(command)  # Use the helper function here
    if result == 0:
        print("WhatsApp Business launched successfully.")
    else:
        print("Failed to launch WhatsApp Business.")

# Function to handle device selection and WhatsApp launch
#def main():
    
def check_and_click_agree_button(selected_device,setup_data):
    while(True):
        if is_agree_button(selected_device):
            click_button("agree_button",setup_data,selected_device)
            break
def check_and_click_input_number(selected_device,setup_data):
    while(True):
        if is_input_phone_field(selected_device):
            click_button("number_input",setup_data,selected_device)
            break
def enter_phone_number(selected_device,phone_number):
    print(f"Entering phone number +994{phone_number}")
    run_adb_command(f"adb -s {selected_device} shell input text {phone_number}")

def click_next_button(selected_device,setup_data):
    click_button("next_button",setup_data,selected_device)
            
def wait_for_connecting_bar_to_disappear(selected_device):
    while(True):
        if not is_connecting_bar(selected_device):
            break

def check_and_click_yes_button(selected_device,setup_data):
    while(True):
        if is_yes_button(selected_device):
            click_button("yes_button",setup_data,selected_device)
            break
def check_and_click_continue_button(selected_device,setup_data):
    
    if is_continue_button(selected_device):
        click_button("continue_button",setup_data,selected_device)
    

def wait_for_sending_bar_to_disappear(selected_device):
    while(True):
        if not is_sending_bar(selected_device):
            break

# Function to save the processed numbers
def save_processed_number(phone_number):
    file_name = "processed_numbers.json"
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            processed_numbers = json.load(f)
    else:
        processed_numbers = []

    # Avoid duplicates
    if phone_number not in processed_numbers:
        processed_numbers.append(phone_number)
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(processed_numbers, f, ensure_ascii=False, indent=4)
        print(f"Phone number +994{phone_number} saved to processed list.")

# Update the check_if_one_hour_came function
def check_if_one_hour_came(setup_data, selected_device, phone_number):
    if is_one_hour(selected_device):
        click_button("ok_button", setup_data, selected_device)
    elif is_wrong_number(selected_device) == "Wrong Number 2":
        print("Number was already tried....")
    elif is_wrong_number(selected_device) == "Wrong Number 1":
        print("OTP Sent....")
        save_processed_number(phone_number)


def check_and_click_wrong_number(setup_data,selected_device):
    if is_wrong_number(selected_device) == "Wrong Number 1":
        click_button("wrong_number_1",setup_data,selected_device)
    elif is_wrong_number(selected_device) == "Wrong Number 2":
        click_button("wrong_number_2",setup_data,selected_device)
    elif is_wrong_number(selected_device) == "Wrong Number 3":
        click_button("wrong_number_3",setup_data,selected_device)


def automate_login(selected_device,setup_data):
    
    check_and_click_agree_button(selected_device,setup_data)

    phone_numbers = input("Enter phone numbers separated by commas: ").split(',')
    phone_numbers = [phone_number.strip() for phone_number in phone_numbers if phone_number.strip()]
    for index,phone_number in enumerate(phone_numbers,start=1):
        clear_screen()
        print(f"{index}. Processing phone number +994{phone_number}")
        check_and_click_input_number(selected_device,setup_data)
        enter_phone_number(selected_device,phone_number)
        click_next_button(selected_device,setup_data)
        wait_for_connecting_bar_to_disappear(selected_device)
        check_and_click_yes_button(selected_device,setup_data)
        check_and_click_continue_button(selected_device,setup_data)
        wait_for_sending_bar_to_disappear(selected_device)
        check_if_one_hour_came(setup_data,selected_device,phone_number)
        check_and_click_wrong_number(setup_data,selected_device)


if __name__ == "__main__":
    clear_screen()
    parser = argparse.ArgumentParser(description="Automate SafeUM login process.")
    parser.add_argument("--setup", type=str, help="Specify the setup name to use.")
    args = parser.parse_args()

    # If a setup name is provided, load that setup
    setup_data = None
    if args.setup:
        setup_data = load_setup_by_name(args.setup)
        if setup_data:
            print(f"Loaded setup '{args.setup}' successfully.")
    
    if setup_data is None:
        # If no setup is provided or failed to load, ask the user to create a new one
        print("No setup provided or failed to load, please create a new one.")
        setup_coordinates()
    
    
    devices = get_connected_devices()
    if not devices:
        print("No devices connected.")
        
    elif len(devices) == 1:
        selected_device = devices[0]
    else:
        print("Connected devices:")
        for i, device in enumerate(devices):
            print(f"{i + 1}. {device}")
        choice = input("Select a device (1, 2, ...): ").strip()
        try:
            selected_device = devices[int(choice) - 1]
        except (IndexError, ValueError):
            print("Invalid choice. Exiting.")
            

    work_profile_id = check_work_profile(selected_device)

    if work_profile_id:
        print(f"Work profile detected with ID: {work_profile_id}")
        profile_choice = input("Open WhatsApp Business in (1) Main Profile or (2) Work Profile? ").strip()
        if profile_choice == "2":
            open_whatsapp_business(selected_device, work_profile_id)
        else:
            open_whatsapp_business(selected_device)
    else:
        print("No work profile detected. Launching WhatsApp Business in the main profile.")
        open_whatsapp_business(selected_device)


    automate_login(selected_device,setup_data)
    
            
