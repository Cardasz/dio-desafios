quantidade_golpes = 4  # No desafio será: int(input())

minerais = ["Carvao", "Ferro", "Diamante", "Pedra"]

for i in range(1, quantidade_golpes + 1):
    # len(minerais) retorna o tamanho da lista, equivalente ao .length do JS
    mina_index = (i - 1) % len(minerais)
    
    # Utilizando f-strings para formatar o texto impresso no console
    print(f"{i}: {minerais[mina_index]}")