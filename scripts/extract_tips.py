import re

source_file = "../Ebook Draft (PTI)_ The Kryssie Method - Mastering AI Col....docx.md"
target_file = "literature_testing/kryssie-method.md" 

output_extraction = "extracted_tips.txt"

with open(source_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

tips = []
# Patterns to identifying tips
tip_patterns = [
    r"♊︎ Pro tip:",
    r"Ace's Tips!",
    r"Pro tip from 2.5 Pro!",
    r"Pro Tip:",
    r"\*\*Tip:\*\*",
    r"Gemini.*Tip"
]

current_tip = None
context_window = []
extracted_count = 0

for i, line in enumerate(lines):
    line = line.strip()
    if not line:
        continue
    
    is_tip_start = False
    for pat in tip_patterns:
        if re.search(pat, line, re.IGNORECASE):
            is_tip_start = True
            break
    
    if is_tip_start:
        # Capture the tip and some preceding context
        context = context_window[-2:] if len(context_window) >= 2 else context_window
        tips.append({
            "line_num": i + 1,
            "context": context,
            "tip_content": line
        })
        extracted_count += 1
    
    context_window.append(line)

# Sort and print for review
with open(output_extraction, "w", encoding="utf-8") as f:
    f.write(f"Total Tips Found: {extracted_count}\n")
    f.write("="*40 + "\n\n")
    for tip in tips:
        f.write(f"Line {tip['line_num']}\n")
        f.write(f"Context: {tip['context']}\n")
        f.write(f"Tip: {tip['tip_content']}\n")
        f.write("-" * 20 + "\n")

print(f"Extraction complete. Found {extracted_count} tips.")
