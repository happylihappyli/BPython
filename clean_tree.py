import os

ROOT_DIR = r"E:\GitHub3\cpp\BPython\src\Python-3.12.2\Lib"

def clean_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    changed = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            new_lines.append(line)
            continue
        
        # Check for closing brace on its own line
        if stripped == '}':
            changed = True
            continue
        
        rstripped = line.rstrip()
        
        # Check for opening brace patterns
        if rstripped.endswith(': {'):
            idx = line.rfind(': {')
            new_line = line[:idx+1] + line[idx+3:]
            new_lines.append(new_line)
            changed = True
        elif rstripped.endswith(':{'):
            idx = line.rfind(':{')
            new_line = line[:idx+1] + line[idx+2:]
            new_lines.append(new_line)
            changed = True
        elif rstripped.endswith('\\ {'):
            idx = line.rfind('\\ {')
            new_line = line[:idx+1] + line[idx+3:]
            new_lines.append(new_line)
            changed = True
        elif rstripped.endswith('\\{'):
            idx = line.rfind('\\{')
            new_line = line[:idx+1] + line[idx+2:]
            new_lines.append(new_line)
            changed = True
        else:
            new_lines.append(line)

    if changed:
        print(f"Cleaning {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

def main():
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    clean_file(file_path)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    main()
