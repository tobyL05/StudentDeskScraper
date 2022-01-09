import subprocess
import os
from src.login import start

print("Running startup")
path_to_req = os.getcwd() + "\\requirements.txt"
cmd = f"pip install -r {path_to_req}"
subprocess.run(args=cmd,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
start()