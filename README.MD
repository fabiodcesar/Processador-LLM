# Projeto de Processamento de Arquivos OCR com Consultas de IA

Este projeto processa uma série de arquivos de texto extraídos de OCR, consulta os modelos de linguagem GPT e Gemini, calcula a similaridade entre as respostas obtidas e salva os resultados processados.

## Requisitos

- Python 3.11.0

## Instruções

1. **Preparar os arquivos de entrada:**
   - Coloque os arquivos de texto extraídos de OCR no diretório `data/ocr` em formato `.txt`.

2. **Instalar as dependências:**
   - Execute o seguinte comando para instalar as dependências necessárias:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configurar as chaves de API:**
   - Configure a chave de API do Gemini na variável de ambiente `GEMINI_API_KEY`.
   - Configure a chave de API do GPT na variável de ambiente `GTP_API_KEY`.

4. **Executar a aplicação:**
   - Rode o arquivo principal com o seguinte comando:
     ```bash
     python main.py
     ```

## Estrutura do Projeto

- `data/input`: Diretório onde devem ser colocados os arquivos de texto de entrada.
- `requirements.txt`: Arquivo com as dependências do projeto.
- `main.py`: Arquivo principal para execução do pipeline.

## Resultados

Os resultados processados serão armazenados em `data/output` de forma cumulativa.
