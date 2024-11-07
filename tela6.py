# Importand as Bibliotecas
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from io import BytesIO

# Importando as Funções
def drop_reset_index(df):
    df = df.dropna()
    df = df.reset_index(drop=True)
    df.index += 1
    return df

def plot_profit_acu(dataframe, title_text):
    dataframe['Profit_acu'] = dataframe.Profit.cumsum()
    n_apostas = dataframe.shape[0]
    profit = round(dataframe.Profit_acu.tail(1).item(), 2)
    # ROI = round((dataframe.Profit_acu.tail(1) / n_apostas * 100).item(), 2)
    dataframe['Investimento_acu'] = dataframe.Investimento.cumsum()
    ROI = round(((dataframe.Profit_acu.tail(1) / dataframe.Investimento_acu.tail(1)) * 100).item(), 2)
    drawdown = dataframe['Profit_acu'] - dataframe['Profit_acu'].cummax()
    drawdown_maximo = round(drawdown.min(), 2)
    winrate_medio = round((dataframe['Profit'] > 0).mean() * 100, 2)
    desvio_padrao = round(dataframe['Profit'].std(), 2)
    plt.figure(figsize=(10, 4))
    plt.plot(dataframe.Profit_acu)
    plt.title(title_text)
    plt.xlabel('Entradas')
    plt.ylabel('Stakes')
    plt.grid(True)
    plt.show()
    st.text(f"Método: {title_text}")
    st.text(f"Profit: {profit} stakes em {n_apostas} jogos")
    st.text(f"ROI: {ROI}%")
    st.text(f"Drawdown Máximo Acumulado: {drawdown_maximo} stakes")
    st.text(f"Winrate Médio: {winrate_medio}%")
    st.text(f"Desvio Padrão: {desvio_padrao}")
    st.text("")


def ajustar_id_mercado(id_mercado, comprimento_decimal_desejado=9):
    id_mercado_str = str(id_mercado)
    partes = id_mercado_str.split('.')
    if len(partes) == 1:
        return id_mercado_str + '.' + '0' * comprimento_decimal_desejado
    parte_inteira, parte_decimal = partes
    zeros_para_adicionar = comprimento_decimal_desejado - len(parte_decimal)
    if zeros_para_adicionar > 0:
        parte_decimal += '0' * zeros_para_adicionar
    id_mercado_ajustado = parte_inteira + '.' + parte_decimal
    return id_mercado_ajustado

def remove_outliers(df, cols):
    for col in cols:
        Q1 = df[col].quantile(0.05)
        Q3 = df[col].quantile(0.95)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df

def entropy(probabilities):
    probabilities = probabilities[probabilities > 0]
    return -np.sum(probabilities * np.log2(probabilities))

# Iniciando a Tela 6
def show_tela6():
    st.title("Resultados")
    
    @st.cache_data
    def load_base():

        base = pd.read_csv('https://github.com/futpythontrader/YouTube/raw/main/Bases_de_Dados/Betfair/Base_de_Dados_Betfair_Exchange_Back_Lay.csv')
        return base

    df = load_base()
    df = df[['Date','League','Home','Away','Goals_H','Goals_A','Goals_Min_H', 'Goals_Min_A',
             'Odd_H_Back','Odd_H_Lay','Odd_A_Back','Odd_A_Lay','Odd_D_Back','Odd_D_Lay',
             'Odd_Under25_FT_Back','Odd_Over25_FT_Back','Odd_BTTS_Yes_Back','Odd_BTTS_No_Back',
             'Odd_CS_0x0_Back','Odd_CS_0x0_Lay','Odd_CS_0x1_Back','Odd_CS_0x1_Lay','Odd_CS_0x2_Back','Odd_CS_0x2_Lay','Odd_CS_0x3_Back','Odd_CS_0x3_Lay',
             'Odd_CS_1x0_Back','Odd_CS_1x0_Lay','Odd_CS_1x1_Back','Odd_CS_1x1_Lay','Odd_CS_1x2_Back','Odd_CS_1x2_Lay','Odd_CS_1x3_Back','Odd_CS_1x3_Lay',
             'Odd_CS_2x0_Back','Odd_CS_2x0_Lay','Odd_CS_2x1_Back','Odd_CS_2x1_Lay','Odd_CS_2x2_Back','Odd_CS_2x2_Lay','Odd_CS_2x3_Back','Odd_CS_2x3_Lay',
             'Odd_CS_3x0_Back','Odd_CS_3x0_Lay','Odd_CS_3x1_Back','Odd_CS_3x1_Lay','Odd_CS_3x2_Back','Odd_CS_3x2_Lay','Odd_CS_3x3_Back','Odd_CS_3x3_Lay',
             'Odd_CS_Goleada_H_Back','Odd_CS_Goleada_H_Lay','Odd_CS_Goleada_A_Back','Odd_CS_Goleada_A_Lay','Odd_CS_Goleada_D_Back','Odd_CS_Goleada_D_Lay']]
    df = drop_reset_index(df)
    
    df['VAR1'] = np.sqrt((df['Odd_H_Back'] - df['Odd_A_Back'])**2)
    df['VAR2'] = np.degrees(np.arctan((df['Odd_A_Back'] - df['Odd_H_Back']) / 2))
    df['VAR3'] = np.degrees(np.arctan((df['Odd_D_Back'] - df['Odd_A_Back']) / 2))
    
    odds_columns = [col for col in df.columns if 'Odd_' in col]

    df_clean = remove_outliers(df, odds_columns)
    df = drop_reset_index(df_clean)

    cs_lay_columns = [col for col in df.columns if 'CS' in col and 'Lay' in col]
    cs_lay_data = df[cs_lay_columns]
    cv_cs_lay = cs_lay_data.apply(lambda x: x.std() / x.mean(), axis=1)
    df['CV_CS'] = cv_cs_lay

    probabilities_cs = cs_lay_data.replace(0, np.nan).apply(lambda x: 1 / x, axis=1)
    entropy_cs = probabilities_cs.apply(lambda x: -np.sum(x * np.log2(x)) if x.sum() != 0 else 0, axis=1)
    df['Entropy_CS'] = entropy_cs
    
    # Escolher qual análise realizar
    analysis_choice = st.selectbox("Escolha o tipo de análise", ["Lay Home", "Lay Away", "Lay 0 x 0", "Lay 1 x 0", "Lay 0 x 1"])
    
    if analysis_choice == "Lay Home":
        flt = ((df.CV_CS >= 1.70) & (df.CV_CS <= 2.40) &
       (df.Entropy_CS >= 3.30) & (df.Entropy_CS <= 3.60) & 
       (df.VAR1 >= 1) & 
       (df.VAR2 >= -70) & (df.VAR2 <= 70) & 
       (df.VAR3 >= -50) & (df.VAR2 <= 60) &
       (df.Odd_H_Lay <= 21))
        df0 = df[flt]
        df0 = drop_reset_index(df0)
        df0['Investimento'] = 10
        df0['Profit'] = -10
        df0.loc[((df0['Goals_H'] <= df0['Goals_A'])), 'Profit'] = 9.40 / (df0['Odd_H_Lay'] - 1)
        df0['Profit_acu'] = df0.Profit.cumsum()
        #df0['Date'] = df0['Date'].dt.date 
    
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df0.index, y=df0['Profit_acu'], mode='lines'))

        fig.update_layout(
            title="Profit Acumulado",
            xaxis_title="Entradas",
            yaxis_title="Stakes"
        )

        st.plotly_chart(fig)
        plot_profit_acu(df0, 'Lay Home')
        df0 = df0[['Date','League','Home','Away','Goals_H','Goals_A','Goals_Min_H','Goals_Min_A',
                   'Odd_H_Back','Odd_H_Lay','Odd_D_Back','Odd_D_Lay','Odd_A_Back','Odd_A_Lay',
                   'Odd_CS_0x1_Lay','Odd_CS_1x0_Lay','Profit']]
        
        def download_excel():
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df0.to_excel(writer, index=False, sheet_name='Sheet1')
                writer.close()
                processed_data = output.getvalue()
                return processed_data

        button = st.download_button(
        label='Download',
        data=download_excel(),
        file_name=f'Lay_Home.xlsx',
        mime='application/vnd.ms-excel')
        
    elif analysis_choice == "Lay Away":
        
        flt = (df.VAR1 >= 4) & (df.VAR2 >= 60) & (df.VAR3 <= -60)
        df0 = df[flt]
        df0 = drop_reset_index(df0)
        df0['Investimento'] = 10
        df0['Profit'] = -10
        df0.loc[((df0['Goals_H'] >= df0['Goals_A'])), 'Profit'] = 9.40 / (df0['Odd_A_Lay'] - 1)
        df0['Profit_acu'] = df0.Profit.cumsum()
    
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df0.index, y=df0['Profit_acu'], mode='lines'))

        fig.update_layout(
            title="Profit Acumulado",
            xaxis_title="Entradas",
            yaxis_title="Stakes"
        )

        st.plotly_chart(fig)
        plot_profit_acu(df0, 'Lay Away')
        df0 = df0[['Date','League','Home','Away','Goals_H','Goals_A','Goals_Min_H','Goals_Min_A',
                   'Odd_H_Back','Odd_H_Lay','Odd_D_Back','Odd_D_Lay','Odd_A_Back','Odd_A_Lay',
                   'Odd_CS_0x1_Lay','Odd_CS_1x0_Lay','Profit']]
        
        def download_excel():
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df0.to_excel(writer, index=False, sheet_name='Sheet1')
                writer.close()
                processed_data = output.getvalue()
                return processed_data

        button = st.download_button(
        label='Download',
        data=download_excel(),
        file_name=f'Lay_Away.xlsx',
        mime='application/vnd.ms-excel')
        
    elif analysis_choice == "Lay 0 x 0":
        flt = ((df.CV_CS >= 1.6) & (df.CV_CS <= 2) &
           (df.Entropy_CS <= 3.4) &
           (df.Odd_CS_0x0_Lay <= 21))
        df0 = df[flt]
        df0 = drop_reset_index(df0)
        df0['Investimento'] = df0['Odd_CS_0x0_Lay'] - 1
        df0['Profit'] = 0.94
        df0.loc[((df0['Goals_H'] == 0) & (df0['Goals_A'] == 0)), 'Profit'] = -1 * (df0['Odd_CS_0x0_Lay'] - 1)
        df0['Profit_acu'] = df0.Profit.cumsum()
    
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df0.index, y=df0['Profit_acu'], mode='lines'))

        fig.update_layout(
            title="Profit Acumulado",
            xaxis_title="Entradas",
            yaxis_title="Stakes"
        )

        st.plotly_chart(fig)
        plot_profit_acu(df0, 'Lay 0 x 0')
        df0 = df0[['Date','League','Home','Away','Goals_H','Goals_A','Goals_Min_H','Goals_Min_A',
                   'Odd_H_Back','Odd_H_Lay','Odd_D_Back','Odd_D_Lay','Odd_A_Back','Odd_A_Lay',
                   'Odd_CS_0x0_Lay','Odd_CS_0x1_Lay','Odd_CS_1x0_Lay','Profit']]
        
        def download_excel():
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df0.to_excel(writer, index=False, sheet_name='Sheet1')
                writer.close()
                processed_data = output.getvalue()
                return processed_data

        button = st.download_button(
        label='Download',
        data=download_excel(),
        file_name=f'Lay_0x0.xlsx',
        mime='application/vnd.ms-excel')
        
    elif analysis_choice == "Lay 1 x 0":
        flt = ((df.CV_CS >= 0.1) & 
               (df.VAR1 >= 1.8) & (df.VAR1 <= 2.1) & 
               (df.VAR2 >= 40) & (df.VAR2 <= 50) & 
               (df.Odd_CS_1x0_Lay <= 21))
        df0 = df[flt]
        df0 = drop_reset_index(df0)
        df0['Investimento'] = df0['Odd_CS_1x0_Lay'] - 1
        df0['Profit'] = 0.94
        df0.loc[((df0['Goals_H'] == 1) & (df0['Goals_A'] == 0)), 'Profit'] = -1 * (df0['Odd_CS_1x0_Lay'] - 1)
        df0['Profit_acu'] = df0.Profit.cumsum()
    
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df0.index, y=df0['Profit_acu'], mode='lines'))

        fig.update_layout(
            title="Profit Acumulado",
            xaxis_title="Entradas",
            yaxis_title="Stakes"
        )

        st.plotly_chart(fig)
        plot_profit_acu(df0, 'Lay 1 x 0')
        df0 = df0[['Date','League','Home','Away','Goals_H','Goals_A','Goals_Min_H','Goals_Min_A',
                   'Odd_H_Back','Odd_H_Lay','Odd_D_Back','Odd_D_Lay','Odd_A_Back','Odd_A_Lay',
                   'Odd_CS_0x0_Lay','Odd_CS_0x1_Lay','Odd_CS_1x0_Lay','Profit']]
        
        def download_excel():
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df0.to_excel(writer, index=False, sheet_name='Sheet1')
                writer.close()
                processed_data = output.getvalue()
                return processed_data

        button = st.download_button(
        label='Download',
        data=download_excel(),
        file_name=f'Lay_1x0.xlsx',
        mime='application/vnd.ms-excel')
        
        
    elif analysis_choice == "Lay 0 x 1":
        
        flt = ((df.VAR1 <= 1) &
       (df.VAR2 >= -30) & (df.VAR2 <= 0) &
       (df.VAR3 >= 20) & (df.VAR2 <= 50) &
       (df.Odd_CS_0x1_Lay <= 50))
        df0 = df[flt]
        df0 = drop_reset_index(df0)
        df0['Investimento'] = df0['Odd_CS_0x1_Lay'] - 1
        df0['Profit'] = 0.94
        df0.loc[((df0['Goals_H'] == 0) & (df0['Goals_A'] == 1)), 'Profit'] = -1 * (df0['Odd_CS_0x1_Lay'] - 1)
        df0['Profit_acu'] = df0.Profit.cumsum()

    
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df0.index, y=df0['Profit_acu'], mode='lines'))

        fig.update_layout(
            title="Profit Acumulado",
            xaxis_title="Entradas",
            yaxis_title="Stakes"
        )

        st.plotly_chart(fig)
        plot_profit_acu(df0, 'Lay 0 x 1')
        df0 = df0[['Date','League','Home','Away','Goals_H','Goals_A','Goals_Min_H','Goals_Min_A',
                   'Odd_H_Back','Odd_H_Lay','Odd_D_Back','Odd_D_Lay','Odd_A_Back','Odd_A_Lay',
                   'Odd_CS_0x0_Lay','Odd_CS_0x1_Lay','Odd_CS_1x0_Lay','Profit']]
        
        def download_excel():
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df0.to_excel(writer, index=False, sheet_name='Sheet1')
                writer.close()
                processed_data = output.getvalue()
                return processed_data

        button = st.download_button(
        label='Download',
        data=download_excel(),
        file_name=f'Lay_0x1.xlsx',
        mime='application/vnd.ms-excel')
    
    
    
    
    
    
    
    
    
    
    
    
    
