import streamlit as st

st.set_page_config(page_title="Cadastro", page_icon="📝")

# Inicializa variáveis
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuarios" not in st.session_state:
    st.session_state.usuarios = []

st.title("📋 Cadastro de Usuário")

with st.form("form_cadastro"):
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    enviar = st.form_submit_button("Cadastrar")

if enviar:
    st.session_state.usuarios.append({
        "Nome": nome,
        "Email": email,
        "Senha": senha
    })
    st.session_state.autenticado = True
    st.success(f"Usuário {nome} cadastrado com sucesso! Agora você pode acessar as outras páginas.")