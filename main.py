from appium import webdriver
import time

# Set up the desired capabilities for the Appium session
desired_caps = {
    'platformName': 'Android',
    'platformVersion': '13.5.0',  # Replace with your actual Android version
    'deviceName': 'Android Emulator',  # Replace with your device name or ID
    'appPackage': 'com.whatsapp',
    'appActivity': 'com.whatsapp.Main',
    'noReset': True
}

# Start an Appium session and connect to the device
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

def select_resend_sms_and_continue():
    # Wait for the screen to load (adjust the sleep time as needed)
    time.sleep(3)

    # Find and click the "Receive SMS" option
    receive_sms_option = driver.find_element_by_xpath("//android.widget.TextView[@text='Receive SMS']")
    receive_sms_option.click()  # This selects "Receive SMS"
    
    time.sleep(2)  # Wait for a moment for the option to be selected

    # Now find and click the "Continue" button
    continue_button = driver.find_element_by_id("com.whatsapp:id/continue_button")
    continue_button.click()

    print("Resend SMS option selected and Continue button clicked.")

# Execute the function
select_resend_sms_and_continue()

# Quit the Appium session
driver.quit()
