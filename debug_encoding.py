
import sys
import os
import codecs

print(f"sys.executable: {sys.executable}")
print(f"sys.path: {sys.path}")

try:
    import encodings
    print(f"encodings package: {encodings}")
    import encodings.aliases
    print(f"encodings.aliases: {encodings.aliases.aliases.get('latin1')}")
except ImportError as e:
    print(f"ImportError: {e}")

try:
    print("Attempting to import encodings.latin_1 directly...")
    import encodings.latin_1
    print("Success importing encodings.latin_1")
    if hasattr(codecs, 'latin_1_encode'):
        print("codecs.latin_1_encode exists")
    else:
        print("codecs.latin_1_encode MISSING")
except ImportError as e:
    print(f"Error importing encodings.latin_1: {e}")
except Exception as e:
    print(f"Error importing encodings.latin_1 (Exception): {e}")

try:
    import codecs
    print("Attempting to lookup latin1...")
    codecs.lookup('latin1')
    print("Success looking up latin1")
except Exception as e:
    print(f"Error looking up latin1: {e}")

try:
    import codecs
    print("Attempting to lookup utf8...")
    codecs.lookup('utf8')
    print("Success looking up utf8")
except Exception as e:
    print(f"Error looking up utf8: {e}")

try:
    s = b"test".decode("latin1")
    print(f"Decoded: {s}")
except Exception as e:
    print(f"Error decoding latin1: {e}")
