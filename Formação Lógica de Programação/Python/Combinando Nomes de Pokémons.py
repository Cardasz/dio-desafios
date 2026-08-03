# Desafio Python: geralmente utilizam a função nativa "input" para leitura:
# - "input()": lê UMA linha com dado(s) de entrada do usuário;
# - "print()": imprime um texto de saída no terminal.

def combinando_nomes_pokemons(palavra):
    # Usando f-string para juntar a palavra recebida com "saur"
    palavra_pokemon = f"{palavra}saur"
    
    return palavra_pokemon

nome_entrada = "Bulba"  # No desafio será: input()

palavra_gerada = combinando_nomes_pokemons(nome_entrada)

print(palavra_gerada)