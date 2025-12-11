
file_path = r'c:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method.md'
map_path = r'c:\Users\kryst\Workspace\Literature\Literature Testing\citation_map_block.md'

with open(map_path, 'r', encoding='utf-8') as f:
    map_content = f.read()

with open(file_path, 'a', encoding='utf-8') as f:
    f.write(map_content)

print("Appended citation map to kryssie-method.md")
