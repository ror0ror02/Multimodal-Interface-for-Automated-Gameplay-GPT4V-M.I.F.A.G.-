
###########################################
#
# Screenshot bot
# Code from ror0ror02
# Translated from Russian by claude 3 haiku
#
# This script is designed to automate the process of a game called Garry's Mod. It uses a combination of screenshot capture, image analysis, and keyboard input simulation to navigate the game.
#
# The main functionality of the script is as follows:
#1. It takes a screenshot of the user at regular intervals.
#2: It sends a screenshot to the GPT-4 language model, which is trained to parse the game state and provide appropriate keyboard commands to advance.
#3: The script then interprets the model's response and simulates the appropriate keyboard inputs to control the game.
#
# The script uses several key components to achieve this functionality:
#
# 1. The take_screenshot() function takes a screenshot of the user's screen and encodes it in base64 format for ease of transmission.
# 2. The send_to_gpt4() function sends a Base64 encoded screenshot to the GPT-4 model and returns the model's response.
# 3. The parse_response() function extracts keyboard commands from the model response and returns them as a list of (key, duration) tuples.
# 4. The `press_key()` function simulates keyboard input by pressing and releasing a specified key for a specified amount of time.
# 5. The main() function asks the user for an OpenAI API key and screenshot interval, then enters a loop where it takes screenshots, sends them to the model, and executes the model's commands.
#
# The script also includes some additional features such as playing a sound when taking a screenshot and when receiving a response from the model.
#
# this script demonstrates how machine learning models such as GPT-4 can be used to automate complex tasks such as navigating a game environment
# by analyzing visual information and providing appropriate control inputs.
#
###########################################

import base64
import requests
import time
from PIL import ImageGrab
import keyboard
import winsound # delite if you on Linux

def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot.save("temp_screenshot.png")
    
    with open("temp_screenshot.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def send_to_gpt4(api_key, image_base64):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": f" You are playing Garry's Mod and will receive screenshots from the game. Your task is to analyze the game state and provide the appropriate keyboard command to progress. Respond using the format: [key] (W A S D SPACE (jump)) [time] (1-100), e.g., W 2. Do not include any additional text in your response.  The current objective is to 'Go to the exit, follow the directional arrows.'.  Tips:  Distances may appear larger than they are. Estimate distances and divide the time by 3. Use W for forward, A for left, S for backward, and D for right movement. If the target is not directly ahead, move left (A) or right (D) first, then forward (W). If you hit a wall, move backward (S). Follow any directional arrows in the screenshot (e.g., if an arrow points right, press D). Important:  Do not use response formats like 'w d 10'. Instead, specify the direction (A or D) and time first, then forward (W) if needed. Interpret all visual hints in the screenshots, such as directional arrows, and respond accordingly. Situations:  If you see an obstacle (wall, fence, object) directly in front of you:  Move left (A) or right (D) depending on the target's location, then forward (W). Example: A 2, W 3. If the target is straight ahead:  Move straight forward (W) for the distance to the target. Example: W 5. If you see a directional arrow in the screenshot:  Follow the indicated direction: W for forward, A for left, S for backward, D for right. Example: D 3. If you are stuck or unable to move forward:  Move backward (S), then try a different direction. Example: S 2, A 3, W 4. If the target is visible but far away:  Estimate the distance and divide the time by 3. Move forward (W) for the estimated time. Example: W 7. If there are multiple paths or directions to choose from:  Analyze the screenshot for visual clues (e.g., open doors, paths, arrows) and choose the most likely direction to reach the target. If you overshoot the target or move past it:  Move backward (S) for a short time, then reassess the situation and adjust your direction accordingly. Remember, your task is to 'Go to the exit, follow the directional arrows.!'. Good luck! If you see a person pointing his hand to the side, then go in that direction."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 100
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    delayed_print(f"│ {response.content}")
    return response.json()

# sound set
# delite if you on Linux
frequency = 200  # frequency in Hertz (e.g., A4)
duration_s = 50  # duration in milliseconds (50 milliseconds)

def delayed_print(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def press_key(key, duration):
    keyboard.press(key)
    winsound.Beep(frequency, duration_s) # delite if you on Linux
    time.sleep(duration)
    winsound.Beep(frequency, duration_s) # delite if you on Linux
    keyboard.release(key)
    winsound.Beep(frequency, duration_s) # delite if you on Linux

def parse_response(response_text):
    commands = []
    response_text = response_text.replace(",", "") 
    lines = response_text.strip().split('\n')
    for line in lines:
        parts = line.strip().split()
        i = 0
        while i < len(parts):
            if parts[i].upper() in ['W', 'A', 'S', 'D', 'SPACE']:
                key = parts[i].upper()
                try:
                    duration = float(parts[i + 1])
                    commands.append((key, duration))
                    i += 2
                except (IndexError, ValueError):
                    break
            else:
                i += 1
    if commands:
        return commands
    else:
        return None

def main():

    """
    The main function that prompts the user for the OpenAI API key and the screenshot interval,
    then enters a loop where it takes screenshots, sends them to the model, and executes the model's commands.
    """

    delayed_print("┌─────────────────────────────────────────────────────┐")
    delayed_print("│ Screenshot Bot │")
    delayed_print("├─────────────────────────────────────────────────────┤")
    
    api_key = input("│ Enter your OpenAI API key: ")
    while not api_key:
        delayed_print("│ API key cannot be empty!")
        api_key = input("│ Enter your OpenAI API key: ")
    
    interval = input("│ Enter the interval between screenshots (in seconds): ")
    while not interval.isdigit() or int(interval) <= 0:
        delayed_print("│ Interval must be a positive integer!")
        interval = input("│ Enter the interval between screenshots (in seconds): ")
    interval = int(interval)
    
    delayed_print("│ ┌───────────────────────────────────────────────────┐")
    delayed_print(f"│ │ Interval set: {interval} seconds")
    delayed_print(f"│ │ API key: {'*' * (len(api_key) - 4)}{api_key[-4:]}")
    delayed_print("│ │")
    delayed_print("│ │ Waiting for screenshots...")
    delayed_print("│ ├───────────────────────────────────────────────────┤")
    delayed_print("│ └───────────────────────────────────────────────────┘")
    
    while True:
        screenshot_base64 = take_screenshot()

        # sound set
        # delite if you on Linux
        frequency = 500
        duration_s = 100

        delayed_print("│ ┌───────────────────────────────────────────────────┐")
        delayed_print("│ │ Screenshot received!")
        delayed_print("│ │ Sending request to GPT-4...")
        delayed_print("│ ├───────────────────────────────────────────────────┤")
        winsound.Beep(frequency, duration_s) # delite if you on Linux
        
        response = send_to_gpt4(api_key, screenshot_base64)
        
        if 'choices' in response:
            winsound.Beep(frequency, duration_s) # delite if you on Linux
            delayed_print("│ │ Model response:")
            delayed_print("│ │")
            response_text = response['choices'][0]['message']['content']
            
            commands = parse_response(response_text)
            
            if commands:
                for key, duration in commands:
                    delayed_print(f"│ │ Pressing key: {key} for {duration} seconds")
                    press_key(key, duration)
            else:
                delayed_print("│ │ Invalid model response format")
                delayed_print("│ │ Model's thoughts:")
                delayed_print("│ │")
                for line in response_text.split('\n'):
                    delayed_print(f"│ │ {line}")
        else:
            delayed_print("│ │ Error analyzing the screenshot:")
            delayed_print("│ │")
            error_text = str(response)
            for line in error_text.split('\n'):
                delayed_print(f"│ │ {line}")
        delayed_print("│ └───────────────────────────────────────────────────┘")
        
        time.sleep(interval)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        delayed_print("└─────────────────────────────────────────────────────┘")
        delayed_print("Bot stopped.")



###########################################

# END SCRIPT
# PROGECT ON MIT license
# PUT A NAME ror0ror02 IF YOU WANT TO UPGRADE

###########################################
        

