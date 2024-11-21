from appium import webdriver
from time import sleep

# Desired capabilities
desired_caps = {
    "platformName": "Android",
    "deviceName": "1089137443002481",  # Your device ID
    "automationName": "UiAutomator2",  # Ensure this is set correctly
    "appPackage": "com.whatsapp",      # WhatsApp package name
    "appActivity": "com.whatsapp.Main", # WhatsApp main activity
    "noReset": True,                   # Prevent app reset between sessions
}

try:
    # Connect to Appium server
    driver = webdriver.Remote('http://127.0.0.1:4723', desired_caps)

    # Wait for WhatsApp to load
    sleep(5)

    print("WhatsApp opened successfully!")
    
    # Add interactions or automation code here
    
    # Wait and observe before quitting
    sleep(10)
finally:
    # Quit the driver
    driver.quit()
