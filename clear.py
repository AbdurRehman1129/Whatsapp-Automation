import os
import re

def detect_work_profile():
    try:
        # Check if ADB is installed and accessible
        adb_check = os.popen("adb version").read()
        if "Android Debug Bridge" not in adb_check:
            print("Error: ADB is not installed or not accessible.")
            return None

        # Execute the ADB command to list users
        output = os.popen("adb shell pm list users").read()

        # Search for the work profile in the output
        match = re.search(r'UserInfo\{(\d+):Work profile:\d+\}', output)
        if match:
            # Extract the work profile ID
            work_profile_id = match.group(1)
            print(f"Work profile detected with ID: {work_profile_id}")
            return work_profile_id
        else:
            print("No work profile found on the device.")
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def clear_whatsapp_business_data(work_profile_id):
    try:
        # Confirm clearing data
        response = input("Do you want to clear WhatsApp Business data in the work profile? (yes/no): ").strip().lower()
        if response == "yes":
            # Use the ADB command to clear WhatsApp Business data in the work profile
            command = f"adb shell pm clear --user {work_profile_id} com.whatsapp.w4b"
            result = os.popen(command).read()
            
            if "Success" in result:
                print("WhatsApp Business data cleared successfully.")
            else:
                print(f"Failed to clear WhatsApp Business data. Output: {result}")
        else:
            print("Operation canceled.")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    work_profile_id = detect_work_profile()
    if work_profile_id:
        clear_whatsapp_business_data(work_profile_id)

if __name__ == "__main__":
    main()
