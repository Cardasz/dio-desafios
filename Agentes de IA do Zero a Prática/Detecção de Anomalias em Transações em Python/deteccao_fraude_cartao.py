# %% [markdown]
# # Detecção de Fraude em Transações de Cartão de Crédito
# Projeto completo: exploração, preparação, modelagem com dados desbalanceados,
# comparação de reamostragem, ajuste de hiperparâmetros/limiar e explicabilidade com SHAP.

# %%
# 0. Instalação automática de dependências e imports
import subprocess
import sys
import warnings

warnings.filterwarnings("ignore")

pacotes = {
    "imblearn": "imbalanced-learn",
    "shap": "shap",
    "xgboost": "xgboost",
    "lightgbm": "lightgbm",
}
for modulo, pacote in pacotes.items():
    try:
        __import__(modulo)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pacote])

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    from IPython.display import display
except ImportError:
    display = print

from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_auc_score,
    average_precision_score,
    precision_recall_curve,
    roc_curve,
    precision_score,
    recall_score,
    f1_score,
)

from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import shap

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)
RANDOM_STATE = 42


# %%
# 1. EXPLORAÇÃO DOS DADOS
URL = "https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv"
df = pd.read_csv(URL)

print("=" * 70)
print("1. EXPLORAÇÃO INICIAL")
print("=" * 70)
print(f"Dimensões da base: {df.shape[0]:,} linhas x {df.shape[1]} colunas")
print(f"Valores nulos: {df.isnull().sum().sum()}")
display(df.head())

prop = df["Class"].value_counts(normalize=True) * 100
contagem = df["Class"].value_counts()

resumo_classes = pd.DataFrame({
    "Quantidade": contagem,
    "Proporção (%)": prop.round(4),
})
resumo_classes.index = ["Normal (0)", "Fraude (1)"]
display(resumo_classes)

# Visualização do desbalanceamento e distribuição de valores
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.countplot(
    data=df,
    x="Class",
    hue="Class",
    legend=False,
    palette={0: "#2E86AB", 1: "#D90429"},
    ax=axes[0],
)
axes[0].set_yscale("log")
axes[0].set_title("Distribuição de Transações (Escala Log)")
axes[0].set_xticks([0, 1])
axes[0].set_xticklabels(["Normal (0)", "Fraude (1)"])
axes[0].set_ylabel("Contagem (log)")

sns.boxplot(
    data=df.assign(Amount_Log=np.log1p(df["Amount"])),
    x="Class",
    y="Amount_Log",
    hue="Class",
    legend=False,
    palette={0: "#2E86AB", 1: "#D90429"},
    ax=axes[1],
)
axes[1].set_title("Distribuição de log(1 + Amount) por Classe")
axes[1].set_xticks([0, 1])
axes[1].set_xticklabels(["Normal (0)", "Fraude (1)"])
axes[1].set_ylabel("log1p(Amount)")

plt.tight_layout()
plt.show()

print("\nResumo estatístico de Amount por classe:")
display(df.groupby("Class")["Amount"].describe().round(2))


# %%
# 2. PREPARAÇÃO DOS DADOS E ENGENHARIA DE ATRIBUTOS TEMPORAIS
print("\n" + "=" * 70)
print("2. PREPARAÇÃO DOS DADOS")
print("=" * 70)

# Garante ordem cronológica antes de calcular atributos sequenciais
df_prep = df.sort_values("Time").reset_index(drop=True)

# Log do valor para reduzir assimetria
df_prep["Amount_Log"] = np.log1p(df_prep["Amount"])

# Variáveis comportamentais ao longo do tempo (estritamente causais)
df_prep["Hour"] = (df_prep["Time"] / 3600.0) % 24.0
df_prep["Time_Diff"] = df_prep["Time"].diff().fillna(0)
df_prep["Amount_Rolling_Mean_20"] = (
    df_prep["Amount"].rolling(window=20, min_periods=1).mean()
)
df_prep["Amount_To_Rolling_Ratio"] = (
    df_prep["Amount"] / (df_prep["Amount_Rolling_Mean_20"] + 1e-5)
)

X = df_prep.drop(columns=["Class", "Amount"])
y = df_prep["Class"]

# Separação estratificada mantendo a proporção de fraudes (~0,17%)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=RANDOM_STATE,
)

print(f"Treino: {X_train.shape[0]:,} linhas | Fraudes: {y_train.sum()} ({y_train.mean()*100:.4f}%)")
print(f"Teste:  {X_test.shape[0]:,} linhas | Fraudes: {y_test.sum()} ({y_test.mean()*100:.4f}%)")


# %%
# 3. TREINAMENTO E COMPARAÇÃO DE MODELOS (BASELINE, BALANCED, RF, XGBOOST, LIGHTGBM)
print("\n" + "=" * 70)
print("3. TREINAMENTO E COMPARAÇÃO DE MODELOS")
print("=" * 70)


def avaliar_modelo(nome, modelo, X_tr, y_tr, X_te, y_te, threshold=0.5):
    modelo.fit(X_tr, y_tr)
    y_prob = modelo.predict_proba(X_te)[:, 1]
    y_pred = (y_prob >= threshold).astype(int)

    metricas = {
        "Modelo": nome,
        "Threshold": threshold,
        "Recall (Fraude)": recall_score(y_te, y_pred),
        "Precisão (Fraude)": precision_score(y_te, y_pred, zero_division=0),
        "F1-Score (Fraude)": f1_score(y_te, y_pred, zero_division=0),
        "ROC-AUC": roc_auc_score(y_te, y_prob),
        "PR-AUC": average_precision_score(y_te, y_prob),
    }
    return modelo, y_prob, y_pred, metricas


scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
print(f"Fator scale_pos_weight calculado no treino: {scale_pos_weight:.2f}\n")

modelos = {
    "Regressão Logística (Baseline)": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
    ]),
    "Regressão Logística (Balanced)": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=RANDOM_STATE,
        )),
    ]),
    "Random Forest (Balanced)": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            class_weight="balanced",
            n_jobs=-1,
            random_state=RANDOM_STATE,
        )),
    ]),
    "XGBoost (scale_pos_weight)": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", XGBClassifier(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            scale_pos_weight=scale_pos_weight,
            base_score=0.5,
            tree_method="hist",
            eval_metric="aucpr",
            n_jobs=-1,
            random_state=RANDOM_STATE,
        )),
    ]),
    "LightGBM (is_unbalance)": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LGBMClassifier(
            n_estimators=200,
            learning_rate=0.05,
            is_unbalance=True,
            n_jobs=-1,
            random_state=RANDOM_STATE,
            verbose=-1,
        )),
    ]),
}

resultados = []
probabilidades = {}
modelos_treinados = {}

for nome, pipe in modelos.items():
    modelo_fit, y_prob, y_pred, metrica = avaliar_modelo(
        nome, pipe, X_train, y_train, X_test, y_test
    )
    resultados.append(metrica)
    probabilidades[nome] = y_prob
    modelos_treinados[nome] = modelo_fit
    print(f"--- {nome} ---")
    print(classification_report(y_test, y_pred, target_names=["Normal", "Fraude"], digits=4))


# %%
# 4. EVOLUÇÃO: COMPARAÇÃO ENTRE UNDERSAMPLING E OVERSAMPLING (SMOTE)
print("\n" + "=" * 70)
print("4. REAMOSTRAGEM: UNDERSAMPLING VS OVERSAMPLING (SMOTE)")
print("=" * 70)

estrategias_rebalanceamento = {
    "XGBoost + RandomUnderSampler": ImbPipeline([
        ("scaler", StandardScaler()),
        ("under", RandomUnderSampler(random_state=RANDOM_STATE)),
        ("clf", XGBClassifier(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            base_score=0.5,
            tree_method="hist",
            eval_metric="aucpr",
            n_jobs=-1,
            random_state=RANDOM_STATE,
        )),
    ]),
    "XGBoost + SMOTE (Oversampling)": ImbPipeline([
        ("scaler", StandardScaler()),
        ("smote", SMOTE(random_state=RANDOM_STATE)),
        ("clf", XGBClassifier(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            base_score=0.5,
            tree_method="hist",
            eval_metric="aucpr",
            n_jobs=-1,
            random_state=RANDOM_STATE,
        )),
    ]),
}

resultados_resample = []
for nome, pipe in estrategias_rebalanceamento.items():
    modelo_fit, y_prob, y_pred, metrica = avaliar_modelo(
        nome, pipe, X_train, y_train, X_test, y_test
    )
    resultados_resample.append(metrica)
    probabilidades[nome] = y_prob
    modelos_treinados[nome] = modelo_fit
    print(f"--- {nome} ---")
    print(classification_report(y_test, y_pred, target_names=["Normal", "Fraude"], digits=4))

df_comparacao_geral = (
    pd.concat([pd.DataFrame(resultados), pd.DataFrame(resultados_resample)], ignore_index=True)
    .sort_values(by="Recall (Fraude)", ascending=False)
    .reset_index(drop=True)
)

print("\nTabela Comparativa Geral (ordenada por Recall na classe Fraude):")
display(df_comparacao_geral.round(4))


# %%
# 5. CURVA ROC E CURVA PRECISION-RECALL
print("\n" + "=" * 70)
print("5. CURVAS ROC E PRECISION-RECALL")
print("=" * 70)

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

for nome, y_prob in probabilidades.items():
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = roc_auc_score(y_test, y_prob)
    axes[0].plot(fpr, tpr, label=f"{nome} (AUC={roc_auc:.4f})")

    prec, rec, _ = precision_recall_curve(y_test, y_prob)
    pr_auc = average_precision_score(y_test, y_prob)
    axes[1].plot(rec, prec, label=f"{nome} (PR-AUC={pr_auc:.4f})")

axes[0].plot([0, 1], [0, 1], "k--", alpha=0.5)
axes[0].set_title("Curva ROC")
axes[0].set_xlabel("Taxa de Falsos Positivos (FPR)")
axes[0].set_ylabel("Recall (TPR)")
axes[0].legend(fontsize=8, loc="lower right")

baseline_pr = y_test.mean()
axes[1].axhline(
    baseline_pr,
    color="k",
    linestyle="--",
    alpha=0.5,
    label=f"Baseline ({baseline_pr:.4f})",
)
axes[1].set_title("Curva Precision-Recall (Foco em Fraude)")
axes[1].set_xlabel("Recall")
axes[1].set_ylabel("Precisão")
axes[1].legend(fontsize=8, loc="lower left")

plt.tight_layout()
plt.show()


# %%
# 6. AJUSTE DE HIPERPARÂMETROS (GRIDSEARCHCV POR RECALL) E LIMIAR (0.5 vs 0.3)
print("\n" + "=" * 70)
print("6. PIPELINE, GRIDSEARCHCV (RECALL) E AJUSTE DE LIMIAR")
print("=" * 70)

pipe_xgb = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", XGBClassifier(
        base_score=0.5,
        tree_method="hist",
        eval_metric="aucpr",
        n_jobs=-1,
        random_state=RANDOM_STATE,
    )),
])

param_grid = {
    "clf__n_estimators": [150, 250],
    "clf__max_depth": [3, 5],
    "clf__learning_rate": [0.05, 0.1],
    "clf__scale_pos_weight": [scale_pos_weight, scale_pos_weight * 1.5],
}

cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=RANDOM_STATE)

grid_search = GridSearchCV(
    estimator=pipe_xgb,
    param_grid=param_grid,
    scoring="recall",
    cv=cv,
    n_jobs=-1,
    verbose=1,
)

grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

print("\nMelhores hiperparâmetros (Recall CV):", grid_search.best_params_)
print(f"Melhor Recall médio na validação cruzada: {grid_search.best_score_:.4f}\n")

# Comparação de limiares 0.5 vs 0.3 no XGBoost Otimizado e no Random Forest em Pipeline
rf_pipeline = modelos_treinados["Random Forest (Balanced)"]

comparacao_limiares = []
for nome_mod, mod in [
    ("XGBoost Otimizado (Pipeline)", best_model),
    ("Random Forest (Pipeline)", rf_pipeline),
]:
    probs = mod.predict_proba(X_test)[:, 1]
    for limiar in [0.5, 0.3]:
        preds = (probs >= limiar).astype(int)
        comparacao_limiares.append({
            "Modelo": nome_mod,
            "Limiar": limiar,
            "Recall": recall_score(y_test, preds),
            "Precisão": precision_score(y_test, preds, zero_division=0),
            "F1-Score": f1_score(y_test, preds, zero_division=0),
            "Fraudes Detectadas (TP)": int(((preds == 1) & (y_test == 1)).sum()),
            "Fraudes Perdidas (FN)": int(((preds == 0) & (y_test == 1)).sum()),
            "Falsos Alarmes (FP)": int(((preds == 1) & (y_test == 0)).sum()),
        })

df_limiares = pd.DataFrame(comparacao_limiares)
display(df_limiares.round(4))

# Curva de trade-off de limiares no modelo otimizado
y_prob_final = best_model.predict_proba(X_test)[:, 1]

limiares = np.linspace(0.05, 0.95, 37)
recalls, precisions, f1s = [], [], []

for t in limiares:
    preds_t = (y_prob_final >= t).astype(int)
    recalls.append(recall_score(y_test, preds_t))
    precisions.append(precision_score(y_test, preds_t, zero_division=0))
    f1s.append(f1_score(y_test, preds_t, zero_division=0))

plt.figure(figsize=(10, 5))
plt.plot(limiares, recalls, label="Recall", linewidth=2)
plt.plot(limiares, precisions, label="Precisão", linewidth=2)
plt.plot(limiares, f1s, label="F1-Score", linewidth=2, linestyle="--")
plt.axvline(0.3, color="red", linestyle=":", label="Limiar Escolhido (0.3)")
plt.axvline(0.5, color="gray", linestyle=":", label="Limiar Padrão (0.5)")
plt.title("Trade-off entre Precisão, Recall e F1 por Limiar de Decisão (XGBoost Otimizado)")
plt.xlabel("Limiar de Probabilidade")
plt.ylabel("Pontuação")
plt.legend()
plt.show()

# Matrizes de confusão lado a lado: 0.5 vs 0.3
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, limiar in zip(axes, [0.5, 0.3]):
    cm = confusion_matrix(y_test, (y_prob_final >= limiar).astype(int))
    ConfusionMatrixDisplay(cm, display_labels=["Normal", "Fraude"]).plot(
        ax=ax, cmap="Blues", colorbar=False
    )
    ax.set_title(f"Matriz de Confusão — XGBoost (Limiar = {limiar})")

plt.tight_layout()
plt.show()


# %%
# 7. IMPORTÂNCIA DAS VARIÁVEIS E EXPLICABILIDADE COM SHAP
print("\n" + "=" * 70)
print("7. EXPLICABILIDADE: FEATURE IMPORTANCE E SHAP")
print("=" * 70)

xgb_clf = best_model.named_steps["clf"]
scaler = best_model.named_steps["scaler"]

# Importância nativa das variáveis (XGBoost)
importancias = pd.Series(
    xgb_clf.feature_importances_, index=X.columns
).sort_values(ascending=False)

plt.figure(figsize=(10, 6))
importancias.head(15).sort_values().plot(kind="barh", color="#1D3557")
plt.title("Top 15 Variáveis Mais Importantes (XGBoost)")
plt.xlabel("Importância")
plt.tight_layout()
plt.show()

# Amostra estratificada para SHAP: todas as fraudes do teste + 1.000 transações normais
idx_fraudes = y_test[y_test == 1].index
idx_normais = y_test[y_test == 0].sample(n=1000, random_state=RANDOM_STATE).index
idx_amostra = idx_fraudes.union(idx_normais)

X_shap_scaled = pd.DataFrame(
    scaler.transform(X_test.loc[idx_amostra]),
    columns=X.columns,
    index=idx_amostra,
)

# Calcula valores SHAP com fallback automático para compatibilidade entre versões
try:
    explainer = shap.TreeExplainer(xgb_clf)
    shap_values = explainer(X_shap_scaled)
except Exception:
    background = X_shap_scaled.sample(n=100, random_state=RANDOM_STATE)
    explainer = shap.Explainer(lambda data: xgb_clf.predict_proba(data)[:, 1], background)
    shap_values = explainer(X_shap_scaled)

if len(shap_values.shape) == 3:
    shap_values = shap_values[:, :, 1]

# Explicação Global (Beeswarm)
print("Impacto global das variáveis nas predições de fraude (SHAP Beeswarm):")
shap.plots.beeswarm(shap_values, max_display=15)

# Explicação Local (Waterfall) de uma fraude real detectada
y_prob_amostra = best_model.predict_proba(X_test.loc[idx_amostra])[:, 1]
y_true_amostra = y_test.loc[idx_amostra].values
fraudes_detectadas = np.where((y_true_amostra == 1) & (y_prob_amostra >= 0.3))[0]

if len(fraudes_detectadas) > 0:
    idx_exemplo = fraudes_detectadas[0]
else:
    idx_exemplo = int(np.argmax(y_prob_amostra * (y_true_amostra == 1)))

print(
    f"\nExplicação local (SHAP Waterfall) — Fraude real | "
    f"Probabilidade prevista: {y_prob_amostra[idx_exemplo]:.4f}"
)
shap.plots.waterfall(shap_values[idx_exemplo], max_display=12)

print("\nExecução finalizada com sucesso!")