# Desafios Python na DIO geralmente usam a função "input" para ler dados 
# e a função nativa "print" para imprimir a saída.

class ItemMagico:
    def __init__(self, tipo, dano, resistencia):
        self.tipo = tipo
        self.dano = dano
        self.resistencia = resistencia

    def calcular_dano(self):
        # [resultado_verdadeiro] if [condicao] else [resultado_falso]
        return self.dano * 2 if self.tipo == 'arma' else self.dano


tipo_item = "arma"          # No desafio será: input()
dano_item = 50              # No desafio será: int(input())
resistencia_item = 100      # No desafio será: int(input())

item_personalizado = ItemMagico(tipo_item, dano_item, resistencia_item)

print(f"Tipo: {item_personalizado.tipo}")
print(f"Dano: {item_personalizado.dano}")
print(f"Resistencia: {item_personalizado.resistencia}")

dano_total = item_personalizado.calcular_dano()
print(f"Dano em combate: {dano_total}")