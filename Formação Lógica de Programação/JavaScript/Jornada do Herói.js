// ==============================================================================
// NOTA SOBRE A ADAPTAÇÃO DO CÓDIGO PARA TESTES LOCAIS (NODE.JS)
// ==============================================================================
// Motivo da mudança: 
// Dentro da plataforma de desafios (como a DIO), o sistema 
// deles possui funções próprias chamadas gets() (para capturar os dados do teste) 
// e print() (para exibir o resultado final para o robô corretor).
//
// Solução para testar a lógica no computador:
// Substituímos as chamadas de gets() pela atribuição manual de valores diretos 
// nas variáveis (ex: const posicaoInicial = 2). Também trocamos o print() 
// pela função padrão do JavaScript para imprimir no terminal: o console.log().
// ==============================================================================

const posicaoInicial = parseInt(gets());
const totalPassos = parseInt(gets());

const posicaoFinal = posicaoInicial + totalPassos;


print(`Posicao final do heroi: ${posicaoFinal}`);