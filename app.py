import pandas as pd
import streamlit as st

# === Carrega os dados exportados ===
arquivo = "/content/emissoes_resultado.xlsx"
df_mensal = pd.read_excel(arquivo, sheet_name="Mensal")
df_anual = pd.read_excel(arquivo, sheet_name="Anual")

# === Título ===
st.set_page_config(page_title="Dashboard de Emissões", layout="wide")
st.title("📊 Dashboard de Emissões e Créditos de Carbono")

# === KPIs ===
col1, col2 = st.columns(2)

with col1:
    receita_brl = df_anual[df_anual["Ano"] == "Receita (BRL)"]["Emission Reductions (tCO2e)"].values[0]
    st.metric("💰 Receita estimada (BRL)", f"R$ {receita_brl:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

with col2:
    receita_usd = df_anual[df_anual["Ano"] == "Receita (USD)"]["Emission Reductions (tCO2e)"].values[0]
    st.metric("💵 Receita estimada (USD)", f"US$ {receita_usd:,.2f}")

# === Gráfico de Emissões Mensais ===
st.subheader("📅 Emissões Mensais por Mês/Ano")
df_mensal_plot = df_mensal.copy()
df_mensal_plot["Mes"] = df_mensal_plot["Mes"].astype(str).str.zfill(2)
df_mensal_plot["AnoMes"] = df_mensal_plot["Ano"].astype(str) + "-" + df_mensal_plot["Mes"]
df_mensal_plot = df_mensal_plot.sort_values("AnoMes")
st.line_chart(df_mensal_plot.set_index("AnoMes")["Emission Reductions (tCO2e)"])

# === Gráfico de Emissões Anuais ===
st.subheader("📈 Emissões Anuais Acumuladas")
df_anual_plot = df_anual[df_anual["Ano"].apply(lambda x: str(x).isdigit())]
df_anual_plot = df_anual_plot.sort_values("Ano")
st.bar_chart(df_anual_plot.set_index("Ano")["Emission Reductions (tCO2e)"])

# === Fonte de dados ===
st.caption("Dados baseados em emissões de resíduos de poda destinados à compostagem (2019-2022).")
