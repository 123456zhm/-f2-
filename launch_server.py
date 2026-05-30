import subprocess
import os
import time

def launch_server():
    os.chdir(r'C:\Users\123\Desktop\f2-xiaohongshu-changes\f2')
    
    process = subprocess.Popen(
        ['python', '-m', 'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8000'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    print("Starting server...")
    time.sleep(3)
    
    if process.poll() is None:
        print("Server started successfully!")
        print("Server is running on http://localhost:8000")
        print("Press Ctrl+C to stop the server")
        
        try:
            while True:
                line = process.stdout.readline()
                if line:
                    print("[SERVER]", line.strip())
        except KeyboardInterrupt:
            print("\nStopping server...")
            process.terminate()
            process.wait()
            print("Server stopped.")
    else:
        print("Server failed to start!")
        output = process.stdout.read()
        print("Error output:")
        print(output)

if __name__ == "__main__":
    launch_server()