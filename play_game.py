import mss
import numpy as np
import cv2
import pyautogui
import time

from tensorflow import keras
import tensorflow as tf 

# load model
model = keras.models.load_model('model/model_1.keras')

# labels
classes = ["up", "down", "left", "right", "nothing"]

def capture_game():
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 945, "width": 1000, "height": 1799}

        screenshot = sct.grab(monitor)
        
        img = np.array(screenshot) # turn to array
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert format
        return img
    
def preprocessing(image):
    # resize an image
    resized = cv2.resize(image,(96,96))
    
    # normalize the values back
    normalized = resized / 255.0
    
    # apparently need to return the batch size since tf wants (bs, height, width, channels)
    batch = np.expand_dims(normalized, axis =0)
    
    return batch
            

def predict_action(model, image, threshold=0.75):
    # Preprocess image
    processed_img = preprocessing(image)
    
    # prediction
    prediction = model.predict(processed_img, verbose=0)
    
    # Convert logits to probabilities if needed
    if prediction.max() > 1:
        probabilities = tf.nn.softmax(prediction[0])
    else:
        probabilities = prediction[0]
    
    max_confidence = np.max(probabilities)
    predicted_class_idx = np.argmax(probabilities)
    predicted_action = classes[predicted_class_idx]
    
    # threshold
    if max_confidence >= threshold:
        return predicted_action, max_confidence
    else:
        return 'nothing', max_confidence

def execute_action(action, prev_action):
    if action == 'up' and prev_action != 'up':
        pyautogui.press('up') 
    
    elif action == 'down' and prev_action != 'down':
        pyautogui.press('down')   
    elif action == 'left' and prev_action != 'left':
        pyautogui.press('left')   
    elif action == 'right' and prev_action != 'right':
        pyautogui.press('right')  
    # Do nothing if no have
    return action

def play_game():
    # main
    print("Starting")
    time.sleep(3)
    
    frame_count = 0
    start_time = time.time()
    previous_action = 'nothing'
    try:
        while True:
            # screenie
            screenshot = capture_game()
            
            # prediction
            action, confidence = predict_action(model, screenshot, threshold=0.85 )
            # action
            execute_action(action, previous_action)
            
            previous_action = action
        
            frame_count += 1
            if frame_count % 5 == 0:
                fps = frame_count / (time.time() - start_time)
                print(f"Action: {action:>0.85} | Confidence: {confidence:.3f} | FPS: {fps:.1f}")
            
        
            time.sleep(0.05) 
            
    except KeyboardInterrupt:
        print("Game stopped")

if __name__ == "__main__":
    play_game()
