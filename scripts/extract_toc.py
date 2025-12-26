
import re

def extract_toc():
    with open('toc.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    toc_lines = []
    capture = False
    
    # We want to start capturing after "Table of Contents" entry
    # And stop before the actual content starts (H1 header)
    
    start_marker_found = False
    
    for line in lines:
        if "Table of Contents" in line and "](" in line:
            start_marker_found = True
            continue
        
        if start_marker_found:
            # content usually starts with strict H1 not indented
            # In toc.md, the content follows the TOC list.
            # The TOC list items are indented by 2 or more spaces usually, except the title one.
            # But the Title one was line 10.
            # The Foreword is line 13, indented by 2.
            
            if line.startswith("# "): # The main content starts
                break
            
            # Remove 2 spaces of indentation to shift left
            if line.startswith("  "):
                clean_line = line[2:]
                toc_lines.append(clean_line)
            elif line.startswith("- ["): # Should not happen if strictly under title, but just in case
                toc_lines.append(line)

    with open('toc_clean.md', 'w', encoding='utf-8') as f:
        f.writelines(toc_lines)

if __name__ == "__main__":
    extract_toc()
