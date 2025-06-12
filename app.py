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

# === Player de Audiodescrição - Posição Corrigida ===
st.markdown("""
<style>
    .audio-accessibility {
        position: absolute;
        top: 140px;
        right: 20px;
        z-index: 100;
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
        .audio-accessibility
