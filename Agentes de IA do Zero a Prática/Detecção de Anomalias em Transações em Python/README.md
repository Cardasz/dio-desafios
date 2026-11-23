# Detecção de Fraude em Transações de Cartão de Crédito

Projeto de Machine Learning ponta a ponta voltado à detecção de transações fraudulentas em um cenário de **desbalanceamento extremo**, da exploração dos dados à explicabilidade individual das decisões com **SHAP**.

> **Dataset:** [Credit Card Fraud Detection (Google Storage / TensorFlow)](https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv) — carregado diretamente via URL no notebook (não versionado no repositório por ultrapassar o limite de 100 MB do GitHub).

---

## 1. O Problema e o Impacto do Desbalanceamento

A base reúne **284.807 transações reais** de cartão de crédito europeias ocorridas em dois dias, com 30 variáveis explicativas (`Time`, `Amount` e `V1` a `V28`, anonimizadas via PCA) e o alvo `Class` (`0` = normal, `1` = fraude).

Apenas **492 transações (0,1727%) são fraudes**. Nesse contexto, a **acurácia é uma métrica enganosa**: um modelo trivial que classifica todas as operações como normais alcança **99,83% de acurácia**, mas não captura nenhuma fraude.

Por isso, a avaliação foi concentrada na **classe positiva (fraude)** usando:

- **Recall:** fração das fraudes reais efetivamente detectadas (prioridade para reduzir prejuízo financeiro direto).
- **Precisão:** fração dos alertas emitidos que eram fraudes reais (controla o atrito com clientes legítimos).
- **F1-Score:** equilíbrio harmônico entre precisão e recall.
- **PR-AUC (Precision-Recall AUC):** muito mais sensível a falsos positivos do que a curva ROC em bases altamente desbalanceadas.

---

## 2. Preparação dos Dados

1. **Transformação de valor:** aplicação de `np.log1p(Amount)` para reduzir a forte assimetria à direita dos valores transacionados.
2. **Engenharia de atributos temporais:** criação de variáveis causais (`Hour`, `Time_Diff`, `Amount_Rolling_Mean_20` e `Amount_To_Rolling_Ratio`) para capturar ritmo de transações e desvios de valor em sequência sem introduzir vazamento de dados futuros.
3. **Divisão estratificada:** separação em 80% treino e 20% teste com `stratify=y`, preservando a proporção exata de 0,17% de fraudes em ambos os conjuntos.
4. **Prevenção de *Data Leakage*:** `StandardScaler` e técnicas de reamostragem (`RandomUnderSampler` e `SMOTE`) encapsulados dentro de `Pipeline` / `ImbPipeline`, garantindo que estatísticas de escala e amostras sintéticas sejam ajustadas apenas nos dados de treino.

---

## 3. Comparação entre Modelos (Classe de Fraude)

Resultados obtidos no conjunto de teste com limiar padrão (`0.5`):

| Modelo | Recall | Precisão | F1-Score | ROC-AUC | PR-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Regressão Logística (Baseline) | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` |
| Regressão Logística (Balanced) | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` |
| Random Forest (Balanced) | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` |
| XGBoost (`scale_pos_weight`) | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` |
| LightGBM (`is_unbalance`) | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` |
| XGBoost + RandomUnderSampler | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` |
| XGBoost + SMOTE | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` | `[0.XXXX]` |

> **Análise de Reamostragem:** o *RandomUnderSampler* eleva o recall, porém derruba a precisão drasticamente pelo descarte massivo de exemplos normais. O *SMOTE* e o ajuste de peso de classe (`scale_pos_weight`) mantiveram melhor equilíbrio entre recall e PR-AUC.

---

## 4. Limiar de Decisão e Explicabilidade com SHAP

### Ajuste de Hiperparâmetros e Limiar

Após otimizar o **XGBoost** via `GridSearchCV` com `StratifiedKFold` e métrica `recall`, comparamos os limiares `0.5` e `0.3`:

- **Limiar 0.5:** Recall = `[0.XXXX]` | Precisão = `[0.XXXX]` | Fraudes detectadas = `[XX/98]` | Falsos alarmes = `[XX]`
- **Limiar 0.3 (escolhido):** Recall = `[0.XXXX]` | Precisão = `[0.XXXX]` | Fraudes detectadas = `[XX/98]` | Falsos alarmes = `[XX]`

Reduzir o limiar para `0.3` permitiu capturar `[X]` fraudes adicionais a um custo controlado de falsos alarmes — trade-off justificável quando o custo de uma fraude não bloqueada supera o custo operacional de uma verificação preventiva.

### O que o SHAP Mostrou

- **Visão Global (Beeswarm):** as componentes `V14`, `V4`, `V12`, `V10` e `V17` (confirme a ordem exata no seu gráfico) concentraram o maior poder discriminativo. Valores muito negativos em `V14` e `V12` e valores elevados em `V4` empurram consistentemente a probabilidade para a classe de fraude.
- **Visão Local (Waterfall):** na transação fraudulenta inspecionada individualmente, o gráfico de cascata quantificou exatamente quanto cada variável somou à log-odds base até ultrapassar o limiar `0.3`, permitindo auditar o motivo do bloqueio.

---

## 5. O Que Foi Evoluído em Relação ao Caminho Base

- **Engenharia de atributos temporais:** inclusão de hora do dia, intervalo entre transações consecutivas e razão do valor atual frente à média móvel recente.
- **Comparação sistemática de reamostragem:** teste controlado de *RandomUnderSampler* vs. *SMOTE* dentro de `ImbPipeline` (sem vazamento na validação cruzada).
- **Ampliação de algoritmos:** adição do **LightGBM** à bateria de comparação e validação do **Random Forest em Pipeline** com ajuste de limiar.
- **Curva de trade-off de limiares:** visualização contínua de Precisão, Recall e F1 entre `0.05` e `0.95` para embasar a escolha de `0.3`.
- **Explicação local com SHAP Waterfall:** além da importância global, decomposição individual de uma fraude detectada.

---

## 6. Como Executar

1. Abra o arquivo `deteccao_fraude_cartao.ipynb` no [Google Colab](https://colab.research.google.com/drive/1k-QHKYG-Eet9qgKRD_dARJfN-8r9ZkaN?usp=sharing).
2. Execute **Ambiente de execução → Executar tudo**.
3. As bibliotecas extras são instaladas automaticamente na primeira célula e os dados são baixados direto da fonte oficial.
