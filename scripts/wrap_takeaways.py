import re

def wrap_takeaways(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    in_takeaways = False
    
    # Regex to detect start
    start_pattern = re.compile(r'^##### \*Key Takeaways')

    for i, line in enumerate(lines):
        # DETECT START
        if start_pattern.match(line):
            if not in_takeaways:
                # Add newline before opening div if not present
                if new_lines and new_lines[-1].strip() != '':
                    new_lines.append('\n')
                new_lines.append('<div class="key-takeaways">\n\n')
                in_takeaways = True
        
        # DETECT END (Look for '---' separator or next major header or div)
        # But allow blank lines inside.
        if in_takeaways:
            # Check if we hit a terminator
            if line.strip() == '---' or line.strip().startswith('<div') or line.startswith('##'):
                 # Close existing takeaway
                 # Ensure newline before closing div
                 if new_lines and new_lines[-1].strip() != '':
                     new_lines.append('\n')
                 new_lines.append('</div>\n\n')
                 in_takeaways = False

        new_lines.append(line)

    # Handle case where file ends inside a takeaway
    if in_takeaways:
         new_lines.append('\n</div>\n')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"Processed {file_path}. Added wrappers.")

if __name__ == "__main__":
    wrap_takeaways(r"C:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method.md")
