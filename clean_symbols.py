#!/usr/bin/env python
"""Remove flashy emojis and symbols from all Python files"""

import os
import re
from pathlib import Path

def clean_file(filepath):
 """Remove emojis and flashy symbols from a file"""
 
 # Read file with robust encoding
 try:
 with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
 content = f.read()
 except:
 return False
 
 original = content
 
 # Remove all emoji and symbol patterns
 emoji_patterns = [
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'', ''),
 (r'+', ''), # Remove decorative lines with 
 (r'+', ''), # Remove decorative lines with 
 (r'+', ''), # Remove decorative lines with 
 ]
 
 for pattern, replacement in emoji_patterns:
 content = re.sub(pattern, replacement, content)
 
 # Clean up multiple spaces and newlines left by emoji removal
 content = re.sub(r' +', ' ', content)
 content = re.sub(r'\n\n\n+', '\n\n', content)
 
 # Only write if content changed
 if content != original:
 try:
 with open(filepath, 'w', encoding='utf-8') as f:
 f.write(content)
 return True
 except:
 return False
 
 return False

# Find and clean all Python files
src_dir = Path(r"c:\Users\hphaniki\Downloads\Autonomous\src")
files_cleaned = 0

for py_file in src_dir.glob("*.py"):
 if clean_file(py_file):
 print(f"Cleaned: {py_file.name}")
 files_cleaned += 1
 else:
 print(f"Skipped: {py_file.name}")

# Clean main.py and other root Python files
root_dir = Path(r"c:\Users\hphaniki\Downloads\Autonomous")
for py_file in root_dir.glob("*.py"):
 if py_file.name not in ['fix_imports.py', 'fix_quotes.py']:
 if clean_file(py_file):
 print(f"Cleaned: {py_file.name}")
 files_cleaned += 1

print(f"\nTotal Python files cleaned: {files_cleaned}")
