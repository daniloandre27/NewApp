import streamlit as st
from tela1 import show_tela1

# Configuração da página
st.set_page_config(page_title="Meu Dashboard", layout="centered")

# Função principal que controla o fluxo do aplicativo
def main():


        # Menu de navegação
        st.title("Monstro dos Greens")
        paginas = ['Lay Home', 'Lay Away', 'Lay 0 x 1']
        escolha = st.radio('', paginas)
        if escolha == 'Lay Home':
            show_tela1()


if __name__ == "__main__":
    main()
