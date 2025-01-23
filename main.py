import os
import time
import shutil
from processador_gpt import processar_chatgtp_3_5_turbo
from processador_gemini import processar_gemini_1_5_flash
from processador_similaridade import calcular_similaridade
from datetime import datetime

# Defina os diretórios de entrada e saída
input_folder_ocr = "data/ocr"
input_folder_prompt = "data/prompt"
output_folder = f"data/output/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')[:-3]}"
prompt_filename = 'prompt-2.txt'

print('Iniciando script')

# Certifique-se de que a pasta de saída existe
if not os.path.exists(output_folder):
    print(f'Criando diretório {output_folder}')
    os.makedirs(output_folder)

# Inicialize o contador de arquivos processados
files_processed = 0
start_time = time.time()

# Lista para armazenar o resumo dos arquivos e similaridades
file_summary = []

with open(f'{input_folder_prompt}/{prompt_filename}', 'r', encoding='utf-8') as file:
    prompt = file.read()

output_prompt_path = os.path.join(output_folder, prompt_filename)
with open(output_prompt_path, 'w', encoding='utf-8') as prompt_file:
    prompt_file.write(prompt)

# Loop para processar cada arquivo na pasta de entrada
for filename in os.listdir(input_folder_ocr):
    if filename.endswith(".txt"):  # Supondo que os arquivos sejam .txt, ou modifique conforme necessário
        print('------------------------------------------')
        print(f'Iniciando processamento para {filename}')
        input_path = os.path.join(input_folder_ocr, filename)
        
        with open(input_path, 'r', encoding='utf-8') as file:
            ocr_text = file.read()

        # Processa GTP
        print(f'Processando GPT')
        resultado_gpt = processar_chatgtp_3_5_turbo(ocr_text, os.path.splitext(filename)[0], output_folder, prompt)

        # Processa Gemini
        print(f'Processando Gemini')
        resultado_gemini = processar_gemini_1_5_flash(ocr_text, os.path.splitext(filename)[0], output_folder, prompt)

        # Calcular a similaridade
        print(f'Calculando similaridade')
        similaridade = calcular_similaridade(resultado_gpt, resultado_gemini, True)
        similarity_output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_similarity.txt")        
        with open(similarity_output_path, 'w', encoding='utf-8') as similarity_file:
            similarity_file.write(f"A similaridade entre os documentos é: {similaridade}")
        
        print(f'Resultado da similaridade: {similaridade} para  {filename}')
        print(f'Fim do processamento para {filename}')
        print('------------------------------------------')
        print('')

        # Copiar o arquivo de entrada para a pasta de saída
        copied_file_path = os.path.join(output_folder, filename)
        shutil.copy(input_path, copied_file_path)
        print(f'Arquivo {filename} copiado para a pasta de saída.')

        # Incrementa o contador de arquivos processados
        files_processed += 1

        # Adiciona o arquivo e a similaridade ao resumo
        file_summary.append(f"{filename}: Similaridade = {similaridade:.4f}")

# Calcule o tempo total e a taxa média de processamento
end_time = time.time()
total_time = end_time - start_time
total_minutes = total_time / 60
average_time_per_file = total_time / files_processed if files_processed > 0 else 0

# Exibe o resumo do processamento
resumo = (
    f"Tempo total decorrido: {total_time:.2f} segundos\n"
    f"Tempo total decorrido: {total_minutes:.2f} minutos\n"
    f"Arquivos processados: {files_processed}\n"
    f"Taxa média de processamento: {average_time_per_file:.2f} segundos/arquivo\n"
)

# Adiciona os detalhes de cada arquivo no resumo
resumo += "\n".join(file_summary)

# Imprime no console
print(resumo)

timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')[:-3]

# Salva o resumo em um arquivo de texto
with open(os.path.join(output_folder, f"{timestamp}_resumo.txt"), 'w', encoding='utf-8') as resumo_file:
    resumo_file.write(resumo)
