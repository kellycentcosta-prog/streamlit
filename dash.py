import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

#cria um cabeçalho
st.header('Dashboard analítico')

#importa a base de dados
df = pd.read_csv('dados_dash.csv', encoding='latin1')

#=====================================

#  SIDEBAR

#=====================================
#ordena em ordem alfabetica, converte a coluna para string
#e retorna  valores únicos
clientes = sorted(df['cliente_nome'].astype(str).unique())
st.sidebar.title('Filtros')

#filtros por cliente
cliente_selecionado = st.sidebar.multiselect(
    label='Selecione os Clientes',
    options=clientes,
    #default=clientes,#começa com todos os clientes
    
)
#Aplicar o filtro
if cliente_selecionado:
    df_filtrado = df[df['cliente_nome'].astype(str).isin(cliente_selecionado)].copy()
    
else:
    df_filtrado = df.copy()
    
    
    
    
    
#mostrar o DF no dash online
#st.dataframe(df)


#=====================================

#   KPIs 

#=====================================

faturamento_total = df_filtrado['produto_valor'].sum()
media = df_filtrado['produto_valor'].mean()
maximo = df_filtrado['produto_valor'].max()
minimo = df_filtrado['produto_valor'].min()

col1,col2 = st.columns(2)
col3,col4=st.columns(2)

with col1:
    st.metric('Total Faturado', f'R${faturamento_total:,.2f}')
with col2:
    st.metric('Média', f'R${media:,.2f}')
with col3:
    st.metric('Máximo', f'R${maximo:,.2f}')
with col4:
    st.metric('Mínimo', f'R${minimo:,.2f}')


    


#====================================

#  DADOS PARA OS GRÁFICOS

#====================================

graf_dados = df_filtrado.groupby('loja_cidade')['produto_produto'].count()
graf_produto = df_filtrado.groupby('produto_produto')['produto_valor'].count()
graf_faturamento_cidade = df_filtrado.groupby('loja_cidade')['produto_valor'].sum()
graf_faturamento_produto = df_filtrado.groupby('produto_produto')['produto_valor'].sum()
#st.dataframe(graf_faturamento_produto)

#=====================================

#   GRÁFIGOS (2X2)

#=====================================

fig = plt.figure(figsize=(10,7))

#Gráfico 1
plt.subplot(2,2,1)
plt.bar(graf_dados.index,graf_dados.values)
plt.title('Vendas por loja')
plt.xticks(rotation=45)



#Gráfico 2
plt.subplot(2,2,2)
plt.bar(graf_faturamento_cidade.index,graf_faturamento_cidade.values)
plt.title('Faturamento por loja')
plt.xticks(rotation=45)

#Gráfico 3
plt.subplot(2,2,3)
plt.bar(graf_produto.index,graf_produto.values)
plt.title('Vendas por produto')
plt.xticks(rotation=45)

#Gráfico 4
plt.subplot(2,2,4)
plt.bar(graf_faturamento_produto.index,graf_faturamento_produto.values)
plt.title('Faturamento por produto')
plt.xticks(rotation=45)

plt.tight_layout()
st.pyplot(fig)

#Convertendo a coluna para data no pandas
df['pagamento_dt_pgto'] = pd.to_datetime(df['pagamento_dt_pgto'])

df_mes = df.groupby(
    df['pagamento_dt_pgto'].dt.to_period('M')#converte cada data para
#periodo mensal ex: 28/01/24, ->2018/01
)['produto_valor'].sum().reset_index()#reset_index(criar um dataframe)

#converte a coluna de data para str, para plotagem do gráfico(streamlit)
df_mes['pagamento_dt_pgto'] = df_mes['pagamento_dt_pgto'].astype(str)

st.line_chart(df_mes.set_index('pagamento_dt_pgto'))
st.dataframe(df_mes)

#st.white('Esse dashoboar mostra os indicadores de vendas.')
#st.title('Dashboard de Vendas')
st.subheader('Gráfico de Pareto')

#st.white('Esse dashoboar mostra os indicadores de vendas.')
#st.title('Dashboard de Vendas')
#Agrupar Produtos e somar valores
grupo_produto = df_filtrado.groupby('produto_produto')['produto_valor'].sum().reset_index().sort_values(by='produto_valor', ascending=False)

#st.dataframe(grupo_produto)

#Criar gráfico
fig,ax1 =plt.subplots(figsize=(12,6))

#Barras
ax1.bar(grupo_produto["produto_produto"],grupo_produto["produto_valor"])

#linha acumulada
ax2 = ax1.twinx()#Cria um eixo y no lado direito

#Criar A coluna Percentual acumulado
grupo_produto['Perc_Acumulado'] = (
    grupo_produto['produto_valor'].cumsum()/
    grupo_produto['produto_valor'].sum()
    )* 100   
           
#Criar gráfico de linha
ax2.plot(
    grupo_produto['produto_produto'],
    grupo_produto['Perc_Acumulado'],
    marker='o',
    color='red'
)

#Linha de 80%
ax2.axhline(80,linestyle='--')

ax1.tick_params(axis='x', rotation=45)

plt.ylim(0,110)

st.pyplot(fig)

st.subheader('Histograma')

# Criando o DataFrame

df_idade = pd.DataFrame(df_filtrado['idade'])

#st.dataframe(hist_idade)

# Criando o gráfico 

fig = plt.figure(figsize=(10,5))

plt.hist(
    df_idade['idade'],
    bins=5, # Divide os dados em cinco blocos
    edgecolor='black'
             )

plt.title('Distribuição das idades')
plt.xlabel('Idade')
plt.ylabel('Frequência')

plt.grid(axis='y', linestyle='--', alpha=0.3)

st.pyplot(fig)


