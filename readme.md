## About
An AI-powered bot that plays Subway Surfers automatically using computer vision and deep learning. The bot captures the game screen, processes the image through a trained CNN model, and executes keyboard actions in real-time.

## Process
lowkey just download requirements.txt and edit play_game.py if you dont wanna train your own model
#### Download requirements.txt
pip install -r requirements.txt
#### Collect Data using
```python
python collect_data2.py
```
Note: The bot captures a specific screen region. Adjust these coordinates in the scripts:
```python
monitor = {"top": 0, "left": 945, "width": 1000, "height": 1799}
```

- Arrow Keys: Capture screenshotfor   respective actions
- No input: Automatically captures"nothing" samples
- ESC: Stop collection

#### Open and run train.ipynb
- Just run through all the code. Its best to get AT LEAST 200 good samples for each label.
- Should have about 80% model acccuracy or else youre kinda cooked
- Edit the model architecture / hyperparameters if needed
- Make sure that each classes has about the same number of samples

#### Run the bot 
```python
python play_game.py
```
## Model Architecture
- Conv2D(64, 3x3) + ReLU + MaxPool2D(2x2)
- Conv2D(8, 3x3) + ReLU + MaxPool2D(2x2)  
- Flatten()
- Dense(64) + ReLU + Dropout(0.3)
- Dense(5) + Linear (output layer)

Labels: ["up", "down", "left", "right", "nothing"]


have fun yuhhhhhhhhhh
