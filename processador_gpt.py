import os
from openai import OpenAI
import json

def processar_chatgtp_3_5_turbo(ocr_text, filename, output_folder, prompt):
    
    """
    Processa o texto extraído via OCR e retorna um JSON estruturado.

    Args:
        ocr_text (str): Texto extraído via OCR.
    
    Returns:
        dict: JSON estruturado com os dados da nota fiscal.
        str: Mensagem de erro em caso de falha.
    """
    # Inicializa o cliente OpenAI
    client = OpenAI()
    try:
        prompt_final = prompt + ' ' +  ocr_text

        # Envia a solicitação para o modelo
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente de IA."},
                {"role": "user", "content": prompt_final}
            ],
            max_tokens=2048
        )  

        # Obtém a mensagem do modelo
        response_message = response.choices[0].message.content
        
        gpt_output_path = os.path.join(output_folder, f"{filename}_gtp_resultado.txt")
        with open(gpt_output_path, 'w', encoding='utf-8') as gpt_file:
            gpt_file.write(response.choices[0].message.content)

        # Remove delimitadores ```json ou similares
        if response_message.startswith("```json"):
            response_message = response_message[7:].strip()
        if response_message.endswith("```"):
            response_message = response_message[:-3].strip()

        # Tenta converter a resposta em JSON
        parsed_data = json.loads(response_message)
        return parsed_data  # Retorna o JSON como um dicionário

    except json.JSONDecodeError as e:
        return f"Erro ao processar o JSON: {e}"

    except Exception as e:
        return f"Erro ao acessar a API ou processar dados: {e}"

# # Exemplo de uso da função
# if __name__ == "__main__":
#     # Texto extraído via OCR (exemplo)
#     ocr_text = """
#     Nota Fiscal Eletrônica
#     Número: 12345
#     Data de Emissão: 2025-01-20
#     Fornecedor: Supermercado XYZ
#     CNPJ: 12.345.678/0001-99
#     Itens:
#     1. Arroz 5kg - Quantidade: 2 - Preço Unitário: 15.00 - Valor Total: 30.00
#     2. Feijão 1kg - Quantidade: 1 - Preço Unitário: 8.00 - Valor Total: 8.00
#     Forma de Pagamento: Cartão de Crédito
#     Valor Total: 38.00
#     Impostos: 2.00
#     """

#     # Chama a função
#     result = process_ocr_to_json(ocr_text)

#     # Imprime o resultado
#     if isinstance(result, dict):
#         print("JSON válido:", json.dumps(result, indent=2))
#     else:
#         print("Erro:", result)
