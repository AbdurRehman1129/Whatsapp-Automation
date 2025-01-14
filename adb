adb -s 127.0.0.1:21503 shell uiautomator dump /sdcard/window_dump.xml
adb -s 127.0.0.1:21503 pull /sdcard/window_dump.xml .
