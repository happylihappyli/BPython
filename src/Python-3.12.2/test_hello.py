print("Hello from built python!")
try:
    import socket
    print("Socket imported")
except ImportError as e:
    print(f"Socket import failed: {e}")
