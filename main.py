import os
import re
import json
import argparse
import time
from datetime import datetime
import threading 

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_setup(setup_name, setup_data):
    setups = load_setups()
    setups[setup_name] = setup_data
    with open("setups.json", "w", encoding="utf-8") as f:
        json.dump(setups, f, ensure_ascii=False, indent=4)
    print(f"Setup '{setup_name}' saved successfully!")

def load_setups():
    if os.path.exists("setups.json"):
        with open("setups.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

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
        "continue_button": input("Continue button (After Yes Button) coordinates (x,y): ").strip(),
        "continue_button_2": input("Continue button (Already Login) coordinates (x,y): ").strip(),
        "cancel_button": input("Cancel (Unable to Connect) button coordinates (x,y): ").strip(),
        "submit_button": input("Submit (Banned) button coordinates (x,y): ").strip(),
        "three_dot": input("Three Dot (Banned) coordinates (x,y): ").strip(),
        "register_button": input("Register new number (Banned) button coordinates (x,y): ").strip()
    }

    setup_name = input("Enter a name for this setup: ").strip()
    save_setup(setup_name, setup_data)

def is_check_status(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "Unable to connect." in xml_content

def is_login_not_available(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "Login not available right now" in xml_content

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
    return "Connecting" in xml_content

def is_continue_button(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "com.whatsapp.w4b:id/primary_button" in xml_content and "CONTINUE" in xml_content 

def is_continue_button_1(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "android:id/button1" in xml_content and "Continue" in xml_content

def is_sending_bar(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "Sending code" in xml_content or "Requesting a call" in xml_content or "Requesting SMS instead" in xml_content or "REQUESTING A CALL..." in xml_content or "REQUESTING SMS INSTEAD" in xml_content

def is_submit_bar(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "Submitting" in xml_content

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
    if "Waiting to automatically detect" in xml_content and "Wrong number?" in xml_content or "Enter the 6-digit code" in xml_content and "Wrong number?" in xml_content:
        return "Wrong Number 1"
    elif "You've tried to register" in xml_content and "Wrong number?" in xml_content:
        return "Wrong Number 2"
    elif "Can't send an SMS with your code because you've tried to register" in xml_content and "Wrong number?" in xml_content:
        return "Wrong Number 3"
    else:
        return None

def is_number_temp_banned(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "REQUEST A REVIEW" in xml_content

def is_number_perma_banned(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "REGISTER NEW NUMBER" in xml_content

def is_review_page(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "CHECK REVIEW STATUS" in xml_content

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
    continue_2_coords = tuple(map(int, setup_data["continue_button_2"].split(',')))
    submit_coords = tuple(map(int, setup_data["submit_button"].split(',')))
    register_coords = tuple(map(int, setup_data["register_button"].split(',')))
    three_coords = tuple(map(int, setup_data["three_dot"].split(',')))
    cancel_coords = tuple(map(int, setup_data["cancel_button"].split(',')))


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
    elif button == "submit_button":
        print("Clicking the Submit button...")
        run_adb_command(f"adb -s {device_id} shell input tap {submit_coords[0]} {submit_coords[1]}")
    elif button == "register_button":
        print("Clicking the Register button...")
        run_adb_command(f"adb -s {device_id} shell input tap {register_coords[0]} {register_coords[1]}")
    elif button == "three_dot":
        print("Clicking the Three Dot...")
        run_adb_command(f"adb -s {device_id} shell input tap {three_coords[0]} {three_coords[1]}")
    elif button == "cancel_button":
        print("Clicking the Cancel button...")
        run_adb_command(f"adb -s {device_id} shell input tap {cancel_coords[0]} {cancel_coords[1]}")
    elif button == "continue_button_2":
        print("Clicking the continue button...")
        run_adb_command(f"adb -s {device_id} shell input tap {continue_2_coords[0]} {continue_2_coords[1]}")


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

def check_and_click_agree_button(selected_device,setup_data):
    while(True):
        if is_agree_button(selected_device):
            click_button("agree_button",setup_data,selected_device)
            break
    if use_different_number(selected_device):
        click_button("agree_button",setup_data,selected_device)

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
    print("Waiting for connecting bar to disappear...", end='', flush=True)
    while(True):
        time.sleep(0.5)
        if not is_connecting_bar(selected_device):
            print("\r" + " " * len("Waiting for connecting bar to disappear..."), end='', flush=True)
            print("\rConnecting bar disappeared...")
            time.sleep(0.5)
            break

def wait_for_submit_bar_to_disppear(selected_device):
    while(True):
        if not is_submit_bar(selected_device):
            break

def check_and_click_yes_button(selected_device,setup_data):
    while(True):
        if is_yes_button(selected_device):
            click_button("yes_button",setup_data,selected_device)
            print("Yes button clicked.")
            break

def check_and_click_continue_button(selected_device,setup_data):
    
    if is_continue_button(selected_device):
        click_button("continue_button",setup_data,selected_device)
    
def wait_for_sending_bar_to_disappear(selected_device):
    print("Waiting for Sending bar to disappear...", end='', flush=True)
    while(True):
        time.sleep(0.5)
        if not is_sending_bar(selected_device):
            print("\r" + " " * len("Waiting for sending bar to disappear..."), end='', flush=True)
            print("\rSending bar disappeared...")
            time.sleep(0.5)
            break

def is_need_help(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "NEED HELP GETTING A CODE?" in xml_content

def save_processed_number(cc,phone_number,otp_status):
    file_name = "processed_numbers.json"
    current_time = datetime.now()
    current_date = current_time.strftime("%Y-%m-%d")
    time_str = current_time.strftime("%H:%M:%S")

    # Data structure to save
    new_entry = {
        "Phone_Number": f"+{cc}{phone_number}",
        "Time": time_str,
        "OTP_Status": otp_status
    }

    try:
        # Load existing data from the file
        with open(file_name, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Initialize if file doesn't exist or is invalid
        data = {}

    # Check if the current date exists, if not, initialize it
    if current_date not in data:
        data[current_date] = []

    # Append the new entry under the current date
    data[current_date].append(new_entry)

    # Save updated data back to the file
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)
    
    print(f"Phone number saved with {otp_status}.")

def is_number_banned(device_id):
    if is_number_temp_banned(device_id):
        return True
    elif is_number_perma_banned(device_id):
        return True
    elif is_review_page(device_id):
        return True
    
def check_and_managed_banned_numbers(cc,setup_data, selected_device, phone_number):
    if is_number_temp_banned(selected_device):
        print("Number is Temp Banned.")
        click_button("agree_button", setup_data, selected_device)  # Fixed order
        time.sleep(0.1)
        click_button("submit_button", setup_data, selected_device)  # Fixed order
        wait_for_submit_bar_to_disppear(selected_device)
        click_button("three_dot", setup_data, selected_device)  # Fixed order
        time.sleep(0.1)
        click_button("register_button", setup_data, selected_device)  # Fixed order
        check_and_click_agree_button(selected_device, setup_data)
        save_processed_number(cc,phone_number, "Banned_Requested")
        return
    elif is_number_perma_banned(selected_device):
        print("Number is Perma Banned.")
        click_button("agree_button", setup_data, selected_device)  # Fixed order
        check_and_click_agree_button(selected_device, setup_data)
        save_processed_number(cc,phone_number, "Permanant_Banned")
        return
    elif is_review_page(selected_device):
        print("Already requested.")
        click_button("three_dot", setup_data, selected_device)  # Fixed order
        time.sleep(0.1)
        click_button("register_button", setup_data, selected_device)  # Fixed order
        check_and_click_agree_button(selected_device, setup_data)
        save_processed_number(cc,phone_number, "Already_Requested")
        return

def check_if_one_hour_came(cc,setup_data, selected_device, phone_number):

    if is_one_hour(selected_device):
        click_button("ok_button", setup_data, selected_device)
        save_processed_number(cc,phone_number,"One_Hour")
 
def check_and_click_wrong_number(cc,setup_data,selected_device,phone_number):
    while True:
        if is_wrong_number(selected_device) == "Wrong Number 1":
            print(f"OTP Sent..")
            threading.Thread(target=save_processed_number, args=(cc,phone_number, "OTP_Sent")).start()
            click_button("wrong_number_1",setup_data,selected_device)
            break
        elif is_wrong_number(selected_device) == "Wrong Number 2":
            print(f"Already Tried..")
            threading.Thread(target=save_processed_number, args=(cc,phone_number, "Already_Tried")).start()
            click_button("wrong_number_2",setup_data,selected_device)
            break
        elif is_wrong_number(selected_device) == "Wrong Number 3":
            print(f"Already Tried..")
            threading.Thread(target=save_processed_number, args=(cc,phone_number, "Already_Tried")).start()
            click_button("wrong_number_3",setup_data,selected_device)
            break
 
def check_and_click_wrong_number_last(setup_data,selected_device,phone_number):
    while True:
        if is_wrong_number(selected_device) == "Wrong Number 1":
            click_button("wrong_number_1",setup_data,selected_device)
            break
        elif is_wrong_number(selected_device) == "Wrong Number 2":
            click_button("wrong_number_2",setup_data,selected_device)
            break
        elif is_wrong_number(selected_device) == "Wrong Number 3":
            click_button("wrong_number_3",setup_data,selected_device)
            break


def manage_check(cc,device_id,setup_data,element,phone_number,index):
    if element == "first" and is_check_status(device_id):
        click_button("cancel_button",setup_data,device_id)
        click_next_button(device_id,setup_data)
        wait_for_connecting_bar_to_disappear(device_id)
        manage_check(cc,device_id,setup_data,"first",phone_number,index)
    elif element == "second" and is_check_status(device_id):
        click_button("cancel_button",setup_data,device_id)
        check_and_click_wrong_number(cc,setup_data,device_id,phone_number)
        automate(selected_device,setup_data,phone_number,index)

def manage_this(cc,selected_device,setup_data,index,phone_number):
    banned = False
    while True:
        if is_yes_button(selected_device):
            click_button("yes_button",setup_data,selected_device)
            break
        elif is_continue_button_1(selected_device):
            click_button("continue_button_2",setup_data,selected_device)
            if is_need_help(selected_device):
                click_button("need_help",setup_data,selected_device)

            break
        elif is_number_banned(selected_device):
            banned = True
            check_and_managed_banned_numbers(cc,setup_data, selected_device, phone_number)
            print("Number is banned and its work is completed.")
            return banned
        elif is_check_status(selected_device):
            manage_check(cc,selected_device,setup_data,"first",phone_number,index)
            break
    
def use_different_number(device_id):
    run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "USE A DIFFERENT NUMBER" in xml_content

def close_and_open_whatsapp(selected_device,work_profile_id=None):
    run_adb_command(f"adb -s {selected_device} shell am force-stop com.whatsapp.w4b")
    time.sleep(1)
    open_whatsapp_business(selected_device,work_profile_id=work_profile_id)

def manage_last(cc,setup_data,selected_device,phone_number,index,work_profile_id):
    while True:
        
            if is_one_hour(selected_device):
                check_if_one_hour_came(cc,setup_data,selected_device,phone_number)
                one_hour = "one_hour"
                return one_hour
            elif is_wrong_number(selected_device):
                check_and_click_wrong_number(cc,setup_data,selected_device,phone_number)
                wrong_number = "wrong_number"
                return wrong_number
            elif is_check_status(selected_device):    
                manage_check(cc,selected_device,setup_data,"second",phone_number,index)
                break
            elif is_login_not_available(selected_device): 
                print("Login not available right now.")
                save_processed_number(cc,phone_number,"Login_Not_Available")
                print("Closing and opening WhatsApp...")   
                close_and_open_whatsapp(selected_device,work_profile_id)
                check_and_click_agree_button(selected_device,setup_data)
                
                login_not_available = "login_not_available"
                return login_not_available
            
            else:
                continue
            
    
def automate(selected_device,setup_data,phone_number,index,work_profile_id,total,cc):
    clear_screen()
    print(f"{index}/{total}. Processing phone number +{cc}{phone_number}")
    check_and_click_input_number(selected_device,setup_data)
    enter_phone_number(selected_device,phone_number)
    click_next_button(selected_device,setup_data)
    wait_for_connecting_bar_to_disappear(selected_device)
    time.sleep(0.5)
    banned = manage_this(cc,selected_device,setup_data,index,phone_number)
    if banned:
        return
    check_and_click_continue_button(selected_device,setup_data)
    if is_sending_bar(selected_device):
        wait_for_sending_bar_to_disappear(selected_device)
    time.sleep(0.5)
    something = manage_last(cc,setup_data, selected_device, phone_number, index,work_profile_id)
    if something == "login_not_available" or something == "wrong_number":
        return
    elif something == "one_hour":
        check_and_click_wrong_number_last(setup_data,selected_device,phone_number)

def automate_login(selected_device,setup_data,work_profile_id):
    phone_numbers = input("Enter phone numbers separated by commas: ").split(',')
    phone_numbers = [phone_number.strip() for phone_number in phone_numbers if phone_number.strip()]
    cc = input("Enter country code: ")
    total = len(phone_numbers)
    check_and_click_agree_button(selected_device,setup_data)
    for index,phone_number in enumerate(phone_numbers,start=1):
        automate(selected_device,setup_data,phone_number,index,work_profile_id,total,cc)


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
            close_and_open_whatsapp(selected_device,work_profile_id)
        else:
            close_and_open_whatsapp(selected_device,work_profile_id=None)
    else:
        print("No work profile detected. Launching WhatsApp Business in the main profile.")
        close_and_open_whatsapp(selected_device,work_profile_id=None)


    automate_login(selected_device,setup_data,work_profile_id)
