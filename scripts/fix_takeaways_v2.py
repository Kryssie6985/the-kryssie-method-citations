import re

def fix_takeaways(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Cleanup format (remove the specific empty block created by previous script)
    # The previous script likely made: <div class="key-takeaways">\n\n</div>\n\n
    content = re.sub(r'<div class="key-takeaways">\s*</div>\s*', '', content)
    
    lines = content.splitlines(keepends=True)
    new_lines = []
    in_takeaways = False
    
    start_pattern = re.compile(r'^##### \*Key Takeaways')

    for i, line in enumerate(lines):
        # DETECT START
        if start_pattern.match(line):
            if not in_takeaways:
                if new_lines and new_lines[-1].strip() != '':
                    new_lines.append('\n')
                new_lines.append('<div class="key-takeaways">\n\n')
                in_takeaways = True
                new_lines.append(line)
                continue # Skip terminator check for the start line itself!
        
        # DETECT END
        if in_takeaways:
            # Terminate on Horizontal Rule '---' or Start of a Div (Part Page)
            # The List is inside, so we don't want to terminate on text lines.
            is_terminator = False
            if line.strip() == '---':
                is_terminator = True
            elif line.strip().startswith('<div class="part-page"'):
                 is_terminator = True
            
            if is_terminator:
                 if new_lines and new_lines[-1].strip() != '':
                     new_lines.append('\n')
                 new_lines.append('</div>\n\n')
                 in_takeaways = False
        
        new_lines.append(line)

    # Convert safely
    final_output = "".join(new_lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_output)
    
    print(f"Processed {file_path}. Cleaned debris and re-wrapped.")

if __name__ == "__main__":
    fix_takeaways(r"C:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method.md")
