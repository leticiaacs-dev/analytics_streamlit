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

# Relatório 1: Entregas
if st.session_state.pagina == 1:
    st.subheader("Relatório 1: Entregas")
    st.write("**Principais KPIs sobre a área de Entregas**")

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

    # Função para calcular os KPIs
    def calcular_kpis(df_andrea, df_marina, mes, ano):
        df_andrea_filtrado = df_andrea[(df_andrea['Ano'] == ano) & (df_andrea['Mês'] == mes)]
        df_marina_filtrado = df_marina[(df_marina['Ano'] == ano) & (df_marina['Mês'] == mes)]
        
        # Total de entregas
        total_entregas = df_andrea_filtrado['N de viagens'].sum() + df_marina_filtrado['N de viagens'].sum()
        
        # Total de KMs rodados
        total_kms = df_andrea_filtrado['TOTAL KM'].sum() + df_marina_filtrado['TOTAL KM'].sum()
        
        # Média de KM por entrega
        media_kms_por_entrega = total_kms / total_entregas if total_entregas > 0 else 0
        
        # Desgaste
        desgaste = df_andrea_filtrado['Valor total'].sum() + df_marina_filtrado['Valor total'].sum()
        
        # Custo por KM
        custo_por_km = desgaste / total_kms if total_kms > 0 else 0
        
        # Custo médio por entrega
        custo_medio_por_entrega = custo_por_km * media_kms_por_entrega
        
        # Cálculo da porcentagem em relação à meta de custo médio por entrega (meta 5)
        if custo_medio_por_entrega > 5:
            porcentagem_meta = ((custo_medio_por_entrega - 5) / 5) * 100  # Quanto é maior que 5
        else:
            porcentagem_meta = ((5 - custo_medio_por_entrega) / 5) * 100  # Quanto é menor que 5

        # Formatando os valores para exibição
        resultados = {
            "Total de entregas": int(total_entregas),
            "Total de KMs rodados": f"{total_kms:.2f}",
            "Média de KM por entrega": f"{media_kms_por_entrega:.2f}",
            "Desgaste R$": f"R$ {desgaste:.2f}",
            "Custo por KM R$": f"R$ {custo_por_km:.2f}",
            "Custo médio por entrega (CME) R$": f"R$ {custo_medio_por_entrega:.2f}",
            "Porcentagem de CME em relação a meta": f"{porcentagem_meta:.2f}%"
        }

        return resultados

    # Carregar os dados
    df_andrea = carregar_dados('extract_csv/delivery_andrea.csv')
    df_marina = carregar_dados('extract_csv/delivery_marina.csv')

    # Caixa de seleção para escolher o ano e o mês
    ano_selecionado = st.selectbox("Selecione o ano", options=df_andrea['Ano'].dropna().unique())
    mes_selecionado = st.selectbox("Selecione o mês", options=ordem_meses)

    # Calcular KPIs
    kpis = calcular_kpis(df_andrea, df_marina, mes_selecionado, ano_selecionado)

    # Exibir KPIs em uma tabela
    kpis_df = pd.DataFrame(list(kpis.items()), columns=["KPI", "Valor"])
    st.table(kpis_df)

    # Exibir a comparação da meta de custo médio por entrega
    custo_medio_por_entrega = float(kpis['Custo médio por entrega (CME) R$'].replace('R$', '').strip())
    porcentagem_meta_valor = float(kpis['Porcentagem de CME em relação a meta'].replace('%', '').strip())

    # Verificar a condição e ajustar o texto da meta
    if custo_medio_por_entrega == 0:
        meta_texto = f"Não temos dados para essa data"
    elif porcentagem_meta_valor > -1:
        meta_texto = f"A meta de CME é de 5.00 reais ou menos (está a {porcentagem_meta_valor:.2f}% acima da meta)"
    else:
        meta_texto = f"A meta de CME é de 5.00 reais ou menos (ótimo, está {porcentagem_meta_valor:.2f}% dentro da meta)"

    # Corrigir a comparação para usar o valor numérico e exibir o texto com a cor apropriada
    if custo_medio_por_entrega > 5 and custo_medio_por_entrega != 0:
        st.markdown(f"<span style='color:red'>{meta_texto}</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span style='color:green'>{meta_texto}</span>", unsafe_allow_html=True)

    # Adicionar uma linha de divisória
    st.markdown("---")

    # Exibir título em negrito
    st.markdown("**Quantidade de entregas e média de KM rodado no mês**")

    # Selecionar o ano usando o selectbox para ambos os DataFrames
    anos_disponiveis = pd.concat([df_andrea['Ano'], df_marina['Ano']]).unique()
    ano_selecionado = st.selectbox("Selecione o ano", options=anos_disponiveis, key="ano_selecionado")

    # Layout com duas colunas para os gráficos
    col1, col2 = st.columns(2)

    # Função para gerar gráfico de entregas por mês e ano
    def grafico_entregas(df, ano):
        df_filtrado = df[df['Ano'] == ano].dropna(subset=['Mês'])
        
        # Aplicar a ordenação correta dos meses
        df_filtrado['Mês'] = pd.Categorical(df_filtrado['Mês'], categories=ordem_meses, ordered=True)
        
        # Criar DataFrame com todos os meses e preencher com zero quando necessário
        df_mensal = df_filtrado.groupby('Mês', observed=True)['N de viagens'].sum().reindex(ordem_meses, fill_value=0).reset_index()

        # Calcular a média de KMs para cada mês
        media_kms_por_mes = df_filtrado.groupby('Mês')['Media Kms'].mean().reindex(ordem_meses, fill_value=0)

        # Gerar gráfico
        plt.figure(figsize=(8, 6))
        bars = plt.bar(df_mensal['Mês'], df_mensal['N de viagens'], color='royalblue', label='Quant. de entregas feitas')
        
        # Adicionar rótulos nas barras, centralizados
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                plt.text(bar.get_x() + bar.get_width()/2, height/2, int(height), 
                         ha='center', va='center', fontsize=10, color='white')

        # Adicionar linha para a média de KMs com pontos conectados
        plt.plot(df_mensal['Mês'], media_kms_por_mes, color='red', marker='o', linestyle='-', lw=2, label='Média de KMs rodados')

        # Adicionar valores nos pontos da linha
        for i, value in enumerate(media_kms_por_mes):
            plt.text(df_mensal['Mês'][i], value, f'{value:.2f}', ha='center', va='bottom', color='red', fontsize=10)

        plt.title(f"Quantidade de entregas por mês em {ano}")
        plt.xlabel('Mês')
        plt.ylabel('Quantidade de entregas')
        plt.ylim(0, 60)  # Definir eixo Y fixo de 0 a 60
        plt.xticks(rotation=45)
        
        # Exibir legenda
        plt.legend(loc='upper left')
        
        st.pyplot(plt)

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