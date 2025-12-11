import re

file_path = "kryssie-method.md"

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Count occurrences
pro_tip_count = text.lower().count("pro tip")
ace_tip_count = text.lower().count("ace's tip")
gemini_tip_count = text.lower().count("gemini pro")
emoji_count = text.count("♊︎")

print(f"Pro Tip count: {pro_tip_count}")
print(f"Ace's Tip count: {ace_tip_count}")
print(f"Gemini Pro count (any context): {gemini_tip_count}")
print(f"♊︎ emoji count: {emoji_count}")

# Print samples of lines with "♊︎"
print("-" * 20)
print("Sample lines with ♊︎:")
lines = text.split('\n')
for line in lines:
    if "♊︎" in line:
        print(line.strip()[:60] + "...")
