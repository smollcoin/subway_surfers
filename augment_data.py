import cv2
import numpy as np
import os

def flip_image(folder_name, store_name, left_right):
    axis =0
    if left_right == True: # flip horizontally
        axis = 1
        
    folder_path = os.path.join("images", folder_name)
    store_path = os.path.join("images", store_name)  
    os.makedirs(store_path, exist_ok=True) #create in images folder
    
    counter = 0
    for file in os.listdir(folder_path):
        img_path = os.path.join(folder_path, file)
        img = cv2.imread(img_path)
        
        if img is not None: 
            flipped_img = cv2.flip(img, axis)  
            
            # Save
            flipped_filename = f"flipped_{file}"
            flipped_path = os.path.join(store_path, flipped_filename)
            cv2.imwrite(flipped_path, flipped_img)
            counter += 1
    
    print(f"Flipped {counter} images from {folder_name} to {store_name}")

flip_image("down", "flip_down",False)
flip_image("up", "flip_up", False)

flip_image("left", "flip_left",True)
flip_image("up", "flip_right", True)
