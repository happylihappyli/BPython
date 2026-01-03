import sys
print(f"Python version: {sys.version}")

try:
    import socket
    print("socket imported successfully")
except Exception as e:
    print(f"Failed to import socket: {e}")

try:
    import unittest.mock
    print("unittest.mock imported successfully")
except Exception as e:
    print(f"Failed to import unittest.mock: {e}")

try:
    import functools
    print("functools imported successfully")
except Exception as e:
    print(f"Failed to import functools: {e}")

try:
    import types
    print("types imported successfully")
except Exception as e:
    print(f"Failed to import types: {e}")
