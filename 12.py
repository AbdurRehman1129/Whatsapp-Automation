import os
import re

def get_work_profile_id():
    try:
        # Execute the ADB command using os.popen
        output = os.popen('adb shell pm list users').read()
        
        # Search for the work profile in the output
        match = re.search(r'UserInfo\{(\d+):Work profile:\d+\}', output)
        
        if match:
            # Extract the work profile ID
            work_profile_id = match.group(1)
            return work_profile_id
        else:
            return "No work profile found"
    
    except Exception as e:
        return f"Error: {str(e)}"

# Get the work profile ID
work_profile_id = get_work_profile_id()
print(f"Work Profile ID: {work_profile_id}")
