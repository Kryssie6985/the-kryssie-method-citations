
import re

def check_tags(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.readlines()

    div_stack = []
    errors = []
    
    for i, line in enumerate(content):
        line_num = i + 1
        
        # Find all divs
        starts = [m.start() for m in re.finditer('<div', line)]
        ends = [m.start() for m in re.finditer('</div>', line)]
        
        # Simple counting on the line (not perfect for nested on same line, but good enough for this structure)
        # Better approach: tokenize the line
        
        # Let's just track the stack visually
        for match in re.finditer(r'(<div[^>]*>)|(</div>)', line):
            tag = match.group(0)
            if tag.startswith('<div'):
                div_stack.append({'line': line_num, 'tag': tag})
            elif tag == '</div>':
                if not div_stack:
                    errors.append(f"Line {line_num}: Found closing </div> but no open <div>.")
                else:
                    div_stack.pop()

    if div_stack:
        for item in div_stack:
            errors.append(f"Line {item['line']}: Unclosed {item['tag']} (End of file reached).")

    if not errors:
        print("No mismatched div tags found.")
    else:
        print("Found tag errors:")
        for e in errors:
            print(e)

if __name__ == "__main__":
    check_tags(r"C:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method-final.md")
