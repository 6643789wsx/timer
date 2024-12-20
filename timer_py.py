import time
import tkinter as tk
import ctypes
import os
from datetime import datetime

def update_time():
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)
    if not is_locked():
        time_label.config(text=f"Time fly: {minutes} minutes {seconds} seconds")
        root.after(1000, update_time)
    else:
        # 下面的工作交给end_check了
        # log_end_time()
        root.destroy()

def is_locked():
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    return hwnd == 0 or user32.GetAsyncKeyState(0x5B) != 0  # 0x5B is the virtual key code for the left Windows key

def log_start_time():
    global log_file
    if not os.path.exists('log'):
        os.makedirs('log')
    log_file = os.path.join('log', f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    with open(log_file, 'a') as f:
        f.write(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def log_end_time():
    with open(log_file, 'r+') as f:
        content = f.read()
        if "End time:" not in content:
            f.write(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Timer")
    root.geometry("350x70")
    root.attributes("-topmost", True)  

    start_time = time.time()
    log_start_time()

    time_label = tk.Label(root, text="", font=("Helvetica", 16))
    time_label.pack(pady=20)

    update_time()
    root.mainloop()