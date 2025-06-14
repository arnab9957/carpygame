#!/usr/bin/env python3
import re
import sys

def replace_fonts_in_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace pygame.font.SysFont with get_font
    content = re.sub(
        r'pygame\.font\.SysFont\("arial", (\d+), bold=True\)',
        r'get_font(\1, bold=True)',
        content
    )
    
    content = re.sub(
        r'pygame\.font\.SysFont\("arial", (\d+)\)',
        r'get_font(\1)',
        content
    )
    
    content = re.sub(
        r'pygame\.font\.SysFont\(None, ([^)]+)\)',
        r'get_font(\1)',
        content
    )
    
    # Write the modified content back to the file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Font replacements completed in {filename}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        replace_fonts_in_file(sys.argv[1])
    else:
        print("Please provide a filename as an argument")
