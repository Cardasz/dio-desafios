// Desafios JavaScript na DIO têm funções "gets" e "print" acessíveis globalmente:
// - "gets" : lê UMA linha com dado(s) de entrada (inputs) do usuário;
// - "print": imprime um texto de saída (output), pulando linha.

class ItemMagico {
  constructor(tipo, dano, resistencia) {
    this.tipo = tipo;
    this.dano = dano;
    this.resistencia = resistencia;
  }

  calcularDano() {
    return this.tipo === 'arma' ? this.dano * 2 : this.dano;
  }
}

// (Valores simulados para teste local)
const tipoItem = "arma";         // No desafio será: gets();
const danoItem = 50;             // No desafio será: parseInt(gets());
const resistenciaItem = 100;     // No desafio será: parseInt(gets());

const itemPersonalizado = new ItemMagico(tipoItem, danoItem, resistenciaItem);

// Imprima os atributos do item personalizado (substituindo print por console.log)
console.log("Tipo: " + itemPersonalizado.tipo);
console.log("Dano: " + itemPersonalizado.dano);
console.log("Resistencia: " + itemPersonalizado.resistencia);

const danoTotal = itemPersonalizado.calcularDano();
console.log("Dano em combate: " + danoTotal);