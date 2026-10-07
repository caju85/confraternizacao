import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

old_kit = "if (item.poll && item.poll.includes('Kit')) stats.kit++;"
new_kit = "if (item.poll && item.poll.includes('Kit')) stats.kit += (1 + parseInt(item.guests || 0));"
content = content.replace(old_kit, new_kit)

old_rateio = "if (item.poll && item.poll.includes('Rateio')) stats.rateio++;"
new_rateio = "if (item.poll && item.poll.includes('Rateio')) stats.rateio += (1 + parseInt(item.guests || 0));"
content = content.replace(old_rateio, new_rateio)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("BBQ Poll sum updated!")
