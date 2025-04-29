import os
import sys
import subprocess

exe_path = "MFATools/MFATools.exe"
if os.path.exists(exe_path):
    subprocess.Popen(exe_path)
