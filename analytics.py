import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Função para carregar o arquivo CSV
def carregar_dados(caminho):
    df = pd.read_csv(caminho)
    return df

# Função para gerar gráfico de entregas por mês e ano
def grafico_entregas(df, ano):
    df_filtrado = df[df['Ano'] == ano]
    df_mensal = df_filtrado.groupby('Mês')['N de viagens'].sum().reset_index()

    # Gerar gráfico
    plt.figure(figsize=(8, 6))
    plt.bar(df_mensal['Mês'], df_mensal['N de viagens'])
    plt.title(f"Quantidade de entregas por mês em {ano}")
    plt.xlabel('Mês')
    plt.ylabel('Quantidade de entregas')
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Carregar os dados
df_andrea = carregar_dados('delivery_andrea.csv')
df_marina = carregar_dados('delivery_marina.csv')

# Caixa de seleção para escolher o ano
ano_selecionado = st.selectbox("Selecione o ano", options=df_andrea['Ano'].unique())

# Layout com duas colunas
col1, col2 = st.columns(2)

# Gráfico para Andréa
with col1:
    st.subheader(f'Andréa - Ano {ano_selecionado}')
    grafico_entregas(df_andrea, ano_selecionado)

# Gráfico para Marina
with col2:
    st.subheader(f'Marina - Ano {ano_selecionado}')
    grafico_entregas(df_marina, ano_selecionado)