let escolha = 1; // No desafio será: parseInt(gets());
let pokemon = "";

switch (escolha) {
  case 1:
    pokemon = "Bulbasaur";
    break;
  case 2:
    pokemon = "Charmander";
    break;
  case 4:
    pokemon = "Pikachu";
    break;
  case 5:
    pokemon = "Mewtwo";
    break;
}

if (escolha === 5) {
  console.log("Voce escolheu o Mewtwo como seu Pokemon inicial."); 
} else {
  console.log(`Voce escolheu o ${pokemon} como seu Pokemon inicial.`);
}