import os

def open_whatsapp():
    # Launch WhatsApp
    os.system("adb shell monkey -p com.whatsapp -c android.intent.category.LAUNCHER 1")
    print("WhatsApp opened.")

def click_agree_continue():
    # Wait for WhatsApp to load and the EULA page to appear
    os.system("adb shell sleep 3")

    # Tap the "Agree and Continue" button (replace with the correct resource ID)
    resource_id_agree_button = "com.whatsapp:id/eula_accept"
    os.system(f'adb shell input tap 540 2318')  # Tap coordinates: near the center of the button
    print("Tapped 'Agree and Continue'.")

if __name__ == "__main__":
    open_whatsapp()
    click_agree_continue()
