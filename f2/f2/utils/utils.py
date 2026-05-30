import os
import re
from datetime import datetime

def create_user_folder(path):
    os.makedirs(path, exist_ok=True)
    return path

def format_file_name(name, max_length=50):
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    return name[:max_length]

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_size(bytes_size):
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.2f} KB"
    else:
        return f"{bytes_size / (1024 * 1024):.2f} MB"