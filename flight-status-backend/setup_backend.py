import os
import subprocess

# Function to run shell commands
def run_command(command):
    result = subprocess.run(command, shell=True, check=True, text=True)
    return result

# Step 1: Create virtual environment
print("Creating virtual environment...")
run_command("py -m venv venv")

# Step 2: Determine the path to the virtual environment's pip
pip_executable = os.path.join("venv", "Scripts", "pip.exe") if os.name == 'nt' else os.path.join("venv", "bin", "pip")

# Step 3: Install required packages using the virtual environment's pip
print("Installing required packages...")
run_command(f"{pip_executable} install Flask flask-cors pymongo")

print("Setup complete. Please activate your virtual environment:")
if os.name == 'nt':
    print("venv\\Scripts\\activate")
else:
    print("source venv/bin/activate")
print("Then you can run your app with 'py app.py'.")
