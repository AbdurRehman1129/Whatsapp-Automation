from appium import webdriver
from time import sleep

# Desired capabilities
desired_caps = {
    "platformName": "Android",
    "deviceName": "1089137443002481",  # Your device ID
    "automationName": "UiAutomator2",  # Required automation framework
    "appPackage": "com.whatsapp",      # WhatsApp package name
    "appActivity": "com.whatsapp.Main",  # WhatsApp main activity
    "noReset": True,                   # Prevent app reset between sessions
}

try:
    # Connect to Appium server
    print("Connecting to Appium server...")
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    print("Connection successful! WhatsApp should now open on your device.")
    
    # Wait for WhatsApp to load
    sleep(5)
    
    # Example interaction (replace with your own logic)
    print("You can now automate interactions here.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Quit the driver only if it was initialized
    try:
        driver.quit()
        print("Driver session ended.")
    except NameError:
        print("Driver was not initialized, skipping quit.")
