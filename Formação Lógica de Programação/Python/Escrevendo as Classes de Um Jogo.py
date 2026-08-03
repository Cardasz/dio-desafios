class Heroi:
    def __init__(self, nome, idade, tipo):
        self.nome = nome
        self.idade = idade
        self.tipo = tipo

    def atacar(self):
        # Em Python, if/elif/else faz o papel do 'switch' tradicional
        tipo_formatado = self.tipo.lower()
        
        if tipo_formatado == "mago":
            ataque = "magia"
        elif tipo_formatado == "guerreiro":
            ataque = "espada"
        elif tipo_formatado == "monge":
            ataque = "artes marciais"
        elif tipo_formatado == "ninja":
            ataque = "shuriken"
        else:
            ataque = "um ataque misterioso"

        print(f"O {self.tipo} atacou usando {ataque}")

heroi1 = Heroi("Arthur", 30, "guerreiro")
heroi2 = Heroi("Merlin", 150, "mago")
heroi3 = Heroi("Shao Lin", 45, "monge")
heroi4 = Heroi("Hattori", 25, "ninja")

lista_de_herois = [heroi1, heroi2, heroi3, heroi4]

print("--- Batalha Iniciada ---\n")

for heroi in lista_de_herois:
    heroi.atacar()