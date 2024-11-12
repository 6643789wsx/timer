import os
from datetime import datetime

# ...existing code...

log_dir = './log'
files = sorted(os.listdir(log_dir))
if files:
    last_file = files[-1]
    with open(os.path.join(log_dir, last_file), 'r+') as f:
        content = f.read()
        if "End time:" not in content:
            f.write(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ...existing code...
