import subprocess
import time
import xml.etree.ElementTree as ET


def open_whatsapp_business(work_profile_id):
    package_name = "com.whatsapp.w4b"
    activity_name = "com.whatsapp.Main"
    subprocess.run(["adb", "shell", "am", "start", "--user", str(work_profile_id), "-n",
                   f"{package_name}/{activity_name}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("WhatsApp Business has been successfully launched in the work profile.")
    time.sleep(2)


def click_agree_and_continue():
    try:
        subprocess.run(["adb", "shell", "input", "tap", "540", "2318"],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Successfully clicked the 'Agree and Continue' button.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while clicking the button: {e}")


def enter_phone_number(phone_number, max_retries=10, delay=2):
    retries = 0
    phone_number_field_found = False
    next_button_found = False

    while retries < max_retries:
        try:
            subprocess.run(["adb", "shell", "uiautomator", "dump"], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["adb", "pull", "/sdcard/window_dump.xml", "./window_dump.xml"],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            tree = ET.parse('./window_dump.xml')
            root = tree.getroot()

            for node in root.iter("node"):
                if node.attrib.get("resource-id") == "com.whatsapp.w4b:id/registration_phone":
                    phone_number_field_found = True
                    break

            if phone_number_field_found:
                subprocess.run(["adb", "shell", "input", "text", phone_number],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"Phone number '{phone_number}' successfully entered.")

                for node in root.iter("node"):
                    if node.attrib.get("resource-id") == "com.whatsapp.w4b:id/registration_submit":
                        next_button_found = True
                        break

                if next_button_found:
                    subprocess.run(["adb", "shell", "input", "tap", "540", "1575"],
                                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print("Successfully clicked the 'Next' button.")
                    break
                else:
                    print(f"'Next' button not found. Attempt {
                          retries + 1} of {max_retries}.")
            else:
                print(f"Phone number input field not found. Attempt {
                      retries + 1} of {max_retries}.")

        except subprocess.CalledProcessError as e:
            print(f"Error during phone number entry. Attempt {
                  retries + 1} of {max_retries}: {e}")
        except Exception as e:
            print(f"Unexpected error. Attempt {
                  retries + 1} of {max_retries}: {e}")

        retries += 1
        time.sleep(delay)

    if not phone_number_field_found:
        print(f"Failed to locate the phone number input field after {
              max_retries} attempts.")
    if not next_button_found:
        print(f"Failed to locate the 'Next' button after {
              max_retries} attempts.")


def click_yes_button(max_retries=10, delay=4):
    retries = 0
    yes_button_found = False

    while retries < max_retries:
        try:
            subprocess.run(["adb", "shell", "uiautomator", "dump"], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["adb", "pull", "/sdcard/window_dump.xml", "./window_dump.xml"],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            tree = ET.parse('./window_dump.xml')
            root = tree.getroot()

            for node in root.iter("node"):
                if node.attrib.get("resource-id") == "android:id/button1" and node.attrib.get("text") == "Yes":
                    yes_button_found = True
                    break

            if yes_button_found:
                subprocess.run(["adb", "shell", "input", "tap", "813", "1417"],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("Successfully clicked the 'Yes' button.")
                break
            else:
                print(f"'Yes' button not found. Attempt {
                      retries + 1} of {max_retries}.")

        except subprocess.CalledProcessError as e:
            print(f"Error while clicking the 'Yes' button. Attempt {
                  retries + 1} of {max_retries}: {e}")
        except Exception as e:
            print(f"Unexpected error while clicking the 'Yes' button. Attempt {
                  retries + 1} of {max_retries}: {e}")

        retries += 1
        time.sleep(delay)

    if not yes_button_found:
        print(f"Failed to locate the 'Yes' button after {
              max_retries} attempts.")


wrong_number_pressed = False


def check_and_click_continue_button(max_retries=10, delay=4):
    global wrong_number_pressed
    retries = 0
    continue_button_found = False
    error_message_found = False

    while retries < max_retries:
        try:
            subprocess.run(["adb", "shell", "uiautomator", "dump"], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["adb", "pull", "/sdcard/window_dump.xml", "./window_dump.xml"],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            tree = ET.parse('./window_dump.xml')
            root = tree.getroot()

            wrong_number_button_found = False
            for node in root.iter("node"):
                if node.attrib.get("content-desc") == "Wrong number?":
                    wrong_number_button_found = True
                    break

            if wrong_number_button_found:
                subprocess.run(["adb", "shell", "input", "tap", "733", "366"],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(["adb", "shell", "input", "tap", "733", "511"],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("Successfully clicked the 'Wrong number?' button.")
                wrong_number_pressed = True
                break

            for node in root.iter("node"):
                if node.attrib.get("resource-id") == "android:id/message" and node.attrib.get("text") == "We couldn't send an SMS to your number. Please check your number and try again in 1 hour.":
                    error_message_found = True
                    break

            if error_message_found:
                subprocess.run(["adb", "shell", "input", "tap", "813", "1417"],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(
                    "Successfully clicked the 'OK' button to dismiss the error message.")
                break

            for node in root.iter("node"):
                if node.attrib.get("resource-id") == "com.whatsapp.w4b:id/primary_button" and node.attrib.get("text") == "CONTINUE":
                    continue_button_found = True
                    break

            if continue_button_found:
                subprocess.run(["adb", "shell", "input", "tap", "540", "2220"],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("Successfully clicked the 'Continue' button.")
            else:
                print(f"'Continue' button not found. Attempt {
                      retries + 1} of {max_retries}.")

        except subprocess.CalledProcessError as e:
            print(f"Error while checking for buttons. Attempt {
                  retries + 1} of {max_retries}: {e}")
        except Exception as e:
            print(f"Unexpected error while checking for buttons. Attempt {
                  retries + 1} of {max_retries}: {e}")

        retries += 1
        time.sleep(delay)

    if not continue_button_found and not wrong_number_pressed:
        print(f"Failed to locate 'Continue' or 'Wrong number?' buttons after {
              max_retries} attempts.")


def check_and_click_wrong_number_button(max_retries=10, delay=4):
    global wrong_number_pressed
    if wrong_number_pressed:
        print("Skipping the 'Wrong number?' button click as it has already been pressed.")
        return

    retries = 0
    while retries < max_retries:
        try:
            subprocess.run(["adb", "shell", "uiautomator", "dump"], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["adb", "pull", "/sdcard/window_dump.xml", "./window_dump.xml"],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            tree = ET.parse('./window_dump.xml')
            root = tree.getroot()

            wrong_number_button_found = False
            for node in root.iter("node"):
                if node.attrib.get("content-desc") == "Wrong number?":
                    wrong_number_button_found = True
                    break

            if wrong_number_button_found:
                subprocess.run(["adb", "shell", "input", "tap", "733", "366"],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(["adb", "shell", "input", "tap", "733", "511"],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("Successfully clicked the 'Wrong number?' button.")
                wrong_number_pressed = True
                break
            else:
                print(f"'Wrong number?' button not found. Attempt {
                      retries + 1} of {max_retries}.")

        except subprocess.CalledProcessError as e:
            print(f"Error while checking for the 'Wrong number?' button or error message. Attempt {
                  retries + 1} of {max_retries}: {e}")
        except Exception as e:
            print(f"Unexpected error. Attempt {
                  retries + 1} of {max_retries}: {e}")

        retries += 1
        time.sleep(delay)

    if retries >= max_retries:
        print(f"Failed to locate the 'Wrong number?' button after {
              max_retries} attempts.")

# Main script execution


open_whatsapp_business(11)
click_agree_and_continue()
numbers_input = input("Enter phone numbers separated by commas: ")
phone_numbers = [number.strip() for number in numbers_input.split(",")]

for index,phone_number in enumerate(phone_numbers,start=1):
    print(f"\n{index}. Processing phone number: {phone_number}")
    wrong_number_pressed = False
    enter_phone_number(phone_number)
    time.sleep(1)
    click_yes_button()
    time.sleep(1)
    check_and_click_continue_button()
    time.sleep(1)
    check_and_click_wrong_number_button()
    time.sleep(1)
