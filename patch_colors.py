import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_grid = '<div class="grid grid-cols-2 text-xs font-mono gap-y-2">'
new_grid = '<div class="grid grid-cols-2 text-xs font-mono gap-y-2 text-gray-300">'

content = content.replace(old_grid, new_grid)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Colors updated!")
