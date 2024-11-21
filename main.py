import os
import time

def run_adb_command(command):
    # Run the ADB command and suppress the output
    os.system(f"{command} > /dev/null 2>&1")

def open_whatsapp():
    # Launch WhatsApp and suppress the verbose output
    run_adb_command("adb shell monkey -p com.whatsapp -c android.intent.category.LAUNCHER 1")
    print("WhatsApp opened.")

def click_agree_continue():
    # Wait for WhatsApp to load and the EULA page to appear
    time.sleep(3)
    # Tap the "Agree and Continue" button (coordinates or resource ID)
    run_adb_command('adb shell input tap 540 2318')  # Adjust if necessary
    print("Tapped 'Agree and Continue'.")

def enter_phone_number(phone_number):
    # Enter the phone number (replace with the correct resource ID)
    run_adb_command(f'adb shell input text "{phone_number}"')
    print(f"Entered phone number: {phone_number}")
    
    # Tap the "Next" button using coordinates (adjust if necessary)
    run_adb_command('adb shell input tap 540 1585')  # Adjust coordinates for "Next"
    print("Tapped 'Next'.")

def click_continue_or_yes():
    start_time = time.time()  # Record the start time
    timeout = 60  # Set timeout period to 60 seconds

    while time.time() - start_time < timeout:
        # Wait a few seconds to let the screen load
        time.sleep(3)

        # Dump the UI XML file
        run_adb_command('adb shell uiautomator dump /sdcard/ui.xml')
        run_adb_command('adb pull /sdcard/ui.xml')

        # Open the XML file and search for the "YES" or "CONTINUE" button by resource ID or text
        with open('ui.xml', 'r', encoding='utf-8') as f:
            ui_content = f.read()

        # Check if the "Yes" button is found by resource ID
        if 'resource-id="android:id/button1"' in ui_content:
            # Tap the "Yes" button (coordinates extracted from the XML)
            run_adb_command('adb shell input tap 813 1437')  # Adjusted coordinates for the "Yes" button
            print("Tapped 'Yes'.")
            os.remove('ui.xml')  # Delete the XML file after use
            break
        elif 'text="CONTINUE"' in ui_content:  # Alternatively, search for CONTINUE text if needed
            # Tap the "Continue" button (adjust coordinates if necessary)
            run_adb_command('adb shell input tap 540 2220')  # Adjust coordinates for "Continue"
            print("Tapped 'Continue'.")
            os.remove('ui.xml')  # Delete the XML file after use
            break
        else:
            # Delete the XML file if no button was found
            os.remove('ui.xml')
            print("Neither 'Continue' nor 'Yes' button found, retrying...")

    if time.time() - start_time >= timeout:
        print("Timeout reached, no button found.")

def click_ok_button(phone_number):
    start_time = time.time()  # Record the start time
    timeout = 60  # Set timeout period to 60 seconds

    while time.time() - start_time < timeout:
        # Wait a few seconds to let the screen load
        time.sleep(3)

        # Dump the UI XML file
        run_adb_command('adb shell uiautomator dump /sdcard/ui.xml')
        run_adb_command('adb pull /sdcard/ui.xml')

        # Open the XML file and search for the "OK" button by resource ID or text
        with open('ui.xml', 'r', encoding='utf-8') as f:
            ui_content = f.read()

        # Check if the "OK" button is found by resource ID
        if 'resource-id="android:id/button1"' in ui_content:
            # Tap the "OK" button (coordinates extracted from the XML)
            run_adb_command('adb shell input tap 813 1437')  # Adjusted coordinates for the "OK" button
            print("Tapped 'OK' button.")
            os.remove('ui.xml')  # Delete the XML file after use

            # Save the number to ONE_Hour.txt if OK button is found
            with open("ONE_Hour.txt", "a") as file:
                file.write(f"{phone_number}\n")
            print(f"Saved {phone_number} to ONE_Hour.txt.")
            break
        else:
            # Delete the XML file if no button was found
            os.remove('ui.xml')
            print("'OK' button not found, retrying...")

    if time.time() - start_time >= timeout:
        print(f"Timeout reached, 'OK' button not found for {phone_number}.")
        # Save the number to OTP_Sent.txt if OK button is not found
        with open("OTP_Sent.txt", "a") as file:
            file.write(f"{phone_number}\n")
        print(f"Saved {phone_number} to OTP_Sent.txt.")
        click_wrong_number_button(phone_number)

def capture_ui_dump():
    # Capture the UI dump using ADB
    run_adb_command('adb shell uiautomator dump /sdcard/window_dump.xml')
    run_adb_command('adb pull /sdcard/window_dump.xml .')
    print("UI dump captured and saved as window_dump.xml.")

def click_wrong_number_button(phone_number):
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

        # Check if the "Wrong number?" button is found by either text or content-desc
        if 'text="Wrong number?"' in ui_content or 'content-desc="Wrong number?"' in ui_content:
            print("'Wrong number?' button found.")
            # Extract coordinates of the button
            run_adb_command('adb shell input tap 894 544')  # Coordinates for 'Wrong number?' button
            print("Tapped 'Wrong number?' button.")
            break
        else:
            print("'Wrong number?' button not found, retrying...")

    if time.time() - start_time >= timeout:
        print("Timeout reached, 'Wrong number?' button not found.")

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Enter multiple phone numbers")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            phone_numbers = input("Enter phone numbers separated by commas: ").strip().split(',')

            open_whatsapp()
            click_agree_continue()

            for phone_number in phone_numbers:
                phone_number = phone_number.strip()  # Remove extra spaces
                enter_phone_number(phone_number)
                click_continue_or_yes()
                click_ok_button(phone_number)
            
            break
        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please select again.")

if __name__ == "__main__":
    main_menu()
