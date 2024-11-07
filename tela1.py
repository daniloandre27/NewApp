# Importando as Bibliotecas
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import matplotlib.pyplot as plt

# Função para Resetar o Índice do DataFrame
def drop_reset_index(df):
    df = df.dropna()
    df = df.reset_index(drop=True)
    df.index += 1
    return df

# Função para Iniciar a Tela 1
def show_tela1():
    st.header("Under Asiatico")
    dia = st.date_input("Data de Análise", date.today())
    dia_formatado = dia.strftime('%d/%m/%Y')

    # Carregando o DataFrame
    #base = pd.read_csv('C:\\Users\\Jarvis\\Documents\\Projetos\\Under\\jogos_filtrados.csv')
    base = pd.read_csv('jogos_filtrados.csv')
    flt = base['date'] == dia_formatado
    Entradas = base[flt]
    Entradas = Entradas[['id','date' ,'league', 'home', 'away', 'ft_ou_handicap_opening', 'ft_ou_o_opening']]
    Entradas = drop_reset_index(Entradas)

    st.subheader("Entradas")
    st.text('')

    for a, b, c, d, e, f in zip(
            Entradas.league,
            Entradas.date,
            Entradas.home,
            Entradas.away,
            Entradas.ft_ou_handicap_opening,
            Entradas.ft_ou_o_opening):
        liga = a
        horario = b
        home = c
        away = d
        Under = e
        odd = f

        st.markdown(f"<span style='color:green'><b>{liga}</b></span>", unsafe_allow_html=True)
        st.markdown(f"{home} x {away} - {horario} | Under:  {Under} | Odd: {odd}")
        link = f'<div style="text-align:left"><a href="https://www.bet365.com/?nr=1#/AX/K^{home}">{"Aposte Aqui"}</a></div>'
        st.markdown(link, unsafe_allow_html=True)
        st.write('______________________________________________')
        st.write('')
