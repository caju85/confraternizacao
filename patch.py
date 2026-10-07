import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Substituir o bloco script
new_script = """<script>
        // DOM Elements
        const form = document.getElementById('rsvp-form');
        const radiosAttending = document.querySelectorAll('input[name="attending"]');
        const dynamicFields = document.getElementById('dynamic-fields');
        const yesFields = document.getElementById('yes-fields');
        const nameInput = document.getElementById('name');
        const termsCheckbox = document.getElementById('terms');
        const formMessage = document.getElementById('form-message');
        const submitBtn = document.getElementById('submit-btn');
        const termLogs = document.getElementById('terminal-logs');
        const connectionStatus = document.getElementById('connection-status');

        radiosAttending.forEach(radio => {
            radio.addEventListener('change', (e) => {
                dynamicFields.classList.remove('hidden');
                hideMessage();
                
                if (e.target.value === 'yes') {
                    yesFields.classList.remove('hidden');
                    nameInput.required = true;
                    termsCheckbox.required = true;
                } else {
                    yesFields.classList.add('hidden');
                    nameInput.required = true;
                    termsCheckbox.required = false;
                    
                    // Limpa opções se mudar para 'Não'
                    const guestChecked = document.querySelector('input[name="guests"]:checked');
                    const pollChecked = document.querySelector('input[name="poll"]:checked');
                    if (guestChecked) guestChecked.checked = false;
                    if (pollChecked) pollChecked.checked = false;
                    termsCheckbox.checked = false;
                }
            });
        });

        // Utils de interface
        function showMessage(msg, type = 'error') {
            formMessage.textContent = msg;
            formMessage.classList.remove('hidden');
            formMessage.className = `p-4 rounded-xl text-sm font-bold text-center border-2 mb-4 ${
                type === 'error' 
                    ? 'bg-red-50 text-red-600 border-red-200' 
                    : 'bg-green-50 text-green-700 border-green-200'
            }`;
        }

        function hideMessage() {
            formMessage.classList.add('hidden');
        }

        async function fetchReservations() {
            try {
                const res = await fetch('/api/rsvp');
                if (!res.ok) throw new Error("Erro na API");
                const data = await res.json();
                
                termLogs.innerHTML = `<div class="text-gray-500">> Sincronizando tabela rsvp_list...</div>`;
                
                let stats = { titulares: 0, acompanhantes: 0, kit: 0, rateio: 0 };
                
                data.forEach(item => {
                    renderLogLine(item);
                    if (item.attending === 'yes') {
                        stats.titulares++;
                        stats.acompanhantes += parseInt(item.guests || 0);
                        if (item.poll && item.poll.includes('Kit')) stats.kit++;
                        if (item.poll && item.poll.includes('Rateio')) stats.rateio++;
                    }
                });

                updateSummary(stats);

                connectionStatus.innerHTML = `
                    <div class="w-2 h-2 rounded-full bg-green-500"></div>
                    <span class="text-xs text-green-500 font-mono">Online</span>
                `;
            } catch (error) {
                console.error("Fetch error:", error);
                connectionStatus.innerHTML = `
                    <div class="w-2 h-2 rounded-full bg-red-500"></div>
                    <span class="text-xs text-red-500 font-mono">Offline</span>
                `;
                termLogs.innerHTML += `<div class="text-red-500">> Falha na conexão com API.</div>`;
            }
        }

        function renderLogLine(data) {
            const div = document.createElement('div');
            const safeName = (data.name || 'Anônimo').replace(/"/g, "'");

            if (data.attending === 'yes') {
                let guestLabel = data.guests == 4 ? "'Familia Dias'" : data.guests;
                let pollLabel = (data.poll || '').includes('Kit') ? "'Kit'" : "'Rateio'";
                
                div.innerHTML = `> <span class="text-blue-400">INSERT INTO</span> rsvp (nome, status, convidados, enquete) <span class="text-blue-400">VALUES</span> ("<span class="text-white">${safeName}</span>", <span class="text-yellow-400">"CONFIRMADO"</span>, <span class="text-white">${guestLabel}</span>, <span class="text-white">${pollLabel}</span>); <span class="text-gray-500">// OK</span>`;
            } else {
                div.innerHTML = `> <span class="text-blue-400">INSERT INTO</span> rsvp (nome, status) <span class="text-blue-400">VALUES</span> ("<span class="text-white">${safeName}</span>", <span class="text-red-500">"AUSENTE"</span>); <span class="text-gray-500">// OK</span>`;
            }

            termLogs.appendChild(div);
            termLogs.scrollTop = termLogs.scrollHeight;
        }

        function updateSummary(stats) {
            document.getElementById('sum-users').textContent = stats.titulares;
            document.getElementById('sum-guests').textContent = stats.acompanhantes;
            document.getElementById('sum-total').textContent = stats.titulares + stats.acompanhantes;
            document.getElementById('sum-kit').textContent = stats.kit;
            document.getElementById('sum-rateio').textContent = stats.rateio;
        }

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideMessage();
            
            const attendingRadio = document.querySelector('input[name="attending"]:checked');
            if (!attendingRadio) return;
            
            const attending = attendingRadio.value;
            const name = nameInput.value.trim();
            
            if (!name) { showMessage("Por favor, digite seu Nome Completo."); return; }

            let guests = 0;
            let poll = '';

            if (attending === 'yes') {
                const guestRadio = document.querySelector('input[name="guests"]:checked');
                const pollRadio = document.querySelector('input[name="poll"]:checked');

                if (!guestRadio) { showMessage("Selecione a quantidade de acompanhantes."); return; }
                if (!pollRadio) { showMessage("Responda à Enquete do Churrasco."); return; }
                if (!termsCheckbox.checked) { showMessage("Você deve concordar com o Termo de Convivência."); return; }

                guests = parseInt(guestRadio.value);
                poll = pollRadio.value;
            }

            submitBtn.disabled = true;
            submitBtn.textContent = 'Processando...';

            try {
                const response = await fetch('/api/rsvp', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, attending, guests, poll })
                });

                if (!response.ok) throw new Error("Erro ao salvar");

                showMessage("Registro efetuado com sucesso! Verifique o terminal abaixo.", "success");
                
                // Recarregar os dados
                await fetchReservations();
                
                setTimeout(() => {
                    form.reset();
                    dynamicFields.classList.add('hidden');
                    yesFields.classList.add('hidden');
                    hideMessage();
                }, 3000);

            } catch (error) {
                console.error("Save error:", error);
                showMessage("Falha na gravação. Tente novamente.", "error");
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Enviar Resposta';
            }
        });

        function createConfetti() {
            const container = document.getElementById('confetti-container');
            const colors = ['bg-red-600', 'bg-yellow-400', 'bg-white', 'bg-red-400']; 
            
            setInterval(() => {
                const conf = document.createElement('div');
                const colorClass = colors[Math.floor(Math.random() * colors.length)];
                
                conf.className = `confetti ${colorClass} shadow-sm`;
                conf.style.left = Math.random() * 100 + 'vw';
                
                const duration = Math.random() * 3 + 3; // 3s a 6s
                conf.style.animationDuration = duration + 's';
                
                container.appendChild(conf);
                
                setTimeout(() => {
                    if (conf.parentNode) conf.parentNode.removeChild(conf);
                }, duration * 1000);
            }, 300); // Confetes a cada 300ms
        }

        // Inicializar
        window.onload = () => {
            createConfetti();
            fetchReservations();
            // Atualizar os dados a cada 10 segundos
            setInterval(fetchReservations, 10000);
        };
    </script>"""

new_content = re.sub(r'<script type="module">.*?</script>', new_script, content, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Patch aplicado com sucesso!")
