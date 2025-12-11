import re
import collections

file_path = "kryssie-method.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Pattern attempts to catch variations like:
# ***Pro Tip:***
# *Ace's Tip:*
# **Gemini Pro 2.5 Tip:**
# Tip:
regex = r"(\*{1,3})(.*?(?:Tip|Tips).*?)\1"

matches = re.findall(regex, content, re.IGNORECASE)

counts = collections.Counter()
detailed_matches = []

for m in matches:
    # m[1] is the inner text, e.g., "Pro Tip:" or "Ace's Tip"
    raw_text = m[1].strip()
    # Clean up colon and whitespace
    clean_text = raw_text.strip(":").strip()
    counts[clean_text] += 1
    detailed_matches.append(clean_text)

print(f"Total Matches: {len(detailed_matches)}")
print("-" * 30)
for type_name, count in counts.most_common():
    print(f"{type_name}: {count}")
print("-" * 30)
