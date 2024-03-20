import subprocess
import sys

def main():
    try:
        with open("requirements.txt", "r") as f:
            packages = f.read().splitlines()

        print(packages)
        for package in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()