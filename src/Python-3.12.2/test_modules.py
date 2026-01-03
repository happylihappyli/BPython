import sys
print(f"Python version: {sys.version}")
# try:
#     import socket
#     print("socket imported successfully")
# except Exception as e:
#     print(f"Failed to import socket: {e}")

# try:
#     import importlib.abc
#     print("importlib.abc imported successfully")
# except Exception as e:
#     print(f"Failed to import importlib.abc: {e}")

try:
    import encodings.aliases
    print("encodings.aliases imported successfully")
except Exception as e:
    print(f"Failed to import encodings.aliases: {e}")

try:
    import ntpath
    print("ntpath imported successfully")
except Exception as e:
    print(f"Failed to import ntpath: {e}")
