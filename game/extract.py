import re

file_path = r'c:\Users\Alan\OneDrive\Desktop\Japitown\game\tl\english\script\characters\violet\quests\violet_quest_04.rpy'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
for i in range(len(lines)):
    if re.match(r'^\s+[a-z_]+ \"\"$', lines[i]):
        prev_line = lines[i-1].strip()
        if prev_line.startswith('#'):
            out.append(f'{i}: {prev_line}')

with open('scratch_extract.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print(f'Extracted {len(out)} lines.')
