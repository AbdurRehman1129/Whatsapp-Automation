from appium import webdriver
from time import sleep

# Desired capabilities
desired_caps = {
    "platformName": "Android",           # OS platform
    "deviceName": "1089137443002481",    # Your device ID
    "automationName": "UiAutomator2",    # Required automation framework
    "appPackage": "com.whatsapp",        # WhatsApp app package
    "appActivity": "com.whatsapp.Main",  # WhatsApp main activity
    "noReset": True,                     # Prevent resetting the app
    "newCommandTimeout": 300             # Timeout to keep the session alive
}

try:
    print("Connecting to Appium server...")
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    print("Connection successful! WhatsApp should now open on your device.")

    # Wait for WhatsApp to load
    sleep(5)

    # Add interactions here, if necessary
    print("Ready for interaction with WhatsApp.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Quit the driver only if it was initialized
    try:
        driver.quit()
        print("Driver session ended.")
    except NameError:
        print("Driver was not initialized, skipping quit.")
