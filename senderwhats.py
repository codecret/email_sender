import pywhatkit as kit
import time
import pyautogui

phone_number = "+90"  # No spaces in the phone number
message = "message"

# Send the first message and wait for WhatsApp Web to open
kit.sendwhatmsg_instantly(phone_number, f"{message} 1")
time.sleep(10)  

# Send the rest of the messages
for i in range(4, 101):
    pyautogui.write(f"{message} {i}")
    pyautogui.press("enter")
    time.sleep(1) 