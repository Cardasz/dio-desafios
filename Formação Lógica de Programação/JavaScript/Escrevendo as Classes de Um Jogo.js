class Heroi {
  constructor(nome, idade, tipo) {
    this.nome = nome; // Variável de escopo da classe
    this.idade = idade;
    this.tipo = tipo;
  }

  atacar() {
    // Variável local para armazenar o tipo de ataque
    let ataque = "";

    switch (this.tipo.toLowerCase()) {
      case "mago":
        ataque = "magia";
        break;
      case "guerreiro":
        ataque = "espada";
        break;
      case "monge":
        ataque = "artes marciais";
        break;
      case "ninja":
        ataque = "shuriken";
        break;
      default:
        ataque = "um ataque misterioso"; // Caso um tipo não mapeado seja inserido
    }

    console.log(`O ${this.tipo} atacou usando ${ataque}`);
  }
}

// Criando instâncias (Objetos) da classe Heroi
const heroi1 = new Heroi("Arthur", 30, "guerreiro");
const heroi2 = new Heroi("Merlin", 150, "mago");
const heroi3 = new Heroi("Shao Lin", 45, "monge");
const heroi4 = new Heroi("Hattori", 25, "ninja");

const listaDeHerois = [heroi1, heroi2, heroi3, heroi4];

console.log("--- Batalha Iniciada ---\n");

for (let i = 0; i < listaDeHerois.length; i++) {
  listaDeHerois[i].atacar();
}