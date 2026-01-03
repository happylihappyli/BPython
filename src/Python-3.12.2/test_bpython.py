import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")
print(f"Current Working Directory: {os.getcwd()}")

# Simple calculation to ensure basic functionality
a = 10
b = 20
print(f"{a} + {b} = {a + b}")

if "bpython" in os.path.basename(sys.executable):
    print("SUCCESS: Running as bpython")
else:
    print("WARNING: Not running as bpython (executable name mismatch?)")
