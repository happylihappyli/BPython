import os
import subprocess
import sys

# Paths
REPO_ROOT = r"E:\GitHub3\cpp\BPython\src\Python-3.12.2"
PCBUILD_DIR = os.path.join(REPO_ROOT, "PCbuild", "amd64")
FREEZE_MODULE_EXE = os.path.join(PCBUILD_DIR, "_freeze_module_d.exe")
DEEPFREEZE_PY = os.path.join(REPO_ROOT, "Tools", "build", "deepfreeze.py")
FROZEN_MODULES_DIR = os.path.join(REPO_ROOT, "Python", "frozen_modules")
DEEPFREEZE_C = os.path.join(REPO_ROOT, "Python", "deepfreeze", "deepfreeze.c")

# Module definitions: (module_name, source_rel_path, header_rel_path)
# Based on _freeze_module.vcxproj and Makefile.pre.in
MODULES = [
    ("importlib._bootstrap", "Lib/importlib/_bootstrap.py", "Python/frozen_modules/importlib._bootstrap.h"),
    ("importlib._bootstrap_external", "Lib/importlib/_bootstrap_external.py", "Python/frozen_modules/importlib._bootstrap_external.h"),
    ("zipimport", "Lib/zipimport.py", "Python/frozen_modules/zipimport.h"),
    ("abc", "Lib/abc.py", "Python/frozen_modules/abc.h"),
    ("codecs", "Lib/codecs.py", "Python/frozen_modules/codecs.h"),
    ("io", "Lib/io.py", "Python/frozen_modules/io.h"),
    ("_collections_abc", "Lib/_collections_abc.py", "Python/frozen_modules/_collections_abc.h"),
    ("_sitebuiltins", "Lib/_sitebuiltins.py", "Python/frozen_modules/_sitebuiltins.h"),
    ("genericpath", "Lib/genericpath.py", "Python/frozen_modules/genericpath.h"),
    ("ntpath", "Lib/ntpath.py", "Python/frozen_modules/ntpath.h"),
    ("posixpath", "Lib/posixpath.py", "Python/frozen_modules/posixpath.h"),
    ("os", "Lib/os.py", "Python/frozen_modules/os.h"),
    ("site", "Lib/site.py", "Python/frozen_modules/site.h"),
    ("stat", "Lib/stat.py", "Python/frozen_modules/stat.h"),
    ("importlib.util", "Lib/importlib/util.py", "Python/frozen_modules/importlib.util.h"),
    ("importlib.machinery", "Lib/importlib/machinery.py", "Python/frozen_modules/importlib.machinery.h"),
    ("runpy", "Lib/runpy.py", "Python/frozen_modules/runpy.h"),
    ("__hello__", "Lib/__hello__.py", "Python/frozen_modules/__hello__.h"),
    ("__phello__", "Lib/__phello__/__init__.py", "Python/frozen_modules/__phello__.h"),
    ("__phello__.ham", "Lib/__phello__/ham/__init__.py", "Python/frozen_modules/__phello__.ham.h"),
    ("__phello__.ham.eggs", "Lib/__phello__/ham/eggs.py", "Python/frozen_modules/__phello__.ham.eggs.h"),
    ("__phello__.spam", "Lib/__phello__/spam.py", "Python/frozen_modules/__phello__.spam.h"),
    ("frozen_only", "Tools/freeze/flag.py", "Python/frozen_modules/frozen_only.h"),
]

def main():
    if not os.path.exists(FREEZE_MODULE_EXE):
        print(f"Error: {FREEZE_MODULE_EXE} not found.")
        return

    # 1. Generate headers
    print("Generating frozen module headers...")
    os.makedirs(FROZEN_MODULES_DIR, exist_ok=True)
    
    generated_headers = []
    
    for mod_name, src_rel, hdr_rel in MODULES:
        src_path = os.path.join(REPO_ROOT, src_rel.replace("/", os.sep))
        hdr_path = os.path.join(REPO_ROOT, hdr_rel.replace("/", os.sep))
        
        if not os.path.exists(src_path):
            print(f"Warning: Source {src_path} not found. Skipping {mod_name}.")
            continue
            
        cmd = [FREEZE_MODULE_EXE, mod_name, src_path, hdr_path]
        print(f"  Freezing {mod_name}...")
        try:
            subprocess.check_call(cmd)
            generated_headers.append(f"{hdr_path}:{mod_name}")
        except subprocess.CalledProcessError as e:
            print(f"  Error freezing {mod_name}: {e}")
            # If freezing fails, we should probably stop or at least note it.
            # deepfreeze might fail if some are missing.

    # 2. Run deepfreeze.py
    print("\nRunning deepfreeze.py...")
    
    # Check if deepfreeze.py exists
    if not os.path.exists(DEEPFREEZE_PY):
        print(f"Error: {DEEPFREEZE_PY} not found.")
        return

    # Ensure output directory exists
    os.makedirs(os.path.dirname(DEEPFREEZE_C), exist_ok=True)

    deepfreeze_args = [sys.executable, DEEPFREEZE_PY] + generated_headers + ["-o", DEEPFREEZE_C]
    
    try:
        subprocess.check_call(deepfreeze_args)
        print(f"Successfully generated {DEEPFREEZE_C}")
    except subprocess.CalledProcessError as e:
        print(f"Error running deepfreeze.py: {e}")

if __name__ == "__main__":
    main()
