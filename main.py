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

    # Check if the "Continue" button is present (you can adjust the resource ID or text as needed)
    continue_button_exists = os.system('adb shell uiautomator dump /sdcard/ui.xml && adb pull /sdcard/ui.xml && grep "CONTINUE" ui.xml')

    if continue_button_exists == 0:  # Check if "CONTINUE" was found
        # Tap the "Continue" button
        os.system('adb shell input tap 540 2220')  # Adjust coordinates if necessary
        print("Tapped 'Continue'.")
    else:
        # Tap the "Yes" button (you can adjust the coordinates if necessary)
        os.system('adb shell input tap 540 1950')  # Adjust coordinates for "Yes"
        print("Tapped 'Yes'.")

if __name__ == "__main__":
    open_whatsapp()
    click_agree_continue()
    enter_phone_number()
    click_continue_or_yes()
