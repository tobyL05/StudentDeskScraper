import subprocess
import os
from src.login import start

print("Running startup")
path_to_req = os.getcwd() + "\\requirements.txt"
cmd = f"pip install -r {path_to_req}"
try:
	subprocess.run(args=cmd)
except:
	print("Error downloading modules")
with open('filx.txt','x') as f:
	f.write(path_to_req)
f.close()
#print(path_to_req)
#start()