import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Substituir o corpo do form
form_content = """
                <!-- Nome -->
                <div>
                    <label for="name" class="block text-base font-bold text-red-700 mb-2">Nome Completo</label>
                    <input type="text" id="name" placeholder="Digite seu nome" required
                        class="w-full bg-gray-50 border-2 border-gray-200 rounded-xl px-4 py-3 text-gray-800 focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-200 transition-all font-medium">
                </div>

                <!-- Disponibilidade -->
                <div class="bg-gray-50 p-5 rounded-xl border-2 border-gray-100">
                    <label class="block text-base font-bold text-red-700 mb-3">Selecione sua disponibilidade</label>
                    <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                        <label class="cursor-pointer">
                            <input type="radio" name="availability" value="Nenhum dia" class="peer sr-only" required>
                            <div class="text-center bg-white border-2 border-gray-200 rounded-lg py-3 text-gray-600 peer-checked:bg-yellow-400 peer-checked:text-red-900 peer-checked:border-yellow-400 font-bold transition-all select-none text-sm">Nenhum dia</div>
                        </label>
                        <label class="cursor-pointer">
                            <input type="radio" name="availability" value="12/12" class="peer sr-only">
                            <div class="text-center bg-white border-2 border-gray-200 rounded-lg py-3 text-gray-600 peer-checked:bg-red-600 peer-checked:text-white peer-checked:border-red-600 font-bold transition-all select-none text-sm">12/12</div>
                        </label>
                        <label class="cursor-pointer">
                            <input type="radio" name="availability" value="13/12" class="peer sr-only">
                            <div class="text-center bg-white border-2 border-gray-200 rounded-lg py-3 text-gray-600 peer-checked:bg-red-600 peer-checked:text-white peer-checked:border-red-600 font-bold transition-all select-none text-sm">13/12</div>
                        </label>
                        <label class="cursor-pointer">
                            <input type="radio" name="availability" value="19/12" class="peer sr-only">
                            <div class="text-center bg-white border-2 border-gray-200 rounded-lg py-3 text-gray-600 peer-checked:bg-red-600 peer-checked:text-white peer-checked:border-red-600 font-bold transition-all select-none text-sm">19/12</div>
                        </label>
                        <label class="cursor-pointer">
                            <input type="radio" name="availability" value="20/12" class="peer sr-only">
                            <div class="text-center bg-white border-2 border-gray-200 rounded-lg py-3 text-gray-600 peer-checked:bg-red-600 peer-checked:text-white peer-checked:border-red-600 font-bold transition-all select-none text-sm">20/12</div>
                        </label>
                        <label class="cursor-pointer">
                            <input type="radio" name="availability" value="Qualquer dia ta ótimo!" class="peer sr-only">
                            <div class="text-center bg-white border-2 border-gray-200 rounded-lg py-3 text-gray-600 peer-checked:bg-green-600 peer-checked:text-white peer-checked:border-green-600 font-bold transition-all select-none text-sm">Qualquer dia ta ótimo!</div>
                        </label>
                    </div>
                </div>

                <!-- Acompanhantes -->
                <div class="bg-gray-50 p-5 rounded-xl border-2 border-gray-100">
                    <label class="block text-base font-bold text-red-700 mb-3">Quantidade de Acompanhantes</label>
                    <div class="grid grid-cols-5 gap-2 md:gap-3">
                        <label class="cursor-pointer">
                            <input type="radio" name="guests" value="0" class="peer sr-only" required>
                            <div class="text-center bg-white border-2 border-gray-200 rounded-lg py-3 text-gray-600 peer-checked:bg-red-600 peer-checked:text-white peer-checked:border-red-600 font-bold transition-all select-none">0</div>
                        </label>
                        <label class="cursor-pointer">
                            <input type="radio" name="guests" value="1" class="peer sr-only">
                            <div class="text-center bg-white border-2 border-gray-200 rounded-lg py-3 text-gray-600 peer-checked:bg-red-600 peer-checked:text-white peer-checked:border-red-600 font-bold transition-all select-none">1</div>
                        </label>
                        <label class="cursor-pointer">
                            <input type="radio" name="guests" value="2" class="peer sr-only">
                            <div class="text-center bg-white border-2 border-gray-200 rounded-lg py-3 text-gray-600 peer-checked:bg-red-600 peer-checked:text-white peer-checked:border-red-600 font-bold transition-all select-none">2</div>
                        </label>
                        <label class="cursor-pointer">
                            <input type="radio" name="guests" value="3" class="peer sr-only">
                            <div class="text-center bg-white border-2 border-gray-200 rounded-lg py-3 text-gray-600 peer-checked:bg-red-600 peer-checked:text-white peer-checked:border-red-600 font-bold transition-all select-none">3</div>
                        </label>
                        <!-- Opção divertida Família Dias (Vale 4) -->
                        <label class="cursor-pointer h-full">
                            <input type="radio" name="guests" value="4" class="peer sr-only">
                            <div class="text-center bg-white border-2 border-gray-200 rounded-lg py-1 h-full text-xs text-gray-600 peer-checked:bg-red-600 peer-checked:text-white peer-checked:border-red-600 font-bold transition-all flex flex-col items-center justify-center select-none">
                                <span>Família</span>
                                <span>Dias</span>
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Enquete do Churrasco -->
                <div class="bg-gray-50 p-5 rounded-xl border-2 border-gray-100">
                    <label class="block text-base font-bold text-red-700 mb-3">Enquete do Churrasco</label>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <label class="cursor-pointer flex-1">
                            <input type="radio" name="poll" value="Kit Churrasco" class="peer sr-only" required>
                            <div class="h-full p-4 bg-white border-2 border-gray-200 rounded-xl text-gray-600 peer-checked:bg-red-600 peer-checked:text-white peer-checked:border-red-600 font-bold transition-all flex flex-col items-center justify-center text-center select-none gap-2">
                                <span class="text-2xl">🥩</span>
                                <span class="text-sm">Contratar Kit Churrasco (Mais prático, todos pagam igual)</span>
                            </div>
                        </label>
                        <label class="cursor-pointer flex-1">
                            <input type="radio" name="poll" value="Rateio da Carne" class="peer sr-only">
                            <div class="h-full p-4 bg-white border-2 border-gray-200 rounded-xl text-gray-600 peer-checked:bg-red-600 peer-checked:text-white peer-checked:border-red-600 font-bold transition-all flex flex-col items-center justify-center text-center select-none gap-2">
                                <span class="text-2xl">🛒</span>
                                <span class="text-sm">Rateio da Carne (Compramos no mercado e dividimos)</span>
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Termos -->
                <div class="bg-yellow-50 p-4 rounded-xl border border-yellow-200">
                    <label class="flex items-start gap-3 cursor-pointer">
                        <input type="checkbox" id="terms" class="mt-1 w-5 h-5 text-red-600 border-gray-300 rounded focus:ring-red-500" required>
                        <span class="text-sm text-yellow-800">
                            <strong>Termo de Convivência:</strong> Concordo em não falar de política, religião ou trabalho durante a festa. Sujeito a multa em cerveja. 🍺
                        </span>
                    </label>
                </div>

                <div id="form-message" class="hidden"></div>
                
                <button type="submit" id="submit-btn" class="w-full bg-red-600 hover:bg-red-700 text-white font-black text-xl py-4 rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1">
                    Enviar Resposta
                </button>
"""

# Tentar encontrar a div <form id="rsvp-form" e substituir tudo dentro até antes do </form>
pattern = r'(<form id="rsvp-form" class="space-y-6">)(.*?)(</form>)'
new_html = re.sub(pattern, r'\1' + form_content + r'\3', content, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("HTML base do form atualizado.")
