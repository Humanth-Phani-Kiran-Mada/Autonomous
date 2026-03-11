#!/usr/bin/env python
"""Carefully remove emojis only from logger calls and comments"""

import os
import re
from pathlib import Path

def clean_python_file(filepath):
    """Remove emojis only from string literals (logger calls and comments)"""
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except:
        return False
    
    original_lines = lines.copy()
    modified = False
    
    # Emoji patterns to remove
    emojis = r'[✅❌🚀🔄🧠💭🔍🎯📚🕷️📈🔧💾⚡🤖📋🎓💪⏸️📊🎉⚙️📖👋💡🛡️📡🚨🎮❓🔐📂🏗️🌐]'
    
    for i, line in enumerate(lines):
        # Only process lines with logger calls or strings
        if 'logger.' in line or 'print(' in line or ('"' in line) or ("'" in line):
            # Remove emojis from the line
            new_line = re.sub(emojis, '', line)
            
            if new_line != line:
                lines[i] = new_line
                modified = True
    
    if modified:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True
        except:
            return False
    
    return False

# Clean all Python files
src_dir = Path(r"c:\Users\hphaniki\Downloads\Autonomous\src")
files_cleaned = 0

for py_file in src_dir.glob("*.py"):
    if clean_python_file(py_file):
        print(f"Cleaned: {py_file.name}")
        files_cleaned += 1

# Clean root Python files
root_dir = Path(r"c:\Users\hphaniki\Downloads\Autonomous")
for py_file in ['main.py', 'config.py', 'test_phase1.py']:
    py_path = root_dir / py_file
    if py_path.exists() and clean_python_file(py_path):
        print(f"Cleaned: {py_file}")
        files_cleaned += 1

print(f"\nTotal Python files cleaned: {files_cleaned}")
