lista_de_jogadores = [
    { "vitorias": 8, "derrotas": 2 },
    { "vitorias": 15, "derrotas": 5 },
    { "vitorias": 35, "derrotas": 10 },
    { "vitorias": 65, "derrotas": 15 },
    { "vitorias": 85, "derrotas": 5 },
    { "vitorias": 95, "derrotas": 5 },
    { "vitorias": 110, "derrotas": 10 }
]

def calcular_nivel_rankeadas(vitorias, derrotas):
    saldo_vitorias = vitorias - derrotas
    nivel = ""

    if vitorias <= 10:
        nivel = "Ferro"
    elif 11 <= vitorias <= 20:
        nivel = "Bronze"
    elif 21 <= vitorias <= 50:
        nivel = "Prata"
    elif 51 <= vitorias <= 80:
        nivel = "Ouro"
    elif 81 <= vitorias <= 90:
        nivel = "Diamante"
    elif 91 <= vitorias <= 100:
        nivel = "Lendário"
    elif vitorias >= 101:
        nivel = "Imortal"

    return f"O Herói tem de saldo de {saldo_vitorias} vitórias e está no nível de {nivel}"

for jogador in lista_de_jogadores:
    resultado = calcular_nivel_rankeadas(jogador["vitorias"], jogador["derrotas"])
    print(resultado)