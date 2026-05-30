import subprocess
import time
import os
import sys

def test_server():
    os.chdir(os.path.join(os.path.dirname(__file__), 'f2'))
    
    proc = subprocess.Popen([
        'python', 'main.py'
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    print("Server started with PID:", proc.pid)
    
    time.sleep(2)
    
    if proc.poll() is None:
        print("Server is running!")
        
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        result = s.connect_ex(('10.61.0.2', 8000))
        if result == 0:
            print("Port 8000 is open!")
            s.close()
        else:
            print("Port 8000 is closed!")
            
        try:
            while True:
                line = proc.stdout.readline()
                if line:
                    print("[SERVER]", line.strip())
                if proc.poll() is not None:
                    print("Server exited with code:", proc.returncode)
                    break
        except KeyboardInterrupt:
            print("\nStopping server...")
            proc.terminate()
    else:
        print("Server failed to start! Exit code:", proc.returncode)
        output = proc.stdout.read()
        print("Error output:")
        print(output)

if __name__ == "__main__":
    test_server()