'''
This code runs the python codes in the Codes folder by a designed order, that autimates the process of data mining, processing, and visualisation.
'''

import subprocess
import os

codes_directory = 'task_code' # Define the path to the 'Codes' directory

scripts = [ '1. initial_setups.py',  '2. traffic_data.py', '3. loops_for_data.py']


def run(script_name): # Function to run each script
    script_path = os.path.join(codes_directory, script_name)
    try:
        with open(os.devnull, 'wb') as devnull:
                subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError:
        print(f"\nError occurred while running script: {script_name}")
        exit(1)

for name in scripts:
    print('Currently running:', name)
    run(name)

print('All scripts are executed')