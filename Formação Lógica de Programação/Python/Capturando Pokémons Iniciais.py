escolha = 1  # No desafio será: int(input())
pokemon = ""

if escolha == 1:
    pokemon = "Bulbasaur"
elif escolha == 2:
    pokemon = "Charmander"
elif escolha == 4:
    pokemon = "Pikachu"
elif escolha == 5:
    pokemon = "Mewtwo"

if escolha == 5:
    print("Voce escolheu o Mewtwo como seu Pokemon inicial.")
else:
    print(f"Voce escolheu o {pokemon} como seu Pokemon inicial.")