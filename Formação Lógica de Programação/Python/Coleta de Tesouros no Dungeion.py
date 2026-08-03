total_salas = 8  # No desafio será: int(input())

# Utilizando EXATAMENTE as listas (arrays) fornecidas pela plataforma
salas_com_tesouro = [2, 4, 7]
salas_com_monstro = [3, 6, 8]

for sala in range(1, total_salas + 1):
    tem_tesouro = sala in salas_com_tesouro
    tem_monstro = sala in salas_com_monstro

    if tem_tesouro:
        print(f"Tesouro na sala {sala}!")
        
    if tem_monstro:
        print(f"Monstro na sala {sala}!")