// Desafios JavaScript na DIO têm funções "gets" e "print" acessíveis globalmente:
// - "gets" : lê UMA linha com dado(s) de entrada (inputs) do usuário;
// - "print": imprime um texto de saída (output), pulando linha.

// Definindo a função chamada "combinandoNomesPokemons"
function combinandoNomesPokemons(palavra) {
  let palavraPokemon = palavra + "saur";
  
  return palavraPokemon;
}

// Entrada da palavra (valor simulado para teste local)
var nomeEntrada = "Bulba"; // No desafio será: gets();

var palavraGerada = combinandoNomesPokemons(nomeEntrada);

// Exibindo a palavra gerada no terminal (substituindo o print() original):
console.log(palavraGerada);