import os
import time

def open_whatsapp():
    # Launch WhatsApp
    os.system("adb shell monkey -p com.whatsapp -c android.intent.category.LAUNCHER 1")
    print("WhatsApp opened.")

def click_agree_continue():
    # Wait for WhatsApp to load and the EULA page to appear
    time.sleep(3)
    # Tap the "Agree and Continue" button (coordinates or resource ID)
    os.system('adb shell input tap 540 2318')  # Adjust if necessary
    print("Tapped 'Agree and Continue'.")

def enter_phone_number():
    # Ask the user for the phone number
    phone_number = input("Please enter your phone number: ")
    
    # Wait for the phone number page to appear
    time.sleep(3)
    
    # Enter the phone number (replace with the correct resource ID)
    os.system(f'adb shell input text "{phone_number}"')
    print(f"Entered phone number: {phone_number}")
    
    # Tap the "Next" button using coordinates (adjust if necessary)
    os.system('adb shell input tap 540 1585')  # Adjust coordinates for "Next"
    print("Tapped 'Next'.")

def handle_yes_or_continue():
    start_time = time.time()  # Record the start time
    timeout = 60  # Set timeout period to 60 seconds

    while time.time() - start_time < timeout:
        # Wait a few seconds to let the screen load
        time.sleep(3)

        # Dump the UI XML file
        os.system('adb shell uiautomator dump /sdcard/ui.xml')
        os.system('adb pull /sdcard/ui.xml')

        # Open the XML file and search for specific elements by resource ID or text
        with open('ui.xml', 'r', encoding='utf-8') as f:
            ui_content = f.read()

        # Check for the "Yes" button
        if 'resource-id="android:id/button1"' in ui_content and 'text="YES"' in ui_content:
            os.system('adb shell input tap 813 1437')  # Adjusted coordinates for "Yes"
            print("Tapped 'Yes'.")
            os.remove('ui.xml')  # Delete the XML file after use
            return True

        # Check for the "Continue" button
        elif 'resource-id="com.whatsapp:id/submit"' in ui_content and 'text="CONTINUE"' in ui_content:
            os.system('adb shell input tap 540 2220')  # Adjusted coordinates for "Continue"
            print("Tapped 'Continue'.")
            os.remove('ui.xml')  # Delete the XML file after use
            return True

        else:
            # Delete the XML file if no button was found
            os.remove('ui.xml')
            print("Neither 'Yes' nor 'Continue' button found, retrying...")

    if time.time() - start_time >= timeout:
        print("Timeout reached, no button found.")
        return False

def handle_ok_or_wrong_number():
    start_time = time.time()  # Record the start time
    timeout = 60  # Set timeout period to 60 seconds

    while time.time() - start_time < timeout:
        # Wait a few seconds to let the screen load
        time.sleep(3)

        # Dump the UI XML file
        os.system('adb shell uiautomator dump /sdcard/ui.xml')
        os.system('adb pull /sdcard/ui.xml')

        # Open the XML file and search for specific elements by resource ID or text
        with open('ui.xml', 'r', encoding='utf-8') as f:
            ui_content = f.read()

        # Check for the "OK" button (1-hour wait page)
        if 'resource-id="android:id/button1"' in ui_content and 'text="OK"' in ui_content:
            os.system('adb shell input tap 813 1437')  # Adjusted coordinates for "OK"
            print("Tapped 'OK' on 1-hour wait page.")
            os.remove('ui.xml')  # Delete the XML file after use
            break

        # Check for the "Wrong number?" button
        elif 'resource-id="com.whatsapp:id/send_code_description"' in ui_content and 'content-desc="Wrong number?"' in ui_content:
            os.system('adb shell input tap 540 566')  # Adjusted coordinates for "Wrong number?"
            print("Tapped 'Wrong number?'.")
            os.remove('ui.xml')  # Delete the XML file after use
            break

        else:
            # Delete the XML file if no button was found
            os.remove('ui.xml')
            print("Neither 'OK' nor 'Wrong number?' button found, retrying...")

    if time.time() - start_time >= timeout:
        print("Timeout reached, no button found.")

if __name__ == "__main__":
    open_whatsapp()
    click_agree_continue()
    enter_phone_number()

    # First handle "Yes" or "Continue"
    if handle_yes_or_continue():
        # After handling "Yes" or "Continue", check for "OK" or "Wrong number?"
        handle_ok_or_wrong_number()
