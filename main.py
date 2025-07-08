import streamlit as st
import requests

st.set_page_config(page_title='Chatbot', layout='wide')
st.title("Chatbot dos Crias da TCS")

with st.sidebar:
    st.header("Configurações")
    modelos = ['llama3.1:8b']
    modelo_selecionado = st.selectbox(
        'Escolha o Modelo',
        options=modelos,
        index=0
    )

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Digite sua mensagem...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Junta o histórico num prompt contínuo (gambiarra pro /api/generate)
    prompt = ""
    for msg in st.session_state.chat_history:
        role = msg["role"]
        content = msg["content"]
        prompt += f"{role.upper()}: {content}\n"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": modelo_selecionado,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:
        resposta = response.json().get("response", "")
    else:
        resposta = f"Erro {response.status_code} ao se comunicar com o Ollama."

    st.session_state.chat_history.append({"role": "assistant", "content": resposta})

# Exibir mensagens
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])