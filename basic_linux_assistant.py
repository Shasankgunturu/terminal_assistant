# to add:
# give output also for decoding as when debugging carry_errors
# multiple lines input while doing so
# deal with &&
# auto complete
# !source my-venv/bin/activate
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
 
curr_path = os.getcwd()
genai.configure(api_key=os.environ['APIKEY'])
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello, I am Shasank. You are a terminal assistant on my Ubuntu system. I would like to call you Batman. \
         If someone asks your name, reply with I'm Batman. My OS specs are based on Ubuntu 24.04. I \
         want you to understand my daily usage, help me autofill my commands, and also give me the required Linux, git, or any other commands per my\
         query. I also want you to understand my codes and file structures and recommend solutions based on my errors. I am an AI and Robotics \
         developer. Give me simple answers with only the commands and avoid any other information. Note: use apt-get and not just apt. \
         Another thing: If what you returned is a command then your output should be printing true and then the command. If if is a follow up \
         question or somethiong, then print no and then the question. If you have multiple commands to give, give them in seperate lines."},
        {"role": "model", "parts": "Great to meet you."},
    ]
)

now = datetime.now()
print(f'Good {get_time_of_day(now.hour)} Shasank.\nDate & Time: {now.ctime()}\nHow can I help you today?')
carry_errors = []
carry_outputs = []
carry_commands = []
while True:
    now = datetime.now()
    if carry_errors:
        query = input("User: Would you like to look up previous error? y/n ")

        if query=="y":
            if len(carry_errors)>1:
                print("Select the error you want to follow up: ")
                for i in range(len(carry_errors)):
                    print(f'{i+1}: {carry_errors[i]}')
                number = input("Enter the number of the error ")
            else:
                number=1
            query = "command: "+carry_commands[number-1] + ", output: " + carry_outputs[number-1] + ", error: " +carry_errors[number-1]
        elif query=="n":
            pass        
        carry_errors.clear()  
        carry_outputs.clear()
        carry_commands.clear()  
    else:
        query = input("User: ")
    if query == "thanks that is all for now":
        response = chat.send_message(query)
        rest_of_words = " ".join(response.text.split()[1:])
        print(rest_of_words)
        break
    response = chat.send_message(query)
    rest_of_words = " ".join(response.text.split()[1:])
    if response.text.split()[0] == "no":
        print("Batman: ", rest_of_words)
        continue
    print("Batman: ", rest_of_words)
    i = input("\nRun the command? y/n ")
    # while i!="y" or i!="n":
        # i = input("\nRun the command? y/n ")
    print()
    if i=="y":
        commands = rest_of_words.replace("```", "").strip()
        commands = [line.strip() for line in commands.splitlines() if line.strip()]
        commands.reverse()
        for command in commands:
            command_list = command.split()
            result = subprocess.run(command_list, capture_output=True, text=True)
            if result.stdout:
                print("Output:\n", result.stdout)
            if result.stderr:
                print("Errors :\n", result.stderr)
                carry_errors.append(result.stderr)
                carry_outputs.append(result.stdout)
                carry_commands.append(command)

# print("Type something (press ESC to stop):")

# while True:
#     key = keyboard.read_event()
#     if key.name == 'esc':
#         print("\nExiting...")
#         break
#     if key.event_type == keyboard.KEY_DOWN:
#         print(key.name, end='', flush=True)  # This will print each keypress in real-time
