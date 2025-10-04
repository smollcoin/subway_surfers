import mss
import numpy as np
import cv2
import pyautogui
import time

from tensorflow import keras
import tensorflow as tf 

# refactored
class game:
    def __init__(self):
        self.model = keras.models.load_model('model/model_9.keras')
        self.classes = ["up", "down", "left", "right", "nothing"]
        self.monitor = {"top": 0, "left": 945, "width": 1000, "height": 1799}
        self.prev_action = 'nothing'
        self.image_size = (96,96)
        

    def capture_game(self):
        with mss.mss() as sct:
            screenshot = sct.grab(self.monitor)
            
            img = np.array(screenshot) # turn to array
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) # remove alpha channel
            return img
    
    def preprocess(self, image):
        resized = cv2.resize(image, self.image_size)
        img_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        normalized = img_rgb / 255.0
        batch = np.expand_dims(normalized, axis=0) # need to return batch since model expects 4D tensor
        
        return batch
    
    def predict_action(self, image, threshold=0.75):
        # Preprocess image
        processed_img = self.preprocess(image)
        
        # prediction
        prediction = self.model.predict(processed_img, verbose=0)
        
        # Convert logits to probabilities if needed
        if prediction.max() > 1:
            probabilities = tf.nn.softmax(prediction[0])
        else:
            probabilities = prediction[0]
        
        max_confidence = np.max(probabilities)
        predicted_class_idx = np.argmax(probabilities)
        predicted_action = self.classes[predicted_class_idx]
        
        # threshold
        if max_confidence >= threshold:
            return predicted_action, max_confidence
        else:
            return 'nothing', max_confidence
    
    def execute_action(self, action):
        if action == 'up' and self.prev_action != 'up':
            pyautogui.press('up') 
        
        elif action == 'down' and self.prev_action != 'down':
            pyautogui.press('down')   
        elif action == 'left' and self.prev_action != 'left':
            pyautogui.press('left')   
        elif action == 'right' and self.prev_action != 'right':
            pyautogui.press('right')  
        # Do nothing if no have
        return action


def main(game=game):
    
    game = game()
    frame_count = 0
    start_time = time.time()

    
    try:
        while True:
            screenshot = game.capture_game()
            
            action, confidence = game.predict_action(screenshot, threshold=0.6)
            
            # Debug: Print what action is being executed
            if action != 'nothing':
                print(f"Executing: {action} (confidence: {confidence:.3f})")
            
            action = game.execute_action(action)
            game.prev_action = action
            
            frame_count += 1
            if frame_count % 10 == 0:
                fps = frame_count / (time.time() - start_time)
                print(f"Action: {action:>7} | Confidence: {confidence:.3f} | FPS: {fps:.1f}")
            
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("Game stopped")
        
if __name__ == "__main__":
    main(game)
