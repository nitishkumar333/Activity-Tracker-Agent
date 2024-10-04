import os
import sys
import subprocess

def install_requirements():
    """Install dependencies from requirements.txt."""
    try:
        # Get the absolute path for requirements.txt
        requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
        
        # Run pip install for the requirements file
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing requirements: {e}")

def initialize():
    """Perform initialization tasks."""
    print("Running setup for the first time...")
    install_requirements()  # Install the required packages

    # Create a file to indicate that the program has run
    first_run_path = os.path.join(os.path.dirname(__file__), 'first_run.txt')
    with open(first_run_path, 'w') as f:
        f.write('You are good to Go.')
