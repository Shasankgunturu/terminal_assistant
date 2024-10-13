import google.generativeai as genai
import os
import PIL.Image
import subprocess
from datetime import datetime

def get_time_of_day(time):
    if time < 12:
        return "Morning"
    elif time < 16:
        return "Afternoon"
    elif time < 19:
        return "Evening"
    else:
        return "Night"

# subprocess.run(["ls", "-l"]) 
curr_path = os.getcwd()
genai.configure(api_key='APIKEY')
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello, You are a terminal assistant on my Ubuntu system. My OS specs are Elementary OS based on Ubuntu 22.04. I \
         want you to understand my daily usage, help me autofill my commands, and also give me the required Linux, git, or any other commands per my\
         query. I also want you to understand my codes and file structures and recommend solutions based on my errors. I am an AI and Robotics \
         developer. Give me simple answers with only the commands and avoid any other information. Note: use apt-get and not just apt. \
         Another thing: If what you returned is a command then your output should be printing true and then the command. If if is a follow up \
         question or somethiong, then print no and then the question"},
        {"role": "model", "parts": "Great to meet you."},
    ]
)
# response = chat.send_message("You know what you are suppossed to do?")
# print(response.text)
now = datetime.now()
print(f'Good {get_time_of_day(now.hour)} Shasank.\nDate & Time: {now.ctime()}\nHow can I help you today?')
while True:
    now = datetime.now()
    query = input("User: ")
    response = chat.send_message(query)
    rest_of_words = " ".join(response.text.split()[1:])
    if response.text.split()[0] == "no":
        print("Batman: ", rest_of_words)
        continue
    print("Batman: ", rest_of_words)
    i = input("\nRun the command? y/n ")
    print()
    if i=="y":
        commands = response.text.replace("```", "").strip()
        commands = [line.strip() for line in commands.splitlines() if line.strip()]
        commands.reverse()
        for command in commands:
            # command = " ".join(command)
            # Join the list of lines into a single command string (if necessary)
            # You can skip this if the command is always on a single line
            command_list = command.split()
            result = subprocess.run(command_list, capture_output=True, text=True)
            print("Output:\n", result.stdout)
            if result.stderr:
                print("Errors :\n", result.stderr)

# print("Type something (press ESC to stop):")

# while True:
#     key = keyboard.read_event()
#     if key.name == 'esc':
#         print("\nExiting...")
#         break
#     if key.event_type == keyboard.KEY_DOWN:
#         print(key.name, end='', flush=True)  # This will print each keypress in real-time
