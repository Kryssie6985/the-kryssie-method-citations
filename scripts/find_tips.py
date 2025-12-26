
import re

FILE_PATH = r"C:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method.md"

def scan_file():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_header = "Start of File"
    header_stack = []
    
    tips = []
    
    # regex patterns
    re_header = re.compile(r"^(#+)\s+(.+)")
    re_bubble = re.compile(r'<div class="speech-bubble')
    re_generic_tip = re.compile(r"(\*\*\*)?(Pro Tip|Tip:|Ace's Tip|Gemini:|Pro tip:|GPT Note:)(\*\*)?", re.IGNORECASE)
    re_todo = re.compile(r"<!--\s*TODO.*-->")

    for i, line in enumerate(lines):
        line = line.strip()
        
        # Header Check
        header_match = re_header.match(line)
        if header_match:
            level = len(header_match.group(1))
            title = header_match.group(2)
            current_header = f"{'#'*level} {title}"
            continue

        # Tip Check
        if re_bubble.search(line):
            tips.append({
                "line": i + 1,
                "type": "Speech Bubble",
                "header": current_header,
                "content": line[:100] + "..." # Snippet
            })
        elif re_generic_tip.search(line):
             # check if inside a speech bubble (simple heuristic: if previous line was bubble start?)
             # actually just log it, we can filter duplicates
             tips.append({
                "line": i + 1,
                "type": "Text Pattern",
                "header": current_header,
                "content": line[:100] + "..."
            })
        elif re_todo.search(line) and ("Ace" in line or "Tip" in line):
             tips.append({
                "line": i + 1,
                "type": "TODO Tip",
                "header": current_header,
                "content": line
            })

    with open("tips_found.txt", "w", encoding="utf-8") as f:
        f.write(f"Found {len(tips)} tips.\n")
        for t in tips:
            f.write(f"Line {t['line']} | {t['header']} | {t['type']} | {t['content']}\n")
    print(f"Saved {len(tips)} tips to tips_found.txt")

if __name__ == "__main__":
    scan_file()
