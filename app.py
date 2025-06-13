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
# Mantém a estilização e o rótulo na caixa flutuante
st.markdown("""
<style>
    .audio-accessibility {
        position: fixed;
        top: 60px;
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
    /* Oculta o botão customizado que você tinha no HTML, pois o player do st.audio já tem controles */
    .audio-accessibility button {
        display: none; /* Oculta o botão do SVG */
    }
    .audio-label {
        font-weight: 600;
        font-size: 15px;
        color: #333;
        white-space: nowrap;
    }
    /* O player do st.audio não será afetado diretamente por estas classes de show/hide */
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
            right: 10px;
            padding: 13px 15px;
        }
        .audio-label {
            font-size: 13px;
        }
    }
</style>

<div class="audio-accessibility" id="audioContainer">
    <span class="audio-label">Audiodescrição</span>
    </div>

<script>
    // Se você não tiver outro elemento para 'audioToggle' ou 'audioPlayer', este script pode ser removido
    const toggleButton = document.getElementById('audioToggle');
    const audioPlayer = document.getElementById('audioPlayer');
    
    if (toggleButton && audioPlayer) { // Verifica se os elementos existem antes de tentar manipulá-los
        toggleButton.addEventListener('click', function() {
            audioPlayer.classList.toggle('show');
            const isExpanded = audioPlayer.classList.contains('show');
            this.setAttribute('aria-expanded', isExpanded);
        });
        
        document.addEventListener('click', function(event) {
            const container = document.getElementById('audioContainer');
            if (!container.contains(event.target) && audioPlayer.classList.contains('show')) {
                audioPlayer.classList.remove('show');
                toggleButton.setAttribute('aria-expanded', 'false');
            }
        });
    }
</script>
""", unsafe_allow_html=True)

# Adiciona o player de áudio do Streamlit logo após a caixa flutuante do rótulo
# O arquivo 'descricao.mp3' DEVE estar no mesmo diretório do seu script Python no GitHub
try:
    audio_file = open('descricao.mp3', 'rb') # Abre o arquivo em modo binário
    audio_bytes = audio_file.read()          # Lê os bytes do arquivo
    st.audio(audio_bytes, format='audio/mp3', start_time=0) # Adiciona o componente de áudio
except FileNotFoundError:
    st.error("Arquivo de audiodescrição 'descricao.mp3' não encontrado. Certifique-se de que ele está no mesmo diretório do seu script no GitHub.")

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
    "Nota Sugerida": [2, 2, 2, 2, 1, 2, 2],
    "Justificativa": [
        "Interface limpa, responsiva, com métrica visual e gráfico bem estruturado",
        "Conecta créditos de carbono com dados públicos sobre resíduos de poda – abordagem original e prática",
        "Uso de dados abertos do governo com explicitação da fonte e visualização clara",
        "Evidencia o impacto positivo da compostagem, tanto ambiental quanto econômico",
        "Só uma fonte claramente identificada (dados.gov.br)",
        "Utiliza Python, Streamlit e Altair",
        "Texto claro, sem barreiras visuais e com audiodescrição"
    ]
})

st.subheader("Autoavaliação")
st.dataframe(avaliacao, use_container_width=True)
