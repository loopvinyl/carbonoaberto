import pandas as pd
import streamlit as st
import altair as alt
import base64

# === Carrega os dados exportados ===
arquivo = "emissoes_resultado.xlsx"  # caminho relativo para funcionar no Streamlit Cloud
df_mensal = pd.read_excel(arquivo, sheet_name="Mensal")
df_anual = pd.read_excel(arquivo, sheet_name="Anual")

# === Configuração da página ===
st.set_page_config(page_title="Carbono Aberto", layout="wide")

# === Player de Audiodescrição Melhorado ===
st.markdown("""
<style>
    .audio-accessibility {
        position: fixed;
        top: 55px;
        right: 15px;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 50px;
        padding: 12px 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        border: 1px solid #e0e0e0;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.3s ease;
        backdrop-filter: blur(4px);
    }
    .audio-accessibility:hover {
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    .audio-accessibility button {
        background: #2e7d32;
        color: white;
        border: none;
        border-radius: 50%;
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    .audio-accessibility button:hover {
        background: #1b5e20;
        transform: scale(1.05);
    }
    .audio-accessibility button:active {
        transform: scale(0.95);
    }
    .audio-accessibility svg {
        width: 24px;
        height: 24px;
        fill: white;
    }
    .audio-label {
        font-weight: 600;
        font-size: 15px;
        color: #333;
        white-space: nowrap;
    }
    .audio-player {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.4s ease;
        width: 240px;
    }
    .audio-player.show {
        max-height: 100px;
        margin-top: 12px;
    }
    
    @media (max-width: 768px) {
        .audio-accessibility {
            top: 55px;
            right: 15px;
            padding: 10px 15px;
        }
        .audio-label {
            font-size: 13px;
        }
    }
</style>

<div class="audio-accessibility" id="audioContainer">
    <button id="audioToggle" aria-label="Controle de audiodescrição">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
        </svg>
    </button>
    <span class="audio-label">Audiodescrição</span>
    <div class="audio-player" id="audioPlayer">
        <audio controls style="width:100%">
            <source src="https://github.com/loopvinyl/carbonoaberto/blob/main/descricao.mp3" type="audio/mp3">
            Seu navegador não suporta o elemento de áudio.
        </audio>
    </div>
</div>

<script>
    const toggleButton = document.getElementById('audioToggle');
    const audioPlayer = document.getElementById('audioPlayer');
    
    toggleButton.addEventListener('click', function() {
        audioPlayer.classList.toggle('show');
        
        // Atualiza o ARIA label
        const isExpanded = audioPlayer.classList.contains('show');
        this.setAttribute('aria-expanded', isExpanded);
    });
    
    // Fecha o player ao clicar fora
    document.addEventListener('click', function(event) {
        const container = document.getElementById('audioContainer');
        if (!container.contains(event.target) && audioPlayer.classList.contains('show')) {
            audioPlayer.classList.remove('show');
            toggleButton.setAttribute('aria-expanded', 'false');
        }
    });
</script>
""", unsafe_allow_html=True)

# === Título Responsivo ===
st.markdown("""
<style>
    @media (max-width: 768px) {
        .titulo-h1 {
            font-size: 3rem !important;
        }
        .titulo-p {
            font-size: 1.2rem !important;
        }
    }
    @media (min-width: 769px) {
        .titulo-h1 {
            font-size: 6rem !important;
        }
        .titulo-p {
            font-size: 1.8rem !important;
        }
    }
</style>

<div style='margin-bottom: 3rem;'>
  <h1 class='titulo-h1' style='line-height: 1.1; margin: 0;'>Carbono Aberto</h1>
  <p class='titulo-p' style='margin: 0;'>aplicativo que contabiliza, em Reais e Dólares, os Créditos de Carbono gerados com as Emissões Evitadas, estimadas ao desviar resíduos com poda para compostagem no lugar da destinação aterragem</p>
</div>
""", unsafe_allow_html=True)

# === KPIs ===
col1, col2 = st.columns(2)

with col1:
    receita_brl = df_anual[df_anual["Ano"] == "Receita (BRL)"]["Emission Reductions (tCO2e)"].values[0]
    st.metric("Receita com Créditos de Carbono (BRL)", f"R$ {receita_brl:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

with col2:
    receita_usd = df_anual[df_anual["Ano"] == "Receita (USD)"]["Emission Reductions (tCO2e)"].values[0]
    st.metric("Receita com Créditos de Carbono (USD)", f"US$ {receita_usd:,.2f}")

# === Gráfico de Emissões Anuais ===
st.subheader("Emissões Evitadas em tCO₂e por ano, com decaimento")

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
    dy=-5
).encode(
    text='Emissões Formatadas:N'
)

st.altair_chart((chart + text), use_container_width=True)

# === Fonte de dados ===
st.caption("Dados baseados em emissões de resíduos de poda destinados à compostagem (2019-2022), extraídos de dados abertos disponíveis em: https://dados.gov.br/dados/conjuntos-dados/destinacao-de-residuos-solidos")

# === Tabela de Avaliação ===
avaliacao = pd.DataFrame({
    "Critério": [
        "Apresentação",
        "Inovação",
        "Fomento à transparência e controle social",
        "Foco em pessoas e impacto para a sociedade",
        "Duas ou mais fontes de dados abertos",
        "Uso de ferramentas tecnológicas",
        "Inclusividade"
    ],
    "Nota (máx.)": [2, 2, 2, 2, 2, 2, 2],
    "Nota Sugerida": [2, 2, 2, 2, 1, 1, 0],
    "Justificativa": [
        "Interface limpa, responsiva, com métrica visual e gráfico bem estruturado. Excelente uso do Altair",
        "Conecta créditos de carbono com dados públicos sobre resíduos de poda – abordagem original e prática",
        "Uso de dados abertos do governo com explicitação da fonte e visualização clara",
        "Evidencia o impacto positivo da compostagem, tanto ambiental quanto econômico",
        "Só uma fonte claramente identificada (dados.gov.br)",
        "Utiliza Python, Streamlit e Altair",
        "Texto claro e sem barreiras visuais, mas falta acessibilidade explícita"
    ]
})

st.subheader("Autoavaliação")
st.dataframe(avaliacao, use_container_width=True)

# === Adicionar nota sobre acessibilidade ===
st.markdown("""
<div style="margin-top: 30px; padding: 15px; background-color: #f0faf0; border-radius: 10px; border-left: 4px solid #2e7d32;">
    <p style="margin: 0; font-size: 16px;">
        <strong>Recurso de acessibilidade:</strong> Utilize o botão de audiodescrição no canto superior direito para ouvir a descrição completa do aplicativo, incluindo explicações sobre o gráfico e os dados apresentados.
    </p>
</div>
""", unsafe_allow_html=True)
