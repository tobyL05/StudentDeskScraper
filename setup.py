import subprocess
import os

print("Running startup")
path_to_req = os.getcwd() + "\\requirements.txt"
cmd = f"pip install -r {path_to_req}"
try:
	subprocess.run(args=cmd)
except:
	print("Error downloading modules")
from src.login import start
start()