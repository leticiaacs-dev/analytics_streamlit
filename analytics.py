import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

##################################### Paginação #####################################

# Definir estado inicial
if "pagina" not in st.session_state:
    st.session_state.pagina = 1

# Função para mudar de página
def mudar_pagina(pagina):
    st.session_state.pagina = pagina

# Criar botões para navegação
col1, col2 = st.columns([1, 1])
if col1.button("⬅ Página Anterior", disabled=st.session_state.pagina == 1):
    mudar_pagina(st.session_state.pagina - 1)

if col2.button("➡ Próxima Página"):
    mudar_pagina(st.session_state.pagina + 1)

##################################### Assuntos #####################################

if st.session_state.pagina == 1:
    st.subheader("Relatório 1: Entregas")
    st.write("Principais KPIs sobre a área de Entregas")

    # Lista ordenada de meses
    ordem_meses = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]

    # Função para carregar o arquivo CSV
    def carregar_dados(caminho):
        df = pd.read_csv(caminho)
        
        # Garantir que "Mês" seja string e padronizar
        df['Mês'] = df['Mês'].astype(str).str.lower().str.strip()
        
        # Garantir que "N de viagens" seja numérico
        df['N de viagens'] = pd.to_numeric(df['N de viagens'], errors='coerce').fillna(0)
        
        return df

    # Função para gerar gráfico de entregas por mês e ano
    def grafico_entregas(df, ano):
        df_filtrado = df[df['Ano'] == ano].dropna(subset=['Mês'])
        
        # Aplicar a ordenação correta dos meses
        df_filtrado['Mês'] = pd.Categorical(df_filtrado['Mês'], categories=ordem_meses, ordered=True)
        
        # Criar DataFrame com todos os meses e preencher com zero quando necessário
        df_mensal = df_filtrado.groupby('Mês', observed=True)['N de viagens'].sum().reindex(ordem_meses, fill_value=0).reset_index()

        # Gerar gráfico
        plt.figure(figsize=(8, 6))
        bars = plt.bar(df_mensal['Mês'], df_mensal['N de viagens'], color='royalblue')
        
        # Adicionar rótulos nas barras
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                plt.text(bar.get_x() + bar.get_width()/2, height, int(height), 
                         ha='center', va='bottom', fontsize=10)

        plt.title(f"Quantidade de entregas por mês em {ano}")
        plt.xlabel('Mês')
        plt.ylabel('Quantidade de entregas')
        plt.ylim(0, 60)  # Definir eixo Y fixo de 0 a 60
        plt.xticks(rotation=45)
        st.pyplot(plt)

    # Carregar os dados
    df_andrea = carregar_dados('extract_csv/delivery_andrea.csv')
    df_marina = carregar_dados('extract_csv/delivery_marina.csv')

    # Caixa de seleção para escolher o ano
    ano_selecionado = st.selectbox("Selecione o ano", options=df_andrea['Ano'].dropna().unique())

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

elif st.session_state.pagina == 2:
    st.subheader("Relatório 2: Página 2")
    st.write("Aqui vão os dados da segunda página.")

elif st.session_state.pagina == 3:
    st.subheader("Relatório 3: Página 3")
    st.write("Aqui vão os dados da terceira página.")