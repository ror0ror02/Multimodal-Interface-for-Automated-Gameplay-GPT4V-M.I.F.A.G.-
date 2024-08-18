
###########################################
#
# Screenshot bot MIFAG
# Code from ror0ror02
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

from pynput.mouse import Button, Controller
import base64
import requests
import time
from PIL import ImageGrab
import keyboard
import winsound  # delite if you on Linux

Max_request = 300 # ========== request_count here ==========

def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot.save("temp_screenshot.png")
    
    with open("temp_screenshot.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def send_to_gpt4(api_key, base64_image, task, previous_actions, request_count):
    if request_count >= Max_request:
        print("End Work.")
        return None, request_count

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    system_content = '''system_content = "You are playing Garry's Mod and will receive screenshots from the game. Your task is to analyze the game state and provide the appropriate keyboard command to progress. Respond using the format: (key) (W A S D SPACE 1 2 3 4 5 6 7 8 9 E LEFT_TURN RIGHT_TURN Ctrl F1 MOUSE_UP MOUSE_DOWN Enter Y) (time) (1-6), : (comment) e.g., W 2 F 1 (You can write up to 10 actions per request.) : (Your thoughts may be here) (: has been added to the response foreground)  Do not include any additional text in your response. Considerable time can pass between screenshots, be ready for changes in the game and adapt."

"At the end of each response, after the main actions, create a simplified map of the current environment using the following symbols:
. - free space
| - wall
P - player
! - monster or danger
E - goal

Example map:

.........
...!.|...
..P..E..
.....|...
.........

please add markdown to end and start map.

AND THE CARD IS MANDATORY AFTER : THIS MUST ALWAYS BE A CARD!!!

The map should reflect the current position of the player, the location of walls, free space, and dangers based on the analysis of the screenshot. The size of the map may vary depending on the visible area in the screenshot. Update the map with each new screenshot to track the player's progress and surroundings.'''
    
    user_content = [
        {
            "type": "text",
            "text": f"The current objective is to '{task}'. This {request_count} request for you. Max request = {Max_request}, and you has stopped. Action can be used: 'W' 'A' 'S' 'D' 'SPACE' '1' '2' '3' '4' '5' '6' '7' '8' '9' 'E' 'RMB' 'LMB' 'F' 'LEFT_TURN' 'RIGHT_TURN' 'Ctrl' 'F1' 'MOUSE_UP' 'MOUSE_DOWN 'Enter' 'Y'"
        },
        {
            "type": "text",
            "text": "Tips: Distances may appear larger than they are. (max time - 6 sec.) Use W for forward, A for left, S for backward, and D for right movement. If the target is not directly ahead, move left (A) or right (D) first, then forward (W). If you hit a wall, move backward (S). Follow any directional arrows in the screenshot (e.g., if an arrow points right, press D). Interpret all visual hints in the screenshots, such as directional arrows, and respond accordingly. If you notice that you are at a dead end, you can post messages about it in thoughts, For example, after the main thoughts you can write your status, be careful not to repeat the same actions, especially if you are at a dead end, and vice versa, if you shoot at someone or move without obvious signs of a dead end. Be careful to apply these actions after 3 unsuccessful attempts to escape. An example of movements from which you can throw yourself away from a dead end on 1 attempt: LEFT_TURN 15 W 2."
        },
        {
            "type": "text",
            "text": "Situations: If you see an obstacle (wall, fence, object) directly in front of you: Move left (A) or right (D) depending on the target's location, then forward (W). Example: A 2, W 3. If the target is straight ahead: Move straight forward (W) for the distance to the target. Example: W 5. If you see a directional arrow in the screenshot: Follow the indicated direction: W for forward, A for left, S for backward, D for right. Example: D 3. If you are stuck or unable to move forward: Move backward (S), then try a different direction. Example: S 2, A 3, W 4. If the target is visible but far away: Estimate the distance and divide the time by 3. Move forward (W) for the estimated time. Example: W 7. If there are multiple paths or directions to choose from: Analyze the screenshot for visual clues (e.g., open doors, paths, arrows) and choose the most likely direction to reach the target. If you overwalk and Shoot! the target or move past it: Move backward (S) for a short time, then reassess the situation and adjust your direction accordingly. If you see an enemy (it's either a combine or a zombie), then shoot immediately. You can specify the duration of shooting if it is an assault rifle (example LMB (2-30) (example with a pistol or RPG LMB 1) If you see a first aid kit on the wall, depending on your health, go to it and press E (Healing time depends on your health in the lower left corner, if it is small, then hold the E button more. For explame, you health - 4 and you press E for 9 sec). Also, if you see a dark place, you can turn on the flashlight to F (time). But check, maybe it’s already turned on. Don't write like this: F1 1 : [Closing the spawn menu], W 6 LMB 1 : [Approaching the monster and preparing to fire the RPG] Write like this: F1 1, W 6 LMB 1 : [Closing the spawn menu, Approaching the monster and preparing to fire the RPG] (This explame!) You can also choose a weapon by creating a sequence of actions in numbers. Example: 5 1 5 1 LMB 1 [comment, you can write what you learned] This command gives you an RPG. (I repeat, not 5 1 LMB 1, but 5 1 5 1 LMB 1) You can also turn up and down using the commands 'MOUSE_UP', 'MOUSE_DOWN'. PLEASE DONT DEATH AND WALK TO WATER! (Except for the tasks) Press SPACE to respawn on the entire translucent red screen. If you fall into the water or get lost, look for land or landmarks and move towards them. You can pop up by pressing the SPACE key and take other actions."
        },
        {
            "type": "text",
            "text": f"Remember, your task is to '{task}'. Good luck! If you see a person pointing his hand to the side, then go in that direction. Use the number keys (1-9) for interacting with objects or performing specific actions as needed. Use the 'E' key to interact with objects or open doors when in close proximity. Use 'RMB' for right mouse button click and 'LMB' for left mouse button click when needed to interact with objects or perform specific actions. (For example, LMB (time) to Shoot! You can also execute more commands at once, for example W 5 A 6 S 2. F - flashlight. Commands LEFT_TURN and RIGHT_TURN They give you the opportunity to change. They work in the same way as all commands, only unlike them - here the seconds indicate the position. 1 second – 50 positions, Example: RIGHT_TURN 4 This command turns you 200 right positions in Garrys Mod. Use F1 to open spawn menu, and LMB for selection in spawn menu, and LEFT_TURN RIGHT_TURN MOUSE_UP MOUSE_DOWN to move the mouse. You can press the Y button and write something in the chat. For example Y 1 Y 1 A 1 Y 1 Enter 1 (write in chat)"
        },
        {
            "type": "text",
            "text": f"Previous actions: {', '.join(previous_actions[-10:])}"
        },
    {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]

    

    payload = {
        "model": "chatgpt-4o-latest", # Model here
        "messages": [
            {
                "role": "system",
                "content": system_content
            },
            {
                "role": "user",
                "content": user_content
            }
        ],
        "max_tokens": 600
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    delayed_print(f"│ {response.content}")
    request_count += 1
    
    # Запись действий GPT-4 в файл
    with open("MIFAG_actions.txt", "a") as file:
        file.write(f"Request {request_count}:\n")
        file.write(f"Task: {task}\n")
        file.write(f"GPT-4 response: {response}")
    
    return response.json(), request_count

# sound set
# delite if you on Linux
frequency = 200  # frequency in Hertz (e.g., A4)
duration_s = 50  # duration in milliseconds (50 milliseconds)

def delayed_print(text, delay=0.0): # 0.0 for max speed
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def press_key(key, duration):
    if key == 'ENTER':
        keyboard.press('enter')
        winsound.Beep(frequency, duration_s)  # delite if you on Linux
        time.sleep(duration)
        winsound.Beep(frequency, duration_s)  # delite if you on Linux
        keyboard.release('enter')
        winsound.Beep(frequency, duration_s)  # delite if you on Linux
    else:
        keyboard.press(key)
        winsound.Beep(frequency, duration_s)  # delite if you on Linux
        time.sleep(duration)
        winsound.Beep(frequency, duration_s)  # delite if you on Linux
        keyboard.release(key)
        winsound.Beep(frequency, duration_s)  # delite if you on Linux

def parse_response(response_text):
    commands = []
    lines = response_text.strip().split('\n')
    for line in lines:
        parts = line.strip().split(':')
        if len(parts) == 2:
            command_text, comment = parts
            command_parts = command_text.strip().split(',')
            for command in command_parts:
                command = command.strip()
                if ' ' in command:
                    command_split = command.split(' ')
                    key = command_split[0]
                    duration = command_split[1]
                    if key.upper() in ['W', 'A', 'S', 'D', 'SPACE', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'E', 'RMB', 'LMB', 'F', 'LEFT_TURN', 'RIGHT_TURN', 'CTRL', 'F1', 'MOUSE_UP', 'MOUSE_DOWN', 'Y', 'ENTER']:
                        try:
                            duration = float(duration)
                            commands.append((key.upper(), duration, comment.strip()))
                        except ValueError:
                            pass
    return commands

def press_key(key, duration, comment):
    # print(f">> {comment}")
    mouse = Controller()
    if key == 'RMB':
        mouse.press(Button.right)
        mouse.release(Button.right)
    elif key == 'LMB':
        mouse.press(Button.left)
        mouse.release(Button.left)
    elif key == 'LEFT_TURN':
        positions_per_second = 50  # Adjust the value as needed for the desired turn speed
        positions_to_move = int(duration * positions_per_second)
        mouse.move(-positions_to_move, 0)
    elif key == 'RIGHT_TURN':
        positions_per_second = 50  # Adjust the value as needed for the desired turn speed
        positions_to_move = int(duration * positions_per_second)
        mouse.move(positions_to_move, 0)
    elif key == 'MOUSE_UP':
        positions_per_second = 50  # Adjust the value as needed for the desired movement speed
        positions_to_move = int(duration * positions_per_second)
        mouse.move(0, -positions_to_move)
    elif key == 'MOUSE_DOWN':
        positions_per_second = 50  # Adjust the value as needed for the desired movement speed
        positions_to_move = int(duration * positions_per_second)
        mouse.move(0, positions_to_move)
    else:
        if key == 'ENTER':
            keyboard.press('enter')
        else:
            keyboard.press(key)
        time.sleep(duration)
        if key == 'ENTER':
            keyboard.release('enter')
        else:
            keyboard.release(key)
    winsound.Beep(frequency, duration_s)
    winsound.Beep(frequency, duration_s)


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
    
    task = input("│ Enter the task for the model: ")
    
    delayed_print("│ ┌───────────────────────────────────────────────────┐")
    delayed_print(f"│ │ Interval set: {interval} seconds")
    delayed_print(f"│ │ API key: {'*' * (len(api_key) - 4)}{api_key[-4:]}")
    delayed_print(f"│ │ Task: {task}")
    delayed_print("│ │")
    delayed_print("│ │ Waiting for screenshots...")
    delayed_print("│ ├───────────────────────────────────────────────────┤")
    delayed_print("│ └───────────────────────────────────────────────────┘")
    
    previous_actions = []
    request_count = 0
    
    while True:
        screenshot_base64 = take_screenshot()

        delayed_print("│ ┌───────────────────────────────────────────────────┐")
        delayed_print("│ │ Screenshot received!")
        delayed_print("│ │ Sending request to GPT-4...")
        delayed_print("│ ├───────────────────────────────────────────────────┤")
        
        response, request_count = send_to_gpt4(api_key, screenshot_base64, task, previous_actions, request_count)

        # sound set
        # delete if you are on Linux
        frequency = 500
        duration_s = 100

        
        if 'choices' in response:
            winsound.Beep(frequency, duration_s) # delete if you are on Linux
            delayed_print("│ │ Model response:")
            delayed_print("│ │")
            response_text = response['choices'][0]['message']['content']
            
            commands = parse_response(response_text)
            
            if commands:
                for command in commands:
                    key, duration, comment = command
                    delayed_print(f"│ │ {comment}")
                    delayed_print(f"│ │ Pressing key: {key} for {duration} seconds")
                    press_key(key, duration, comment)
                    previous_actions.append(f"{key} {duration} : {comment}")
                    
                # Extract and print the map
                map_start = response_text.find("```")
                map_end = response_text.find("```", map_start + 1)
                if map_start != -1 and map_end != -1:
                    map_text = response_text[map_start + 3:map_end].strip()
                    delayed_print("│ │")
                    delayed_print("│ │ Environment Map:")
                    for line in map_text.split('\n'):
                        delayed_print(f"│ │ {line}")
                    
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
        
        if request_count == 0:
            time.sleep(1)

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
