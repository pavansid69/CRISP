import subprocess
import sys

def run_script(script_name):
    """Run a Python script using subprocess and handle errors."""
    try:
        print(f"\nRunning {script_name}...")
        subprocess.run([sys.executable, script_name], check=True)
        print(f"Successfully executed {script_name}.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing {script_name}.")
        print(f"Error details: {e}")

if __name__ == "__main__":
    # List of scripts to execute in order
    scripts = [
        "sentiment_analysis.py",
        "risk_analysis.py",
        "client_satisfaction.py"
    ]

    # Run each script in sequence
    for script in scripts:
        run_script(script)

    print("All scripts have been executed successfully.")
    sys.stdout.flush()
