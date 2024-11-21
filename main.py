from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Desired capabilities for Appium
desired_caps = {
    "platformName": "Android",  # Change to "iOS" for iPhone
    "deviceName": "YourDeviceName",  # Replace with your device name
    "automationName": "UiAutomator2",  # Use "XCUITest" for iOS
    "appPackage": "com.whatsapp",  # WhatsApp package name
    "appActivity": "com.whatsapp.Main",  # WhatsApp main activity
    "noReset": True,  # Keeps the app in its current state
}

# Connect to Appium server
driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

try:
    # Wait until the login page loads
    wait = WebDriverWait(driver, 30)
    login_input = wait.until(EC.presence_of_element_located((By.ID, "com.whatsapp:id/registration_phone")))
    
    # Enter phone number
    phone_number = "1234567890"  # Replace with your phone number
    login_input.send_keys(phone_number)

    # Submit phone number (optional, uncomment if needed)
    # driver.find_element(By.ID, "com.whatsapp:id/next_button").click()

    print("Phone number entered successfully!")
finally:
    # Close the driver
    driver.quit()
