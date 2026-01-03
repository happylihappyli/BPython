import sys
import importlib
import importlib.machinery
import importlib.util
import os

print(f"sys.path: {sys.path}")
print(f"cwd: {os.getcwd()}")

# Check if site.py ran and updated suffixes
try:
    import importlib._bootstrap_external as be
    print(f"SOURCE_SUFFIXES: {be.SOURCE_SUFFIXES}")
except Exception as e:
    print(f"Could not check SOURCE_SUFFIXES: {e}")

# Check hooks
print("sys.path_hooks items:")
for hook in sys.path_hooks:
    print(f"  {hook}")

# Try finding spec manually
print("\nTrying find_spec('utils'):")
try:
    spec = importlib.machinery.PathFinder.find_spec('utils')
    print(f"Spec for utils: {spec}")
except Exception as e:
    print(f"find_spec failed: {e}")

# Try import
print("\nTrying import utils:")
try:
    import utils
    print(f"Successfully imported utils: {utils}")
    print(f"utils file: {utils.__file__}")
except Exception as e:
    print(f"Import failed: {e}")
