import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = 'Win32GUI'
if sys.platform == "win32":
    base = "Win32GUI"

setup(name = "Caliper",
      version = "0.1",
      description = "Caliper for ECG",
      options = {"build_exe": build_exe_options},
      executables = [Executable(script="browser.py", base = 'Win32GUI'), Executable(script="mainApp.py", base = 'Win32GUI'), Executable(script="Caliper.py", base = 'Win32GUI', icon='installer.ico')])