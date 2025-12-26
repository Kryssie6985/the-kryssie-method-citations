
import os
import shutil

# Source: Literature Root
source_dir = r"C:\Users\kryst\Workspace\Literature"
# Destination: Citation Hub Sources
dest_dir = r"C:\Users\kryst\Workspace\Literature\the-kryssie-method-citations\sources"

# Files identified by strict filters (based on user request)
# 1. How to Talk to Gemini (Like Kryssie Does)
# 2. Interaction Kryssie Style (Vol 3, Part 4)
# 3. Chapter 3: The AI Teacher
# 4. Advanced Gemini Interaction

# We prefer .md versions if available, otherwise .docx or .pdf
# User said "Move them", so we will use shutil.move (but maybe copy first to be safe during test?)
# User said "don't copy them i'm limited on space please move them" -> OK, MOVE.

def normalize_filename(name):
    # standard clean
    name = name.lower()
    name = "".join([c for c in name if c.isalnum() or c in (' ', '_', '-', '.')])
    name = name.replace(' ', '_')
    return name

files_to_move = []

# Scan dir
for f in os.listdir(source_dir):
    full_path = os.path.join(source_dir, f)
    if not os.path.isfile(full_path): continue
    
    # Filter Logic
    is_target = False
    
    # "How to Talk to Gemini"
    if "how to talk to gemini" in f.lower():
        is_target = True
    
    # "Interaction Kryssie Style"
    elif "interaction kryssie style" in f.lower():
        is_target = True
        
    # "Advanced Gemini Interaction"
    elif "advanced gemini interaction" in f.lower():
        is_target = True
        
    # "Chapter 3" (The Novel? Or Chapter 3 AI Teacher?)
    # User said: "Chapter three is my novel... same place... sneak peek"
    # User also said: "Finalized Chapter 3_ The AI Teacher.docx.md" was seen earlier.
    # Wait, "Chapter 3: The AI Teacher" might be the novel chapter? "It's the only chapter we've wrote together".
    elif "chapter 3" in f.lower() and "ai teacher" in f.lower():
        is_target = True
        
    if is_target:
        # Prefer MD > DOCX > PDF if duplicates exist? 
        # For now, just identify all candidates.
        files_to_move.append(f)

print("Candidates to MOVE:")
for f in files_to_move:
    print(f"- {f}")

