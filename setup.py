import os

def reqs():
	print("Running startup")
	path_to_req = os.path.dirname(__file__) + "\\requirements.txt"
	cmd = f"pip install -r {path_to_req}"
	os.system(cmd)


if __name__ == "__main__":
	reqs()
	from src.login import start
	start()
