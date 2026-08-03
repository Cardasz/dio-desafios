herois = [
    { "nome": "Arthur", "xp": 850 },
    { "nome": "Lancelot", "xp": 1500 },
    { "nome": "Galahad", "xp": 4500 },
    { "nome": "Merlin", "xp": 6000 },
    { "nome": "Gawain", "xp": 7500 },
    { "nome": "Percival", "xp": 8500 },
    { "nome": "Bors", "xp": 9500 },
    { "nome": "Rei Pelicano", "xp": 15000 }
]

for heroi in herois:
    nome = heroi["nome"]
    xp = heroi["xp"]
    nivel = ""

    if xp <= 1000:
        nivel = "Ferro"
    elif 1001 <= xp <= 2000:
        nivel = "Bronze"
    elif 2001 <= xp <= 5000:
        nivel = "Prata"
    elif 5001 <= xp <= 7000:
        nivel = "Ouro"
    elif 7001 <= xp <= 8000:
        nivel = "Platina"
    elif 8001 <= xp <= 9000:
        nivel = "Ascendente"
    elif 9001 <= xp <= 10000:
        nivel = "Imortal"
    elif xp >= 10001:
        nivel = "Radiante"

    print(f"O Herói de nome **{nome}** está no nível de **{nivel}**")