import keyboard
import time 
import os
import pyautogui
from PIL import ImageGrab


keys = ["left", "right", "up", "down", "space", "esc"]

def read_keypress():
    # Non-blocking check for each key
    for key in keys:
        if keyboard.is_pressed(key):
            return key
    return None  # No key pressed

def take_screenshot():
    bbox = (945, 0, 1945, 1799)
    a_screenshot = ImageGrab.grab(bbox=bbox)
    return a_screenshot

def save_screenshot(key_pressed, a_screenshot):

    folder_path = os.path.join("images", key_pressed)
    
    timestamp = str(int(time.time() * 1000))  # milliseconds for uniqueness
    filename = f"{timestamp}_{key_pressed}.png"
    file_path = os.path.join(folder_path, filename)
    
    # Save the screenshot
    a_screenshot.save(file_path)
    print(f"Screenshot saved to: {file_path}")
    
def detect_game_running(a_screenshot):
    # x pos 218
    x = 218
    # y pos 79
    y = 79
    
    pixel_color = a_screenshot.getpixel((218,79))
    print(pixel_color)
    expected_color = (219,79,236)
    for i in range(3):  # rgb
        if abs(pixel_color[i] - expected_color[i]) > 30:
            print("Waiting for game to start")
            return False
    return True

loop = True
print("starting in 5 seconds")
time.sleep(5)
while loop:
    start_time = time.time()
    key_detected = False
    detected_key = None
    
    # Check for keypresses first (faster)
    while time.time() - start_time < 0.7:  # Reduced detection window
        keypress = read_keypress()
        
        if keypress == "esc":
            print("Exiting...")
            loop = False
            key_detected = True
            break
        elif keypress in keys:
            detected_key = keypress
            key_detected = True
            
            # Take screenshot 
            a_screenshot = take_screenshot()
            
            # Quick game check
            if detect_game_running(a_screenshot):
                save_screenshot(keypress, a_screenshot)
            
            time.sleep(0.1)  # Reduced delay
            break
            
        time.sleep(0.005)  # Faster polling
    
    # nothing
    if not key_detected:
        a_screenshot = take_screenshot()
        if detect_game_running(a_screenshot):
            save_screenshot("nothing", a_screenshot)
            print("Nothing")

