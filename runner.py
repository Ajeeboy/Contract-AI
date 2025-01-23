# Import handler libaries
import subprocess
import threading

# Define runtime command
runtime_command = r"streamlit run src\contract-ai-frontend.py"

# Define function for runner output threading
def print_webapp_output(process):
    while True:
        line = process.stdout.readline()
        if not line:
            break
        line = line.strip()
        print(line)
        if "Network URL" in line:
            break

# Execute venv bat
setup_result = subprocess.run(["run-in-venv.bat"], shell=True, capture_output=True, text=True)
print(setup_result.stdout)

# Execute runner
try:
    print(f"\nWebapp starting...")
    webapp_process = subprocess.Popen(runtime_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.DETACHED_PROCESS)
    thread = threading.Thread(target=print_webapp_output, args=(webapp_process,))
    thread.start()
    thread.join()
    print(f"\nWebapp running...\nPress CTRL+C to terminate")
    webapp_process.wait()
except KeyboardInterrupt:
    print(f"\nKeyboard interrupt received, terminating webapp...")
    webapp_process.terminate()
    webapp_process.wait()
    print(f"Webapp terminated")