import pandas as pd
import streamlit as st

# === Carrega os dados exportados ===
arquivo = "emissoes_resultado.xlsx"  # caminho relativo para funcionar no Streamlit Cloud
df_mensal = pd.read_excel(arquivo, sheet_name="Mensal")
df_anual = pd.read_excel(arquivo, sheet_name="Anual")

# === Configuração da página ===
st.set_page_config(page_title="Dashboard de Emissões", layout="wide")
st.title("Dashboard da Iniciativa Carbono Aberto")

# === KPIs ===
col1, col2 = st.columns(2)

with col1:
    receita_brl = df_anual[df_anual["Ano"] == "Receita (BRL)"]["Emission Reductions (tCO2e)"].values[0]
    st.metric("💰 Receita total com Créditos de Carbono (BRL)", f"R$ {receita_brl:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

with col2:
    receita_usd = df_anual[df_anual["Ano"] == "Receita (USD)"]["Emission Reductions (tCO2e)"].values[0]
    st.metric("💰 Receita total com Créditos de Carbono (USD)", f"US$ {receita_usd:,.2f}")

# === Gráfico de Emissões Mensais ===
st.subheader("Emissões Evitadas em tCO2e por mês, sem decaimento")
df_mensal_plot = df_mensal.copy()
df_mensal_plot["Mes"] = df_mensal_plot["Mes"].astype(str).str.zfill(2)
df_mensal_plot["AnoMes"] = df_mensal_plot["Ano"].astype(str) + "-" + df_mensal_plot["Mes"]
df_mensal_plot = df_mensal_plot.sort_values("AnoMes")
st.line_chart(df_mensal_plot.set_index("AnoMes")["Emission Reductions (tCO2e)"])

# === Gráfico de Emissões Anuais ===
#st.subheader("Emissões Evitadas em tCO2e por Ano, com decaimento")
#df_anual_plot = df_anual[df_anual["Ano"].apply(lambda x: str(x).isdigit())]
#df_anual_plot = df_anual_plot.sort_values("Ano")
#st.bar_chart(df_anual_plot.set_index("Ano")["Emission Reductions (tCO2e)"])
##

# === Gráfico de Emissões Anuais ===
st.subheader("Emissões Evitadas em tCO2e por Ano, com decaimento")

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Filtra e ordena os dados
df_anual_plot = df_anual[df_anual["Ano"].apply(lambda x: str(x).isdigit())]
df_anual_plot = df_anual_plot.sort_values("Ano")

# Configurações do gráfico
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(
    df_anual_plot["Ano"].astype(str),  # Converte anos para string
    df_anual_plot["Emission Reductions (tCO2e)"],
    color='#1f77b4'
)

# Formata o eixo Y para o padrão brasileiro (pontos para milhares)
ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: f'{x:,.0f}'.replace(',', '.'))
)

# Rótulos e título
plt.xlabel("Ano")
plt.ylabel("Emissões Evitadas (tCO₂e)")
plt.title("Emissões Evitadas por Ano")
plt.xticks(rotation=45)  # Rotaciona os anos para melhor legibilidade

# Exibe o gráfico no Streamlit
st.pyplot(fig)

##
# === Fonte de dados ===
st.caption("Dados baseados em emissões de resíduos de poda destinados à compostagem (2019-2022), extraídos de dados abertos disponíveis em: https://dados.gov.br/dados/conjuntos-dados/destinacao-de-residuos-solidos")
