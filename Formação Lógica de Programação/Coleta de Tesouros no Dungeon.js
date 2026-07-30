const totalSalas = 8; // No desafio será: parseInt(gets());

// Utilizando EXATAMENTE os arrays fornecidos pela plataforma
const salasComTesouro = [2, 4, 7];
const salasComMonstro = [3, 6, 8];

for (let sala = 1; sala <= totalSalas; sala++) {
    const temTesouro = salasComTesouro.includes(sala);
    const temMonstro = salasComMonstro.includes(sala);

    if (temTesouro) {
        console.log("Tesouro na sala " + sala + "!");
    } 
    
    if (temMonstro) {
        console.log("Monstro na sala " + sala + "!");
    }
}