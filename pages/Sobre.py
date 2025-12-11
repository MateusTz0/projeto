import streamlit as st
from io import BytesIO
import random
import datetime
import pandas as pd
# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="sobre", page_icon="🏠")

# BLOQUEIO DE ACESSO
if "autenticado" not in st.session_state or not st.session_state.autenticado:
    st.warning("⚠️ Você precisa se cadastrar para acessar esta página.")
    st.stop()

st.markdown(
    """
    <style>
    .big-title {font-size:36px; font-weight:700;}
    .subtitle {font-size:18px; color: #666; margin-bottom: 12px}
    .feature {padding:10px 12px; border-radius:10px; background: rgba(0,0,0,0.03); margin-bottom:8px}
    .muted {color:#6b7280}
    .logo {border-radius:12px}
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 3])
with col1:
    st.image("https://via.placeholder.com/220x80.png?text=ProFoco+Logo", width=180, caption=None, output_format="PNG")
with col2:
    st.markdown("<div class='big-title'>ProFoco</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Seu assistente diário de temas de estudo — claro, simples e eficiente.</div>", unsafe_allow_html=True)

st.markdown("---")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric(label="Sugestões diárias", value="1 tema / dia")
with c2:
    st.metric(label="Customização", value="Alto")
with c3:
    st.metric(label="Registro de progresso", value="Incluso")

st.markdown("---")

#Conteúdo principal
st.header("Sobre o ProFoco")
st.write(
    "O ProFoco é um aplicativo criado para ajudar estudantes e profissionais a manterem uma rotina de estudos mais organizada, consistente e motivadora. Receba sugestões de temas diários alinhadas com seus objetivos e disponibilidade."
)


with st.expander("Como funciona", expanded=False):
    st.write(
        "O ProFoco analisa seus objetivos, áreas de interesse e disponibilidade diária para sugerir temas de estudo personalizados. \n\n" 
        "Em vez de perder tempo decidindo por onde começar, você recebe uma orientação clara — um tema por dia — ajustado ao seu progresso e preferências."
    )

with st.expander("Por que o ProFoco existe", expanded=False):
    st.write(
        "Manter uma rotina de estudos é difícil quando há muitos tópicos e materiais. O ProFoco nasceu para tornar o processo mais leve: um guia simples, porém inteligente, que acompanha seu ritmo e incentiva evolução contínua."
    )

with st.expander("Recursos principais", expanded=True):
    st.markdown("<div class='feature'><strong>• Sugestão diária de tema</strong> — personalizada para você.</div>", unsafe_allow_html=True)
    st.markdown("<div class='feature'><strong>• Registro de progresso</strong> — histórico e métricas simples.</div>", unsafe_allow_html=True)
    st.markdown("<div class='feature'><strong>• Ajuste inteligente</strong> — adapta-se conforme seu desempenho.</div>", unsafe_allow_html=True)
    st.markdown("<div class='feature'><strong>• Listas configuráveis</strong> — organize áreas e temas do seu jeito.</div>", unsafe_allow_html=True)
    st.markdown("<div class='feature'><strong>• Notificações e metas</strong> — estímulo à constância.</div>", unsafe_allow_html=True)

st.markdown("---")

# Missão
st.subheader("Nossa missão")
st.write("Ajudar você a estudar com mais clareza, foco e propósito — todos os dias.")

st.write("\n")
cols = st.columns([3,1])
with cols[0]:
    st.info("Quer experimentar o ProFoco? Baixe a versão de demonstração ou comece uma avaliação gratuita no app.")
with cols[1]:
    if st.button("Abrir demonstração" ):
        st.toast("Funcionalidade de demonstração não implementada nesta amostra.")

st.markdown("---")

#contato
st.subheader("Equipe & Contato")
st.write("Equipe pequena e ágil focada em produto, design e educação.\nPara parcerias e suporte: contato@profoco.app")

#baixar folheto sobre o profoco
brochure_md = """# ProFoco - Folheto\n\nProFoco é seu assistente de estudos diário...\n\n- Sugestão diária de tema\n- Registro de progresso\n- Ajuste inteligente\n"""

if st.download_button("Baixar folheto (PDF demo)", data=BytesIO(brochure_md.encode("utf-8")), file_name="profoco_folheto_demo.txt", mime="text/plain"):
    st.success("Download iniciado")

st.markdown("---")

#resumir página
if st.checkbox("Versão curta da página", value=False):
    st.markdown("**ProFoco** — sugestão diária de tema para ajudar sua rotina de estudos. Simples, pessoal e eficiente.")

st.markdown("<div class='muted'>© {year} ProFoco — Feito com foco e café.</div>".format(year=2025), unsafe_allow_html=True)

with st.expander("Texto para App Store / Pitch", expanded=False):
    st.code(
        """
ProFoco — Seu assistente diário de estudos. Receba um tema por dia, acompanhe seu progresso e aprenda com constância.
- Sugestões personalizadas
- Histórico e métricas
- Ajuste inteligente ao seu ritmo
"""
    )
