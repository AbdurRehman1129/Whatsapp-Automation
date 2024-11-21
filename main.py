from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Desired capabilities
desired_caps = {
    "platformName": "Android",
    "deviceName": "Android Emulator",  # Replace with your device name
    "automationName": "UiAutomator2",
    "appPackage": "com.whatsapp",
    "appActivity": "com.whatsapp.Main",
    "noReset": True,
}

# Connect to Appium server
driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

try:
    # Wait for the phone number input field
    wait = WebDriverWait(driver, 30)
    phone_input = wait.until(EC.presence_of_element_located((By.ID, "com.whatsapp:id/registration_phone")))

    # Enter phone number
    phone_number = "1234567890"  # Replace with the phone number
    phone_input.send_keys(phone_number)

    print("Phone number entered successfully!")
finally:
    # Quit the driver
    driver.quit()
