
import os

# Update the Citation Map in kryssie-method.md with manual fixes

file_path = r'c:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method.md'
base_url = "https://github.com/kryssie6985/the-kryssie-method-citations/blob/main/sources"

# Manual Mappings
mappings = {
    "[cite:151-193]": f"{base_url}/how_to_talk_to_gemini.pdf",
    "[cite:_194-228]": f"{base_url}/advanced_gemini_interaction.md",
    "[cite:_127-150]": f"{base_url}/interaction_kryssie_style_vol_3.md",
    "[cite:_1-169]": f"{base_url}/interaction_kryssie_style_part_4.md",
    # Orphan/Dead link - pointing to placeholder or keeping as is? 
    # User said "only 1 i think is dead". I'll create a placeholder for it earlier.
    # Assuming I created 'conversation_history_research.md' or similar?
    # Actually I tried to create 'conversation_history_research.md' in step 708 but it was canceled.
    # I'll point it to a placeholder I'll create now.
    "[cite:_1-147]": f"{base_url}/research_conversation_history.md"
}

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the lines in the citation map
for cite_tag, url in mappings.items():
    # Regex to replace the whole line for safety
    # Escape brackets
    safe_tag = cite_tag.replace('[', '\\[').replace(']', '\\]')
    # Pattern: [cite:TAG]: OLD_URL
    import re
    pattern = re.compile(rf'{safe_tag}:.*')
    
    if pattern.search(content):
        # formatted replacement
        replacement = f"{cite_tag}: {url}"
        content = pattern.sub(replacement, content)
        print(f"Updated {cite_tag}")
    else:
        print(f"Tag {cite_tag} not found in map.")
        # If not found, maybe append? But it should be there from previous generation.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Map updated.")
