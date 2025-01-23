from sentence_transformers import SentenceTransformer, util

# Carregar o modelo pré-treinado
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Função para converter o documento estruturado em uma string textual
def document_to_text(doc):
    """
    Converte um documento estruturado (em formato JSON) para uma string textual.
    """
    itens = ', '.join([f"{item['Quantidade']}x {item['Nome']} a {item['Preco Unitario']} cada, totalizando {item['Valor Total']}" for item in doc['Itens']])

    return f"Documento: Número {doc['Documento']['Numero']}, Tipo {doc['Documento']['Tipo']}, Data de Emissão {doc['Documento']['Data de Emissao']}." \
           f" Fornecedor: Nome {doc['Fornecedor']['Nome']}, CNPJ {doc['Fornecedor']['CNPJ']}." \
           f" Itens: {itens}." \
           f" Totais: Valor Total {doc['Totais']['Valor Total']}, Impostos {doc['Totais']['Impostos']}." \
           f" Pagamento: Forma {doc['Pagamento']['Forma']}."

# Função para calcular a similaridade entre dois documentos
def calcular_similaridade(documento1, documento2, verificar_numeros_diferentes):
    """
    Calcula a similaridade entre dois documentos e retorna zero se houver diferença nos valores numéricos (quantidade, preço, valor total, impostos).
    """

    # Verificar se os documentos são dicionários
    if not isinstance(documento1, dict) or not isinstance(documento2, dict):
        return 0.0  # Se algum dos documentos não for um dicionário, retorna 0.0
    
    # Verificar se 'Itens' existe em ambos os documentos
    if 'Itens' not in documento1 or 'Itens' not in documento2:
        return 0.0  # Itens não estão no formato esperado
    
    # Verificar se algum valor numérico é diferente entre os documentos
    if verificar_numeros_diferentes and verificar_valores_numericos_diferentes(documento1, documento2):
        return 0.0

    # Verificar se algum valor numérico é diferente entre os documentos
    if verificar_numeros_diferentes & verificar_valores_numericos_diferentes(documento1, documento2):
        return 0.0    
    
    # Converter os documentos em texto
    texto_documento1 = document_to_text(documento1)
    texto_documento2 = document_to_text(documento2)

    # Gerar embeddings para os documentos
    embedding1 = model.encode(texto_documento1)
    embedding2 = model.encode(texto_documento2)

    # Calcular a similaridade entre os embeddings
    similaridade = util.pytorch_cos_sim(embedding1, embedding2)
    
    return similaridade.item()

# Função para verificar se valores numéricos em dois documentos são iguais
def verificar_valores_numericos_diferentes(doc1, doc2):
    """
    Verifica se algum valor numérico (quantidade, preço, valor total, impostos) é diferente entre dois documentos.
    """

    # Verificar todos os itens de "Itens" em ambos os documentos
    for item1, item2 in zip(doc1['Itens'], doc2['Itens']):
        if (item1['Quantidade'] != item2['Quantidade'] or
            item1['Preco Unitario'] != item2['Preco Unitario'] or
            item1['Valor Total'] != item2['Valor Total']):
            return True

    # Verificar os totais (valor total e impostos) dos documentos
    if (doc1['Totais']['Valor Total'] != doc2['Totais']['Valor Total'] or
        doc1['Totais']['Impostos'] != doc2['Totais']['Impostos']):
        return True

    return False