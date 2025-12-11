import re

file_path = "kryssie-method.md"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

tip_lines = []
for i, line in enumerate(lines):
    # distinct visual markers often used
    if "Tip" in line or "tip" in line:
        # Filter for likely header usage
        if re.search(r"(?:Pro|Ace|Gemini|Key).*Tip", line, re.IGNORECASE) or "Tip:" in line:
             # Exclude "Key Takeaways" as they are handled separately
            if "Key Takeaways" in line:
                continue
            tip_lines.append((i + 1, line.strip()))

print(f"Total Potential Matches: {len(tip_lines)}")
print("-" * 30)
for ln, text in tip_lines:
    print(f"Line {ln}: {text}")
