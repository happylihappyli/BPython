import os
import shutil

SOURCE_ROOT = os.getcwd()
EXTERNALS_LIB = os.path.join(SOURCE_ROOT, "externals", "pythonx86", "tools", "Lib")
LIB_ROOT = os.path.join(SOURCE_ROOT, "Lib")

MODULES = [
    "importlib/_bootstrap.py",
    "importlib/_bootstrap_external.py",
    "zipimport.py",
    "abc.py",
    "codecs.py",
    "io.py",
    "_collections_abc.py",
    "_sitebuiltins.py",
    "genericpath.py",
    "ntpath.py",
    "posixpath.py",
    "os.py",
    "site.py",
    "stat.py",
    "importlib/util.py",
    "importlib/machinery.py",
    "runpy.py",
]

def restore():
    for mod in MODULES:
        src = os.path.join(EXTERNALS_LIB, mod.replace("/", os.sep))
        dst = os.path.join(LIB_ROOT, mod.replace("/", os.sep))
        
        if os.path.exists(src):
            print(f"Restoring {mod} from {src}...")
            shutil.copy2(src, dst)
        else:
            print(f"Warning: Source not found for {mod} at {src}")

if __name__ == "__main__":
    restore()