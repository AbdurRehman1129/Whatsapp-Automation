import os
import time

def check_and_click_ok():
    # Check if "OK" button exists for one-hour wait message
    os.system("adb shell uiautomator dump /sdcard/ui.xml")
    os.system("adb pull /sdcard/ui.xml ./ui.xml")
    
    with open("ui.xml", "r") as file:
        xml_content = file.read()
        
        if 'resource-id="android:id/button1"' in xml_content and 'text="OK"' in xml_content:  # Check for "OK" button
            print("Found 'OK' button, clicking it...")
            os.system('adb shell input tap 817 1410')  # Coordinates for "OK" button (Adjust if needed)
            return True
        elif 'We couldn\'t send an SMS to your number.' in xml_content:  # If 1-hour message appears
            print("OTP send failed, saving number to OTP_sent.txt")
            return False
    return False

def click_wrong_number():
    # Check and click the "Wrong Number" button
    os.system("adb shell uiautomator dump /sdcard/ui.xml")
    os.system("adb pull /sdcard/ui.xml ./ui.xml")
    
    with open("ui.xml", "r") as file:
        xml_content = file.read()
        
        if 'text="Wrong number?"' in xml_content:  # Check for "Wrong number?" text
            print("Found 'Wrong Number' button, clicking it...")
            os.system('adb shell input tap 540 1950')  # Adjust coordinates for "Wrong Number" button
            return True
    return False

def write_number_to_file(phone_number):
    # Write the number to OTP_sent.txt
    with open("OTP_sent.txt", "a") as file:
        file.write(f"{phone_number}\n")
    print(f"Number {phone_number} saved to OTP_sent.txt.")

def enter_phone_number():
    phone_number = input("Please enter the phone number: ")
    
    # Wait for the phone number page to appear
    os.system("adb shell sleep 3")
    
    # Enter the phone number
    os.system(f'adb shell input text "{phone_number}"')
    print(f"Entered phone number: {phone_number}")
    
    # Tap the "Next" button using coordinates (adjust if necessary)
    os.system('adb shell input tap 540 1585')  # Adjust coordinates for "Next"
    print("Tapped 'Next'.")
    return phone_number

def process_number():
    phone_number = enter_phone_number()

    # Check if the OTP is sent (i.e., one hour has passed)
    if check_and_click_ok():
        write_number_to_file(phone_number)
        click_wrong_number()
        return True
    return False

def main():
    while True:
        if not process_number():
            print("Failed to process the number. Please try again.")
            continue
        
        # Ask the user if they want to send another number
        repeat = input("Do you want to enter another number? (yes/no): ").strip().lower()
        if repeat != "yes":
            break
    print("Process completed.")

if __name__ == "__main__":
    main()
