import os

file_path = r"E:\GitHub3\cpp\BPython\src\Python-3.12.2\Lib\socket.py"
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    stripped = line.strip()
    if not stripped:
        new_lines.append(line)
        continue
    
    # Check for closing brace on its own line
    if stripped == '}':
        # Skip this line
        continue
    
    # Check for opening brace at end of line
    # We use rstrip() to check the content
    rstripped = line.rstrip()
    if rstripped.endswith('{'):
        # Remove the last char '{'
        # We need to preserve the whitespace before it if it matters, 
        # but usually we can just strip the '{' and any whitespace before it?
        # No, `try: {` -> `try:`.
        # `def ... *, {` -> `def ... *,`.
        # So we just find the last `{` and remove it.
        # But be careful about `d = {'a': 1}` (one line dict). 
        # Does it end with `{`? No, it ends with `}`.
        # What about `d = {` (start of multi-line dict)?
        # I verified there are no such cases in socket.py.
        # So it is safe to remove trailing `{`.
        
        # Find the index of the last '{'
        idx = line.rfind('{')
        # Check if it's really at the end (ignoring whitespace)
        if line[idx+1:].strip() == '':
             # It is at the end. Remove it.
             # We also remove the whitespace before it?
             # `try: {` -> `try:`
             # `try:  {` -> `try:  ` -> `try:`?
             # Let's just remove the `{` and keep the line as is otherwise.
             # But if it was `try: {`, we want `try: \n`.
             # If we leave `try: `, it's fine.
             new_line = line[:idx] + line[idx+1:]
             new_lines.append(new_line)
        else:
             new_lines.append(line)
    else:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Done cleaning socket.py again")
