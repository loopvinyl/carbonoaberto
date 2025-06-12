import pandas as pd
import streamlit as st

# === Carrega os dados exportados ===
arquivo = "emissoes_resultado.xlsx"  # caminho relativo para funcionar no Streamlit Cloud
df_mensal = pd.read_excel(arquivo, sheet_name="Mensal")
df_anual = pd.read_excel(arquivo, sheet_name="Anual")

# === Configuração da página ===
#st.set_page_config(page_title="Carbono Aberto", layout="wide")
#st.title("Carbono Aberto: aplicativo que contabiliza, em Reais e Dólares, os Créditos de Carbono gerados com as 'Emissões Evitadas', estimadas ao desviar resíduos com poda para compostagem no lugar da destinação aterragem")
#

# === Configuração da página ===
st.set_page_config(page_title="Carbono Aberto", layout="wide")

# Título grande, subtítulo colado, espaçamento só abaixo do subtítulo
st.markdown("""
<div style='margin-bottom: 2rem;'>
  <h1 style='font-size: 9rem; line-height: 1.1; margin: 0;'>Carbono Aberto</h1>
  <p style='font-size: 1.8rem; margin: 0;'>aplicativo que contabiliza, em Reais e Dólares, os Créditos de Carbono gerados com as 'Emissões Evitadas', estimadas ao desviar resíduos com poda para compostagem no lugar da destinação aterragem.</p>
</div>
""", unsafe_allow_html=True)


#
# === KPIs ===
col1, col2 = st.columns(2)

with col1:
    receita_brl = df_anual[df_anual["Ano"] == "Receita (BRL)"]["Emission Reductions (tCO2e)"].values[0]
    st.metric("💰 Receita com Créditos de Carbono (BRL)", f"R$ {receita_brl:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

with col2:
    receita_usd = df_anual[df_anual["Ano"] == "Receita (USD)"]["Emission Reductions (tCO2e)"].values[0]
    st.metric("💰 Receita com Créditos de Carbono (USD)", f"US$ {receita_usd:,.2f}")

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

# === Fonte de dados ===
st.caption("Dados baseados em emissões de resíduos de poda destinados à compostagem (2019-2022), extraídos de dados abertos disponíveis em: https://dados.gov.br/dados/conjuntos-dados/destinacao-de-residuos-solidos")

