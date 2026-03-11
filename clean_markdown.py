#!/usr/bin/env python
"""Remove flashy emojis and symbols from all markdown and text files"""

import os
import re
from pathlib import Path

def clean_markdown(filepath):
    """Remove emojis from markdown/text files"""
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except:
        return False
    
    original = content
    
    # Remove all emoji and symbol patterns
    emoji_patterns = [
        (r'✅', ''),
        (r'❌', ''),
        (r'🚀', ''),
        (r'🔄', ''),
        (r'🧠', ''),
        (r'💭', ''),
        (r'🔍', ''),
        (r'🎯', ''),
        (r'📚', ''),
        (r'🕷️', ''),
        (r'📈', ''),
        (r'🔧', ''),
        (r'💾', ''),
        (r'⚡', ''),
        (r'🤖', ''),
        (r'📋', ''),
        (r'🎓', ''),
        (r'💪', ''),
        (r'⏸️', ''),
        (r'📊', ''),
        (r'🎉', ''),
        (r'⚙️', ''),
        (r'📖', ''),
        (r'👋', ''),
        (r'💡', ''),
        (r'🛡️', ''),
        (r'📡', ''),
        (r'🚨', ''),
        (r'🎮', ''),
        (r'❓', ''),
        (r'🔐', ''),
        (r'📂', ''),
        (r'🏗️', ''),
        (r'🌐', ''),
        (r'⚙', ''),
        (r'✓', ''),
        (r'✗', ''),
        (r'→', '->'),
        (r'←', '<-'),
        (r'━+', '-'),
        (r'═+', '='),
        (r'─+', '-'),
    ]
    
    for pattern, replacement in emoji_patterns:
        content = re.sub(pattern, replacement, content)
    
    # Clean up multiple spaces/dashes left by emoji removal
    content = re.sub(r'  +', ' ', content)
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except:
            return False
    
    return False

# Clean markdown files
root_dir = Path(r"c:\Users\hphaniki\Downloads\Autonomous")
files_cleaned = 0

for md_file in root_dir.glob("*.md"):
    if clean_markdown(md_file):
        print(f"Cleaned: {md_file.name}")
        files_cleaned += 1

# Clean text files
for txt_file in root_dir.glob("*.txt"):
    if clean_markdown(txt_file):
        print(f"Cleaned: {txt_file.name}")
        files_cleaned += 1

print(f"\nTotal documentation files cleaned: {files_cleaned}")
