import streamlit as st
import pandas as pd
import csv
from tela1 import show_tela1

def verificar_login(usuario, senha):
    with open('usuarios.csv', mode='r') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=';')
        for linha in leitor_csv:
            if usuario == linha[0] and senha == linha[1]:
                return True
    return False

def verificar_admin(usuario):
    with open('usuarios.csv', mode='r') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=';')
        for linha in leitor_csv:
            if len(linha) >= 3 and usuario == linha[0] and linha[2] == '1':
                return True
    return False

def usuario_existe(usuario):
    with open('usuarios.csv', mode='r') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=';')
        for linha in leitor_csv:
            if usuario == linha[0]:
                return True
    return False

def adicionar_usuario(usuario, senha, usuario_atual):
    if usuario == "" or senha == "":
        st.error("Por favor, preencha o usuário e a senha.")
        return
    if usuario_existe(usuario):
        st.error("O usuário já existe.")
        return
    if not verificar_admin(usuario_atual):
        st.error("Apenas administradores podem adicionar novos usuários.")
        return
    with open('usuarios.csv', mode='a', newline='') as arquivo:
        escritor_csv = csv.writer(arquivo, delimiter=';')
        escritor_csv.writerow([usuario, senha])
        st.success("Usuário registrado com sucesso!")

def alterar_senha(usuario, senha_atual, nova_senha):
    if not verificar_login(usuario, senha_atual):
        st.error("Senha atual incorreta. Tente novamente.")
        return
    with open('usuarios.csv', mode='r') as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=';')
        linhas = list(leitor_csv)
    with open('usuarios.csv', mode='w', newline='') as arquivo:
        escritor_csv = csv.writer(arquivo, delimiter=';')
        for linha in linhas:
            if linha[0] == usuario:
                linha[1] = nova_senha
            escritor_csv.writerow(linha)
    st.success("Senha alterada com sucesso!")

st.set_page_config(page_title="Meu Dashboard", layout="centered")

def main():
    if 'logado' not in st.session_state:
        st.session_state['logado'] = False
    if 'usuario_atual' not in st.session_state:
        st.session_state['usuario_atual'] = None

    if not st.session_state['logado']:
        st.write("<h1 style='text-align: center;'>Bem-Vindo</h1>", unsafe_allow_html=True)
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        
        if st.button("Login"):
            if verificar_login(usuario, senha):
                st.session_state['logado'] = True
                st.session_state['usuario_atual'] = usuario
                # Redireciona o fluxo para a atualização da interface
                st.experimental_rerun()
            else:
                st.error("Usuário ou senha incorretos.")
                return  # Retorna para evitar o restante do código ao exibir o erro

    else:
        st.markdown("<h1 style='text-align: center;'>Bem-vindo vencedor!</h1>", unsafe_allow_html=True)
        
        # Menu de navegação
        opcoes = ["Under", "Back", "Over", "Resultados"]
        escolha = st.selectbox("Selecione uma opção", opcoes)

        # Exibir a tela escolhida
        if escolha == "Under":
            show_tela1()  # Mostra a tela 1
        elif escolha == "Back":
            st.write("Aqui estarão as análises (em desenvolvimento).")  # Mostra a tela 2, adicionar quando estiver disponível
        elif escolha == "Over":
            st.write("Aqui estarão as análises (em desenvolvimento).")  # Mostra a tela 3, adicionar quando estiver disponível
        elif escolha == "Resultados":
            st.write("Aqui estarão os resultados das análises (em desenvolvimento).")

        if st.checkbox("Cadastro de usuários"):
            st.subheader("Cadastro de Usuários")
            novo_usuario = st.text_input("Novo usuário", key="novo_usuario")
            nova_senha_cadastro = st.text_input("Nova senha", key="nova_senha_cadastro", type="password")
            if st.button("Cadastrar"):
                adicionar_usuario(novo_usuario, nova_senha_cadastro, st.session_state['usuario_atual'])

        if st.checkbox("Alteração de senha"):
            st.subheader("Alterar Senha")
            senha_atual = st.text_input("Senha atual", key="senha_atual", type="password")
            nova_senha_input = st.text_input("Nova senha", key="nova_senha_input", type="password")
            if st.button("Alterar"):
                alterar_senha(st.session_state['usuario_atual'], senha_atual, nova_senha_input)

        if st.button("Sair"):
            st.session_state['logado'] = False
            st.experimental_rerun()  # Atualiza imediatamente após o logout

if __name__ == "__main__":
    main()

st.write(
    "<h1 style='text-align: center; font-size: 15px;'>Quer participar? Chama o Altair<br>Zap: (22)98802-4908</h1>",
    unsafe_allow_html=True
)
