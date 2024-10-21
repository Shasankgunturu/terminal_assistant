import sys
import termios
import tty

# Function to capture keypress in real-time
def get_keypress():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)  # Read one character at a time
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

# Dummy function to simulate your model providing suggestions
def get_model_suggestion(partial_command):
    # Replace this with actual model interaction logic
    suggestions = {
        "ls": ["ls -l", "ls -a", "ls /home"],
        "git": ["git status", "git add", "git commit -m 'message'"]
    }
    return suggestions.get(partial_command, [])

# Function to display the suggestion in lighter (dim) style
def display_suggestion(partial_command, suggestions):
    if suggestions:
        # Print the suggestion in lighter text style (dimmed)
        print(f"\033[2m{suggestions[0]}\033[0m", end='\r', flush=True)

# Main function to interactively capture input and show suggestions
def main():
    partial_command = ""
    while True:
        key = get_keypress()  # Capture single keypress
        if key == "q":  # User presses Enter
            sys.stdout.write("\n")  # Move to the next line
            break
        elif key == "\x7f":  # Backspace handling
            partial_command = partial_command[:-1]
        else:
            partial_command += key  # Append the character to the current input
        
        # Get suggestions based on the current input
        suggestions = get_model_suggestion(partial_command)
        
        # Clear the current line
        sys.stdout.write("\033[K")  # ANSI escape code to clear the line
        sys.stdout.write(f"{partial_command}")  # Print the user's input
        
        # Display the suggestion in lighter text
        display_suggestion(partial_command, suggestions)

if __name__ == "__main__":
    main()
