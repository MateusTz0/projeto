import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dados", page_icon="📄")

# Palavra secreta que libera a visualização
PALAVRA_CHAVE = "mateus123"

st.title("🔒 Acesso Restrito")

# Campo para a senha
codigo = st.text_input("Digite a palavra-chave para acessar:", type="password")

# Se a senha estiver errada OU não foi digitada
if codigo != PALAVRA_CHAVE:
    st.warning("⚠️ Digite a palavra-chave correta para ver os dados.")
    st.stop()  # PARA TUDO AQUI! Nada abaixo aparece.

# Se chegou aqui → senha correta
st.success("✅ Acesso liberado!")

# Mostrar dados cadastrados
if "usuarios" in st.session_state and st.session_state.usuarios:
    df = pd.DataFrame(st.session_state.usuarios)
    st.title("👥 Usuários Cadastrados")
    st.table(df)
else:
    st.info("Nenhum usuário cadastrado ainda.")
