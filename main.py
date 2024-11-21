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

def click_continue_or_yes():
    start_time = time.time()  # Record the start time
    timeout = 60  # Set timeout period to 60 seconds

    while time.time() - start_time < timeout:
        # Wait a few seconds to let the screen load
        time.sleep(3)

        # Dump the UI XML file
        os.system('adb shell uiautomator dump /sdcard/ui.xml')
        os.system('adb pull /sdcard/ui.xml')

        # Open the XML file and search for the "YES" or "CONTINUE" button by resource ID or text
        with open('ui.xml', 'r', encoding='utf-8') as f:
            ui_content = f.read()

        # Check if the "Yes" button is found by resource ID
        if 'resource-id="android:id/button1"' in ui_content:
            # Tap the "Yes" button (coordinates extracted from the XML)
            os.system('adb shell input tap 813 1437')  # Adjusted coordinates for the "Yes" button
            print("Tapped 'Yes'.")
            os.remove('ui.xml')  # Delete the XML file after use
            break
        elif 'text="CONTINUE"' in ui_content:  # Alternatively, search for CONTINUE text if needed
            # Tap the "Continue" button (adjust coordinates if necessary)
            os.system('adb shell input tap 540 2220')  # Adjust coordinates for "Continue"
            print("Tapped 'Continue'.")
            os.remove('ui.xml')  # Delete the XML file after use
            break
        else:
            # Delete the XML file if no button was found
            os.remove('ui.xml')
            print("Neither 'Continue' nor 'Yes' button found, retrying...")

    if time.time() - start_time >= timeout:
        print("Timeout reached, no button found.")

def click_ok_button():
    start_time = time.time()  # Record the start time
    timeout = 60  # Set timeout period to 60 seconds

    while time.time() - start_time < timeout:
        # Wait a few seconds to let the screen load
        time.sleep(3)

        # Dump the UI XML file
        os.system('adb shell uiautomator dump /sdcard/ui.xml')
        os.system('adb pull /sdcard/ui.xml')

        # Open the XML file and search for the "OK" button by resource ID or text
        with open('ui.xml', 'r', encoding='utf-8') as f:
            ui_content = f.read()

        # Check if the "OK" button is found by resource ID
        if 'resource-id="android:id/button1"' in ui_content:
            # Tap the "OK" button (coordinates extracted from the XML)
            os.system('adb shell input tap 813 1437')  # Adjusted coordinates for the "OK" button
            print("Tapped 'OK' button.")
            os.remove('ui.xml')  # Delete the XML file after use
            break
        else:
            # Delete the XML file if no button was found
            os.remove('ui.xml')
            print("'OK' button not found, retrying...")

    if time.time() - start_time >= timeout:
        print("Timeout reached, 'OK' button not found.")

def capture_ui_dump():
    # Capture the UI dump using ADB
    os.system('adb shell uiautomator dump /sdcard/window_dump.xml')
    os.system('adb pull /sdcard/window_dump.xml .')
    print("UI dump captured and saved as window_dump.xml.")

def click_wrong_number_button():
    start_time = time.time()  # Record the start time
    timeout = 60  # Set timeout period to 60 seconds

    while time.time() - start_time < timeout:
        # Wait a few seconds to let the screen load
        time.sleep(3)

        # Capture the UI dump again after handling previous buttons
        capture_ui_dump()

        # Open the window_dump.xml file and search for the "Wrong number?" button
        with open('window_dump.xml', 'r', encoding='utf-8') as f:
            ui_content = f.read()

        # Debugging: print part of the XML content to verify
        print("Checking UI XML for 'Wrong number?' button...")

        # Check if the "Wrong number?" button is found by either text or content-desc
        if 'text="Wrong number?"' in ui_content or 'content-desc="Wrong number?"' in ui_content:
            print("'Wrong number?' button found.")
            # Extract coordinates of the button
            # You could extract the bounds of the button if necessary
            # Here we assume the position to be at (733, 536) (adjust if necessary)
            os.system('adb shell input tap 733 536')  # Coordinates for 'Wrong number?' button
            print("Tapped 'Wrong number?' button.")
            break
        else:
            print("'Wrong number?' button not found, retrying...")

    if time.time() - start_time >= timeout:
        print("Timeout reached, 'Wrong number?' button not found.")

if __name__ == "__main__":
    open_whatsapp()
    click_agree_continue()
    enter_phone_number()
    click_continue_or_yes()
    click_ok_button()  # Handle the "OK" button
    click_wrong_number_button()  # Handle the "Wrong number?" button
