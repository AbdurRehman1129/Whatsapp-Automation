import time

def select_resend_sms_and_continue():
    # Find and click the "Receive SMS" option
    receive_sms_option = device.find_element_by_xpath("//android.widget.TextView[@text='Receive SMS']")
    receive_sms_option.click()  # This selects "Receive SMS"
    
    time.sleep(2)  # Wait for a moment for the option to be selected

    # Now find and click the "Continue" button
    continue_button = device.find_element_by_id("com.whatsapp:id/continue_button")
    continue_button.click()

    print("Resend SMS option selected and Continue button clicked.")

# Execute the function
select_resend_sms_and_continue()
