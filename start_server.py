import subprocess
import time
import os

def start_server():
    os.chdir(os.path.join(os.path.dirname(__file__), 'f2'))
    proc = subprocess.Popen([
        'python', 'main.py'
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    print("Server started with PID:", proc.pid)
    
    while True:
        line = proc.stdout.readline()
        if line:
            print(line.strip())
        if proc.poll() is not None:
            print("Server exited with code:", proc.returncode)
            break

if __name__ == "__main__":
    start_server()