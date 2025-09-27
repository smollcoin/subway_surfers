import pyautogui
from PIL import ImageGrab

screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor, 2880,1800
print(screenWidth, screenHeight)


bbox = (945, 0, 1945, 1799) 

# Take a screenshot of the specified region
a_screenshot = ImageGrab.grab(bbox=bbox)

# Save the screenshot
a_screenshot.save("./images/region_screenshot.png")
