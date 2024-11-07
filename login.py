import streamlit as st
import csv
from menu import main as menu_main

def verificar_login(usuario, senha):
    with open('usuarios.csv', mode='r') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=';')
        for linha in leitor_csv:
            if usuario == linha[0] and senha == linha[1]:
                return True
    return False

def valida():
    if 'logado' not in st.session_state or not st.session_state['logado']:
        st.write("<h1 style='text-align: center;'>Bem-Vindo</h1>", unsafe_allow_html=True)
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
            
        if st.button("Login"):
            if verificar_login(usuario, senha):
                st.session_state['logado'] = True
                st.session_state['usuario_atual'] = usuario
            else:
                st.error("Usuário ou senha incorretos.")
    else:
        menu_main()

if __name__ == "__main__":
    valida()
st.write("<h1 style='text-align: center; font-size: 15px;'>Quer participar? Chama o Altair<br>Zap: (22)98802-4908</h1>", unsafe_allow_html=True)     
