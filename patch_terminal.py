import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix terminal text color
content = content.replace('class="terminal p-4 h-64 overflow-y-auto text-sm"', 'class="terminal p-4 h-64 overflow-y-auto text-sm text-gray-300"')

# Add dates poll to terminal status
old_enquete = """<div class="col-span-2 mt-2 border-t border-gray-800 pt-2 text-gray-400 flex flex-col sm:flex-row sm:gap-4">
                        <span class="text-yellow-500">> ENQUETE:</span>
                        <span>[Kit Churrasco: <span id="sum-kit" class="text-white font-bold">0</span>]</span>
                        <span>[Rateio da Carne: <span id="sum-rateio" class="text-white font-bold">0</span>]</span>
                    </div>"""

new_enquete = """<div class="col-span-2 mt-2 border-t border-gray-800 pt-2 text-gray-400 flex flex-col sm:flex-row sm:gap-4">
                        <span class="text-yellow-500">> ENQUETE CHURRAS:</span>
                        <span>[Kit Churrasco: <span id="sum-kit" class="text-white font-bold">0</span>]</span>
                        <span>[Rateio da Carne: <span id="sum-rateio" class="text-white font-bold">0</span>]</span>
                    </div>
                    <div class="col-span-2 mt-1 text-gray-400 flex flex-col sm:flex-row sm:gap-4 sm:flex-wrap">
                        <span class="text-green-400">> DATAS:</span>
                        <span>[12/12: <span id="sum-d12" class="text-white font-bold">0</span>]</span>
                        <span>[13/12: <span id="sum-d13" class="text-white font-bold">0</span>]</span>
                        <span>[19/12: <span id="sum-d19" class="text-white font-bold">0</span>]</span>
                        <span>[20/12: <span id="sum-d20" class="text-white font-bold">0</span>]</span>
                        <span>[Qualquer: <span id="sum-any" class="text-white font-bold">0</span>]</span>
                    </div>"""

content = content.replace(old_enquete, new_enquete)

# Update JS to count dates
old_js_stats = "let stats = { titulares: 0, acompanhantes: 0, kit: 0, rateio: 0 };"
new_js_stats = "let stats = { titulares: 0, acompanhantes: 0, kit: 0, rateio: 0, d12: 0, d13: 0, d19: 0, d20: 0, any: 0 };"
content = content.replace(old_js_stats, new_js_stats)

old_js_loop = """if (item.poll && item.poll.includes('Rateio')) stats.rateio++;
                    }"""
new_js_loop = """if (item.poll && item.poll.includes('Rateio')) stats.rateio++;
                        
                        if (item.availability === '12/12') stats.d12++;
                        if (item.availability === '13/12') stats.d13++;
                        if (item.availability === '19/12') stats.d19++;
                        if (item.availability === '20/12') stats.d20++;
                        if (item.availability === 'Qualquer dia ta ótimo!') stats.any++;
                    }"""
content = content.replace(old_js_loop, new_js_loop)

old_js_update = """document.getElementById('sum-rateio').textContent = stats.rateio;"""
new_js_update = """document.getElementById('sum-rateio').textContent = stats.rateio;
                document.getElementById('sum-d12').textContent = stats.d12;
                document.getElementById('sum-d13').textContent = stats.d13;
                document.getElementById('sum-d19').textContent = stats.d19;
                document.getElementById('sum-d20').textContent = stats.d20;
                document.getElementById('sum-any').textContent = stats.any;"""
content = content.replace(old_js_update, new_js_update)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Terminal and stats updated!")
