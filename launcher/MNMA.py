# pyinstaller --onefile --icon=../logo.ico --windowed MNMA.py

import subprocess

mfa_path = r"MFAAvalonia.exe"

subprocess.run(mfa_path)
