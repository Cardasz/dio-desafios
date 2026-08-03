# ==============================================================================
# NOTA SOBRE A ADAPTAÇÃO DO CÓDIGO PARA TESTES LOCAIS (PYTHON)
# ==============================================================================
# Motivo da mudança: 
# Dentro da plataforma de desafios (como a DIO), o sistema 
# deles injeta os dados de teste através da entrada padrão, que lemos 
# usando a função nativa input().
#
# Solução para testar a lógica no computador:
# Você pode substituir as chamadas de input() pela atribuição manual de 
# valores diretos nas variáveis (ex: posicao_inicial = 2) durante os testes,
# e depois voltar para input() na hora de enviar o código. O Python já 
# utiliza print() nativamente para exibir o resultado.
# ==============================================================================

# No desafio da DIO, a leitura é feita com input()
posicao_inicial = int(input())
total_passos = int(input())

posicao_final = posicao_inicial + total_passos

# O Python possui a função print() nativa, e utilizamos f-strings para formatar
print(f"Posicao final do heroi: {posicao_final}")