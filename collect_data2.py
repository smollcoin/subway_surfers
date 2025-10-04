# revised version of data collection 
# uses mss instead of pyautogui for streaming screenshots + faster

import keyboard
import time 
import os
import mss
import numpy as np
from PIL import Image
import cv2

keys = ["left", "right", "up", "down", "space", "esc"]

sct = mss.mss()
monitor = {"top": 0, "left": 945, "width": 1000, "height": 1799} 

def read_keypress():
    # Non-blocking 
    for key in keys:
        if keyboard.is_pressed(key):
            return key
    return None  # No key pressed

def take_screenshot():
    screenshot = sct.grab(monitor)
    
    img_array = np.array(screenshot)
    # convert to RGB
    img_rgb = img_array[:, :, :3]  # drop alpha channel 
    img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)  # c BGR to RGB
    
    # convert back to PIL Image
    pil_image = Image.fromarray(img_rgb)
    
    return pil_image

def save_screenshot(key_pressed, a_screenshot):
    folder_path = os.path.join("images", f"{key_pressed}_1")
    os.makedirs(folder_path, exist_ok=True) 
    
    timestamp = str(int(time.time() * 1000))  
    filename = f"{timestamp}_{key_pressed}.png"
    file_path = os.path.join(folder_path, filename)
    
    a_screenshot.save(file_path)
    print(f"screenshot saved to: {file_path}_1")

def detect_game_running(screenshot):
    """Simple check if game is running"""
    try:
        img_array = np.array(screenshot)
        mean_brightness = np.mean(img_array)
        return mean_brightness > 50 
    except:
        return True

loop = True
print("Starting data collection in 5 seconds")
time.sleep(4)

try:
    while loop:
        start_time = time.time()
        key_detected = False
        detected_key = None
        
        # check keypress
        while time.time() - start_time < 0.5: 
            keypress = read_keypress()
            
            if keypress == "esc":
                print("Exiting...")
                loop = False
                key_detected = True
                break
            elif keypress in keys:
                detected_key = keypress
                key_detected = True
                
                # take screenshot
                a_screenshot = take_screenshot()
                
                # check if game is running and save
                if detect_game_running(a_screenshot):
                    save_screenshot(keypress, a_screenshot)
                
                time.sleep(0.1)  
                break
                
            time.sleep(0.005) 
        
        # Save nothing pics
        if not key_detected:
            a_screenshot = take_screenshot()
            if detect_game_running(a_screenshot):
                save_screenshot("nothing", a_screenshot)
                

finally:
    sct.close()
    print("finished")
