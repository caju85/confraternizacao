import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Title and Header
content = content.replace("<title>Confirmação - Confraternização SAC TI</title>", "<title>Confirmação - Confraternização SAC & Amigos</title>")
content = content.replace("🔥 Confra SAC TI", "🔥 Confraternização SAC & Amigos")

# 2. Update JS loop to add 1 + guests
old_d12 = "if (item.availability === '12/12') stats.d12++;"
new_d12 = "if (item.availability === '12/12') stats.d12 += (1 + parseInt(item.guests || 0));"
content = content.replace(old_d12, new_d12)

old_d13 = "if (item.availability === '13/12') stats.d13++;"
new_d13 = "if (item.availability === '13/12') stats.d13 += (1 + parseInt(item.guests || 0));"
content = content.replace(old_d13, new_d13)

old_d19 = "if (item.availability === '19/12') stats.d19++;"
new_d19 = "if (item.availability === '19/12') stats.d19 += (1 + parseInt(item.guests || 0));"
content = content.replace(old_d19, new_d19)

old_d20 = "if (item.availability === '20/12') stats.d20++;"
new_d20 = "if (item.availability === '20/12') stats.d20 += (1 + parseInt(item.guests || 0));"
content = content.replace(old_d20, new_d20)

old_any = "if (item.availability === 'Qualquer dia ta ótimo!') stats.any++;"
new_any = "if (item.availability === 'Qualquer dia ta ótimo!') stats.any += (1 + parseInt(item.guests || 0));"
content = content.replace(old_any, new_any)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Title and JS updated!")
