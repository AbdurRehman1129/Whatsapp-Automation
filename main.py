import time
import os

# Function to check and click the "OK" button if the one-hour waiting page is shown
def click_ok_if_waiting():
    # Check for the "We couldn't send an SMS" text
    if exists(resourceId="android:id/message", text="We couldn't send an SMS to your number"):
        # Wait for the OK button to appear
        wait_for_element(resourceId="android:id/button1", timeout=5)
        click(resourceId="android:id/button1")
        return True
    return False

# Function to click the "Wrong number?" button
def click_wrong_number():
    # Wait for "Wrong number?" button to appear and click it
    wait_for_element(resourceId="com.whatsapp:id/send_code_description", text="Wrong number?", timeout=5)
    click(resourceId="com.whatsapp:id/send_code_description")

# Function to enter the number and proceed
def enter_number_and_proceed(number):
    # Enter the phone number in the input field
    send_keys(resourceId="com.whatsapp:id/phone_number_input", text=number)
    time.sleep(1)
    
    # Click the Next button
    click(resourceId="com.whatsapp:id/next_button")
    
    # Handle the waiting page if it appears
    if click_ok_if_waiting():
        # Log the number that needs to wait for OTP
        with open("OTP_sent.txt", "a") as f:
            f.write(f"{number}\n")

# Main loop for handling multiple numbers
def process_numbers(numbers):
    for number in numbers:
        print(f"Processing number: {number}")
        
        # Enter the number and proceed
        enter_number_and_proceed(number)
        
        # Click the wrong number button to continue the process
        click_wrong_number()
        
        # Prompt to continue with the next number
        input("Press Enter to send the next number...")

# Example usage
if __name__ == "__main__":
    # List of numbers to process
    numbers = ["+994409632322", "+994409632323"]
    
    process_numbers(numbers)
