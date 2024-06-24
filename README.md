# Multimodal Interface for Automated Gameplay (M.I.F.A.G.)

M.I.F.A.G. is a Python application that leverages the power of OpenAI's GPT-4o Vision model to analyze screenshots from a game (in this case, Garry's Mod) and provide appropriate keyboard commands to progress through the game. This multimodal interface combines visual understanding and natural language processing to enable automated gameplay.

M.I.F.A.G. Plays Garris Mod (Demo) - https://www.youtube.com/watch?v=z0oZKTjw8gI

## Features

- **Screenshot Capture**: The application can capture screenshots from the game window at a specified interval (in seconds). This allows for continuous monitoring and analysis of the game state.

- **GPT-4o Integration**: The captured screenshots are sent to the powerful GPT-4o Vision model provided by OpenAI. This model combines computer vision and natural language processing capabilities to understand and interpret the visual content of the screenshots.

- **Game State Analysis**: The GPT-4o Vision model analyzes the screenshots and determines the current state of the game. It takes into account various visual elements, such as obstacles, paths, directional arrows, and other relevant objects or cues.

- **Decision Making**: Based on the analysis of the game state, the GPT-4o Vision model generates appropriate keyboard commands and durations. These commands are designed to navigate the character through the game environment and progress towards the objective.

- **Keyboard Command Execution**: The application parses the responses from the GPT-4o Vision model and executes the specified keyboard commands (W, A, S, D, SPACE) for the given durations. This simulates user input and controls the character's movement and actions within the game.

- **Audio Feedback**: During the gameplay process, the application provides audio feedback through beep sounds. These sounds are played when a screenshot is captured, when the GPT-4o Vision model's response is received, and when keyboard commands are executed. This auditory feedback helps users monitor the application's progress.

- **Real-time Gameplay**: The application runs in a continuous loop, capturing screenshots, sending them to the GPT-4o Vision model, and executing the received commands. This allows for real-time, automated gameplay without the need for manual user input.

The combination of visual understanding, natural language processing, and automated keyboard input makes M.I.F.A.G. a powerful tool for exploring the possibilities of multimodal interfaces in gaming and other interactive applications.

## Requirements

- Python 3.x
- OpenAI API key (with access to the GPT-4o Vision model)
- Pillow (Python Imaging Library)
- requests
- keyboard
- winsound (for Windows)

## Installation

1. Clone the repository or download the source code.
2. Install the required Python packages by running `pip install -r requirements.txt`.

## Usage

1. Run the script with `python MIFAG.bot.new.py`.
2. Enter your OpenAI API key when prompted.
3. Specify the interval (in seconds) between capturing screenshots.
4. The script will start capturing screenshots from the game window and sending them to the GPT-4o Vision model for analysis.
5. The model's responses (keyboard commands and durations) will be executed in the game window.
6. Audio feedback will be provided during the gameplay process.

## Notes

- Make sure the game window is visible and focused during the execution of the script.
- The script is designed to work with Garry's Mod, but it can be adapted to other games by modifying the instructions provided to the GPT-4o Vision model.
- The audio feedback is currently implemented for Windows systems using the winsound module. For other operating systems, you may need to modify or replace the audio functionality.

## License

This project is licensed under the MIT License.

## Acknowledgments

This project utilizes the GPT-4o Vision model provided by OpenAI. Special thanks to the OpenAI team for their groundbreaking work in artificial intelligence and natural language processing.
