import pandas as pd
import streamlit as st

# === Carrega os dados exportados ===
arquivo = "emissoes_resultado.xlsx"  # caminho relativo para funcionar no Streamlit Cloud
df_mensal = pd.read_excel(arquivo, sheet_name="Mensal")
df_anual = pd.read_excel(arquivo, sheet_name="Anual")

# === Configuração da página ===
st.set_page_config(page_title="Carbono Aberto", layout="wide")
st.title("App Carbono Aberto: calcula 'Emissões Evitadas', ao desviar resíduos com poda para compostagem no lugar da destinação aterragem, estima os créditos de carbono gerados em Reais e Dólares")

# === KPIs ===
col1, col2 = st.columns(2)

with col1:
    receita_brl = df_anual[df_anual["Ano"] == "Receita (BRL)"]["Emission Reductions (tCO2e)"].values[0]
    st.metric("💰 Receita com Créditos de Carbono (BRL)", f"R$ {receita_brl:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

with col2:
    receita_usd = df_anual[df_anual["Ano"] == "Receita (USD)"]["Emission Reductions (tCO2e)"].values[0]
    st.metric("💰 Receita com Créditos de Carbono (USD)", f"US$ {receita_usd:,.2f}")


# === Gráfico de Emissões Mensais ===
#st.subheader("Emissões Evitadas em tCO2e por mês, sem decaimento")
#df_mensal_plot = df_mensal.copy()
#df_mensal_plot["Mes"] = df_mensal_plot["Mes"].astype(str).str.zfill(2)
#df_mensal_plot["AnoMes"] = df_mensal_plot["Ano"].astype(str) + "-" + df_mensal_plot["Mes"]
#df_mensal_plot = df_mensal_plot.sort_values("AnoMes")
#st.line_chart(df_mensal_plot.set_index("AnoMes")["Emission Reductions (tCO2e)"])
#

# === Gráfico de Emissões Mensais ===
st.subheader("Emissões Evitadas em tCO2e por mês, sem decaimento")
import altair as alt

# Pré-processamento dos dados
df_mensal_plot = df_mensal.copy()
df_mensal_plot["Mes"] = df_mensal_plot["Mes"].astype(str).str.zfill(2)
df_mensal_plot["AnoMes"] = df_mensal_plot["Ano"].astype(str) + "-" + df_mensal_plot["Mes"]
df_mensal_plot = df_mensal_plot.sort_values("AnoMes")

# Formatação brasileira para os valores
df_mensal_plot = df_mensal_plot.copy()
df_mensal_plot["Emissões Formatadas"] = df_mensal_plot["Emission Reductions (tCO2e)"].apply(
    lambda x: f"{x:,.0f}".replace(",", ".").replace(".", ",", 1)
)

# Criar o gráfico de linha com Altair
chart = alt.Chart(df_mensal_plot).mark_line(point=True).encode(
    x=alt.X('AnoMes:N', title='Mês/Ano', axis=alt.Axis(labelAngle=45)),
    y=alt.Y('Emission Reductions (tCO2e):Q', title='Emissões Evitadas (tCO₂e)',
            axis=alt.Axis(format='.0f', labelExpr="replace(datum.label, /\\B(?=(\\d{3})+(?!\\d))/g, '.')"))
).properties(
    width=700,
    height=400
)

# Adicionar pontos com tooltip
points = chart.mark_point().encode(
    tooltip=[
        alt.Tooltip('AnoMes:N', title='Período'),
        alt.Tooltip('Emission Reductions (tCO2e):Q', title='Emissões', format='.0f')
    ]
)

# Adicionar rótulos nos pontos
text = chart.mark_text(
    align='left',
    baseline='bottom',
    dx=5,
    dy=-5
).encode(
    text=alt.Text('Emissões Formatadas:N')
)

st.altair_chart((chart + points + text), use_container_width=True)

#
# === Gráfico de Emissões Anuais ===
#st.subheader("Emissões Evitadas em tCO2e por Ano, com decaimento")
#df_anual_plot = df_anual[df_anual["Ano"].apply(lambda x: str(x).isdigit())]
#df_anual_plot = df_anual_plot.sort_values("Ano")
#st.bar_chart(df_anual_plot.set_index("Ano")["Emission Reductions (tCO2e)"])
##

# === Gráfico de Emissões Anuais ===
st.subheader("Emissões Evitadas em tCO2e por ano, com decaimento")
import altair as alt

# Filtra e ordena os dados
df_anual_plot = df_anual[df_anual["Ano"].apply(lambda x: str(x).isdigit())]
df_anual_plot = df_anual_plot.sort_values("Ano")

# Formata os números para padrão brasileiro diretamente nos dados
df_anual_plot = df_anual_plot.copy()
df_anual_plot["Emissões Formatadas"] = df_anual_plot["Emission Reductions (tCO2e)"].apply(
    lambda x: f"{x:,.0f}".replace(",", ".").replace(".", ",", 1)
)

# Cria o gráfico com Altair
chart = alt.Chart(df_anual_plot).mark_bar().encode(
    x=alt.X('Ano:N', title='Ano', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Emission Reductions (tCO2e):Q', title='Emissões Evitadas (tCO₂e)', 
            axis=alt.Axis(format='.0f', labelExpr="replace(datum.label, /\\B(?=(\\d{3})+(?!\\d))/g, '.')"))
).properties(
    width=600,
    height=400
)

# Adiciona rótulos
text = chart.mark_text(
    align='center',
    baseline='bottom',
    dy=-5  # Ajusta posição vertical
).encode(
    text='Emissões Formatadas:N'
)

st.altair_chart((chart + text), use_container_width=True)


##
# === Fonte de dados ===
st.caption("Dados baseados em emissões de resíduos de poda destinados à compostagem (2019-2022), extraídos de dados abertos disponíveis em: https://dados.gov.br/dados/conjuntos-dados/destinacao-de-residuos-solidos")
