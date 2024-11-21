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
    # Wait a few seconds to let the screen load
    time.sleep(3)

    # Dump the UI XML file
    os.system('adb shell uiautomator dump /sdcard/ui.xml')
    os.system('adb pull /sdcard/ui.xml')

    # Open the XML file and search for the "CONTINUE" or "YES" text
    with open('ui.xml', 'r', encoding='utf-8') as f:
        ui_content = f.read()

    # Check if "CONTINUE" button exists in the UI XML
    if 'CONTINUE' in ui_content:
        # Tap the "Continue" button (adjust coordinates if necessary)
        os.system('adb shell input tap 540 2220')  # Adjust coordinates for "Continue"
        print("Tapped 'Continue'.")
    elif 'YES' in ui_content:
        # Tap the "Yes" button (adjust coordinates if necessary)
        os.system('adb shell input tap 540 1950')  # Adjust coordinates for "Yes"
        print("Tapped 'Yes'.")
    else:
        print("Neither 'Continue' nor 'Yes' button was found.")

if __name__ == "__main__":
    open_whatsapp()
    click_agree_continue()
    enter_phone_number()
    click_continue_or_yes()
