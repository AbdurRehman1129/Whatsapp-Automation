from appium import webdriver
from time import sleep

# Desired capabilities
desired_caps = {
    "platformName": "Android",
    "deviceName": "1089137443002481",  # Use your device ID here
    "automationName": "UiAutomator2",
    "appPackage": "com.whatsapp",
    "appActivity": "com.whatsapp.Main",
    "noReset": True,
}

# Create a WebDriver instance and connect to Appium server
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

# Wait for WhatsApp to open
sleep(5)

# Example of interacting with WhatsApp (if you want to automate entering a number)
# You can change this part to suit your automation, e.g., entering a phone number, sending a message, etc.

# Wait for the WhatsApp UI to load and find the phone number field (you may need to adjust the locator)
# Example: Enter a phone number (change locator as needed)
try:
    phone_number_field = driver.find_element_by_id("com.whatsapp:id/registration_phone")  # Adjust this ID as necessary
    phone_number_field.send_keys("1234567890")  # Replace with the phone number you want to enter
    print("Phone number entered successfully!")
except Exception as e:
    print(f"Error: {e}")

# Wait for a while to see the result
sleep(10)

# Quit the driver (close the app and stop the session)
driver.quit()
