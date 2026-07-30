const listaDeJogadores = [
    { vitorias: 8, derrotas: 2 },
    { vitorias: 15, derrotas: 5 },
    { vitorias: 35, derrotas: 10 },
    { vitorias: 65, derrotas: 15 },
    { vitorias: 85, derrotas: 5 },
    { vitorias: 95, derrotas: 5 },
    { vitorias: 110, derrotas: 10 }
];

function calcularNivelRankeadas(vitorias, derrotas) {
    let saldoVitorias = vitorias - derrotas;
    let nivel = "";

    if (vitorias <= 10) {
        nivel = "Ferro";
    } else if (vitorias >= 11 && vitorias <= 20) {
        nivel = "Bronze";
    } else if (vitorias >= 21 && vitorias <= 50) {
        nivel = "Prata";
    } else if (vitorias >= 51 && vitorias <= 80) {
        nivel = "Ouro";
    } else if (vitorias >= 81 && vitorias <= 90) {
        nivel = "Diamante";
    } else if (vitorias >= 91 && vitorias <= 100) {
        nivel = "Lendário";
    } else if (vitorias >= 101) {
        nivel = "Imortal";
    }

    return `O Herói tem de saldo de ${saldoVitorias} vitórias e está no nível de ${nivel}`;
}

for (let i = 0; i < listaDeJogadores.length; i++) {
    let jogador = listaDeJogadores[i];
    
    let resultado = calcularNivelRankeadas(jogador.vitorias, jogador.derrotas);
    

    console.log(resultado);
}