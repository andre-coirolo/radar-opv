# Dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
from . import Functions as fn
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.nonparametric.smoothers_lowess import lowess

def main(df_Qireal, df_Metas, df_ProdRet, df_SLA, df_TMR, df_IS_Final):
    st.title("Radar OPV")
    st.sidebar.title("Painel de Controle")
    # options = ["SUBGRUPO50", "SUBGRUPO48", "SUBGRUPO45"]
    # choice = st.sidebar.radio("Select an option", options)
    
    def filtrar_data(df, i, f):
        df_filtrado = df[(df['Data'] >= pd.to_datetime(i)) & (df['Data'] <= pd.to_datetime(f))]
        return df_filtrado

    def filtrar_mes(df, i, f):
        # transformar i e f em datetime do primeiro dia do mês
        mesano_inicio = pd.Timestamp(year=i.year, month=i.month, day=1)
        mesano_fim = pd.Timestamp(year=f.year, month=f.month, day=1)

        # criar coluna MesAno como datetime
        df = df.copy()
        df['Mes'] = df['Mes'].astype(int)
        df['Ano'] = df['Ano'].astype(int)
        df['MesAno'] = pd.to_datetime(dict(year=df['Ano'], month=df['Mes'], day=1))

        # filtrar pelo intervalo
        df_filtrado = df[(df['MesAno'] >= mesano_inicio) & (df['MesAno'] <= mesano_fim)]
        return df_filtrado

    def filtrar_ano(df, i, f):
        ano_inicio = i.year
        ano_fim = f.year

        df_filtrado = df[(df['Ano'] >= ano_inicio) & (df['Ano'] <= ano_fim)]
        return df_filtrado

    def filtrar_grupos(df, grupos):
        df_filtrado = df[df['Grupo_Vendedor'].isin(grupos)]
        return df_filtrado

    def format_timedelta(td):
        if pd.isnull(td): # Coluna formatada para hover/ticks
            return ""
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    st.set_page_config(
    page_title="Radar OPV",
    layout="wide",
    initial_sidebar_state="expanded"
    )
    
    #-#-#-#-#-# SIDEBAR #-#-#-#-#-#
    
    with st.sidebar:
        st.header("Filtros")
        
        # Período (usa range do ProdRet; aplica aos demais)
        min_date = pd.to_datetime(df_ProdRet["Data"]).min()
        max_date = pd.to_datetime(df_ProdRet["Data"]).max()
        # definir a default_min e default_max
        default_min = pd.Timestamp(year=max_date.year, month=1, day=1)
        default_max = max_date
        # validar se max_date é menor que default_max
        if max_date < default_max:
            default_max = max_date
        # validar se min_date é maior que default_min
        if min_date > default_min:
            default_min = min_date
        # Input das datas no calendário
        date_input = st.date_input(
            "Intervalo de Data",
            value=(default_min, default_max),
            min_value=min_date, max_value=max_date
        )
        # Garante que sempre tenha start_date e end_date válidos (durante a escolha das datas garante que os gráficos não quebrem)
        if isinstance(date_input, tuple) and len(date_input) == 2:
            start_date, end_date = date_input
        else:
            start_date, end_date = default_min, default_max
        
        # Grupos (dinâmico do df_ProdRet, pré-seleciona 3 principais)
        grupos_disponiveis = ["SUBGRUPO48", "SUBGRUPO45", "SUBGRUPO50"]
        default_grupos = ["SUBGRUPO48", "SUBGRUPO45", "SUBGRUPO50"]
        grupos_sel = st.pills("Grupos OPV", grupos_disponiveis, default=default_grupos, selection_mode="multi", width="stretch")
        if grupos_sel == []:
            grupos_sel = grupos_disponiveis

        # Botão Remover TMR > 1 hora
        remover_outlier_tmr = st.toggle("TMR < 01:00:00")
        
    #-#-#-#-#-# Transformações e aplicações de filtros #-#-#-#-#-#
    
    ### Transformar as tabelas com Functions
    
    def transformar_bases(df_ProdRet, df_SLA, df_TMR, df_IS_Final, remover_outlier_tmr):
        # Prod
        df_prod_dia_pessoa, df_prod_mes_pessoa, df_prod_ano_pessoa = fn.Prod_Pessoa(df_ProdRet)
        df_prod_dia_grupo, df_prod_mes_grupo, df_prod_ano_grupo = fn.Prod_Grupo(df_ProdRet)
        df_prod_dia_OPV, df_prod_mes_OPV, df_prod_ano_OPV = fn.Prod_OPV(df_ProdRet)

        # Ret
        df_ret_dia_pessoa, df_ret_mes_pessoa, df_ret_ano_pessoa = fn.Ret_Pessoa(df_ProdRet)
        df_ret_dia_grupo, df_ret_mes_grupo, df_ret_ano_grupo = fn.Ret_Grupo(df_ProdRet)
        df_ret_dia_OPV, df_ret_mes_OPV, df_ret_ano_OPV = fn.Ret_OPV(df_ProdRet)

        # SLA
        df_sla_dia_pessoa, df_sla_mes_pessoa, df_sla_ano_pessoa = fn.SLA_Pessoa(df_SLA)
        df_sla_dia_grupo, df_sla_mes_grupo, df_sla_ano_grupo = fn.SLA_Grupo(df_SLA)
        df_sla_dia_OPV, df_sla_mes_OPV, df_sla_ano_OPV = fn.SLA_OPV(df_SLA)

        # TMR
        df_tmr_dia_pessoa, df_tmr_mes_pessoa, df_tmr_ano_pessoa = fn.TMR_Pessoa(df_TMR, remover_outlier_tmr)
        df_tmr_dia_grupo, df_tmr_mes_grupo, df_tmr_ano_grupo = fn.TMR_Grupo(df_TMR, remover_outlier_tmr)
        df_tmr_dia_OPV, df_tmr_mes_OPV, df_tmr_ano_OPV = fn.TMR_OPV(df_TMR, remover_outlier_tmr)

        # IS
        df_is_dia_pessoa, df_is_mes_pessoa, df_is_ano_pessoa = fn.IS_Pessoa(df_IS_Final)
        df_is_dia_grupo, df_is_mes_grupo, df_is_ano_grupo = fn.IS_Grupo(df_IS_Final)
        df_is_dia_OPV, df_is_mes_OPV, df_is_ano_OPV = fn.IS_OPV(df_IS_Final)
        
        return (
        df_prod_dia_pessoa, df_prod_mes_pessoa, df_prod_ano_pessoa,
        df_prod_dia_grupo, df_prod_mes_grupo, df_prod_ano_grupo,
        df_prod_dia_OPV, df_prod_mes_OPV, df_prod_ano_OPV,
        df_ret_dia_pessoa, df_ret_mes_pessoa, df_ret_ano_pessoa,
        df_ret_dia_grupo, df_ret_mes_grupo, df_ret_ano_grupo,
        df_ret_dia_OPV, df_ret_mes_OPV, df_ret_ano_OPV,
        df_sla_dia_pessoa, df_sla_mes_pessoa, df_sla_ano_pessoa,
        df_sla_dia_grupo, df_sla_mes_grupo, df_sla_ano_grupo,
        df_sla_dia_OPV, df_sla_mes_OPV, df_sla_ano_OPV,
        df_tmr_dia_pessoa, df_tmr_mes_pessoa, df_tmr_ano_pessoa,
        df_tmr_dia_grupo, df_tmr_mes_grupo, df_tmr_ano_grupo,
        df_tmr_dia_OPV, df_tmr_mes_OPV, df_tmr_ano_OPV,
        df_is_dia_pessoa, df_is_mes_pessoa, df_is_ano_pessoa,
        df_is_dia_grupo, df_is_mes_grupo, df_is_ano_grupo,
        df_is_dia_OPV, df_is_mes_OPV, df_is_ano_OPV
    )

    bases = transformar_bases(df_ProdRet, df_SLA, df_TMR, df_IS_Final, remover_outlier_tmr)


    ### Aplicação dos filtros

    def aplicar_filtros(bases, start_date, end_date):
        # Desempacotando variáveis
        (
            df_prod_dia_pessoa, df_prod_mes_pessoa, df_prod_ano_pessoa,
            df_prod_dia_grupo, df_prod_mes_grupo, df_prod_ano_grupo,
            df_prod_dia_OPV, df_prod_mes_OPV, df_prod_ano_OPV,
            df_ret_dia_pessoa, df_ret_mes_pessoa, df_ret_ano_pessoa,
            df_ret_dia_grupo, df_ret_mes_grupo, df_ret_ano_grupo,
            df_ret_dia_OPV, df_ret_mes_OPV, df_ret_ano_OPV,
            df_sla_dia_pessoa, df_sla_mes_pessoa, df_sla_ano_pessoa,
            df_sla_dia_grupo, df_sla_mes_grupo, df_sla_ano_grupo,
            df_sla_dia_OPV, df_sla_mes_OPV, df_sla_ano_OPV,
            df_tmr_dia_pessoa, df_tmr_mes_pessoa, df_tmr_ano_pessoa,
            df_tmr_dia_grupo, df_tmr_mes_grupo, df_tmr_ano_grupo,
            df_tmr_dia_OPV, df_tmr_mes_OPV, df_tmr_ano_OPV,
            df_is_dia_pessoa, df_is_mes_pessoa, df_is_ano_pessoa,
            df_is_dia_grupo, df_is_mes_grupo, df_is_ano_grupo,
            df_is_dia_OPV, df_is_mes_OPV, df_is_ano_OPV
        ) = bases
        
        # Filtros dia
        df_prod_dia_pessoa = filtrar_data(df_prod_dia_pessoa, start_date, end_date)
        df_prod_dia_grupo = filtrar_data(df_prod_dia_grupo, start_date, end_date)
        df_prod_dia_OPV = filtrar_data(df_prod_dia_OPV, start_date, end_date)
        df_ret_dia_pessoa = filtrar_data(df_ret_dia_pessoa, start_date, end_date)
        df_ret_dia_grupo = filtrar_data(df_ret_dia_grupo, start_date, end_date)
        df_ret_dia_OPV = filtrar_data(df_ret_dia_OPV, start_date, end_date)
        df_sla_dia_pessoa = filtrar_data(df_sla_dia_pessoa, start_date, end_date)
        df_sla_dia_grupo = filtrar_data(df_sla_dia_grupo, start_date, end_date)
        df_sla_dia_OPV = filtrar_data(df_sla_dia_OPV, start_date, end_date)
        df_tmr_dia_pessoa = filtrar_data(df_tmr_dia_pessoa, start_date, end_date)
        df_tmr_dia_grupo = filtrar_data(df_tmr_dia_grupo, start_date, end_date)
        df_tmr_dia_OPV = filtrar_data(df_tmr_dia_OPV, start_date, end_date)
        df_is_dia_pessoa = filtrar_data(df_is_dia_pessoa, start_date, end_date)
        df_is_dia_grupo = filtrar_data(df_is_dia_grupo, start_date, end_date)
        df_is_dia_OPV = filtrar_data(df_is_dia_OPV, start_date, end_date)
        
        # Filtros mês
        df_prod_mes_pessoa = filtrar_mes(df_prod_mes_pessoa, start_date, end_date)
        df_prod_mes_grupo = filtrar_mes(df_prod_mes_grupo, start_date, end_date)
        df_prod_mes_OPV = filtrar_mes(df_prod_mes_OPV, start_date, end_date)
        df_ret_mes_pessoa = filtrar_mes(df_ret_mes_pessoa, start_date, end_date)
        df_ret_mes_grupo = filtrar_mes(df_ret_mes_grupo, start_date, end_date)
        df_ret_mes_OPV = filtrar_mes(df_ret_mes_OPV, start_date, end_date)
        df_sla_mes_pessoa = filtrar_mes(df_sla_mes_pessoa, start_date, end_date)
        df_sla_mes_grupo = filtrar_mes(df_sla_mes_grupo, start_date, end_date)
        df_sla_mes_OPV = filtrar_mes(df_sla_mes_OPV, start_date, end_date)
        df_tmr_mes_pessoa = filtrar_mes(df_tmr_mes_pessoa, start_date, end_date)
        df_tmr_mes_grupo = filtrar_mes(df_tmr_mes_grupo, start_date, end_date)
        df_tmr_mes_OPV = filtrar_mes(df_tmr_mes_OPV, start_date, end_date)
        df_is_mes_pessoa = filtrar_mes(df_is_mes_pessoa, start_date, end_date)
        df_is_mes_grupo = filtrar_mes(df_is_mes_grupo, start_date, end_date)
        df_is_mes_OPV = filtrar_mes(df_is_mes_OPV, start_date, end_date)
        
        # Filtro ano
        df_prod_ano_pessoa = filtrar_ano(df_prod_ano_pessoa, start_date, end_date)
        df_prod_ano_grupo = filtrar_ano(df_prod_ano_grupo, start_date, end_date)
        df_prod_ano_OPV = filtrar_ano(df_prod_ano_OPV, start_date, end_date)
        df_ret_ano_pessoa = filtrar_ano(df_ret_ano_pessoa, start_date, end_date)
        df_ret_ano_grupo = filtrar_ano(df_ret_ano_grupo, start_date, end_date)
        df_ret_ano_OPV = filtrar_ano(df_ret_ano_OPV, start_date, end_date)
        df_sla_ano_pessoa = filtrar_ano(df_sla_ano_pessoa, start_date, end_date)
        df_sla_ano_grupo = filtrar_ano(df_sla_ano_grupo, start_date, end_date)
        df_sla_ano_OPV = filtrar_ano(df_sla_ano_OPV, start_date, end_date)
        df_tmr_ano_pessoa = filtrar_ano(df_tmr_ano_pessoa, start_date, end_date)
        df_tmr_ano_grupo = filtrar_ano(df_tmr_ano_grupo, start_date, end_date)
        df_tmr_ano_OPV = filtrar_ano(df_tmr_ano_OPV, start_date, end_date)
        df_is_ano_pessoa = filtrar_ano(df_is_ano_pessoa, start_date, end_date)
        df_is_ano_grupo = filtrar_ano(df_is_ano_grupo, start_date, end_date)
        df_is_ano_OPV = filtrar_ano(df_is_ano_OPV, start_date, end_date)

        return (df_prod_dia_pessoa, df_prod_mes_pessoa, df_prod_ano_pessoa,
                df_prod_dia_grupo, df_prod_mes_grupo, df_prod_ano_grupo,
                df_prod_dia_OPV, df_prod_mes_OPV, df_prod_ano_OPV,
                df_ret_dia_pessoa, df_ret_mes_pessoa, df_ret_ano_pessoa,
                df_ret_dia_grupo, df_ret_mes_grupo, df_ret_ano_grupo,
                df_ret_dia_OPV, df_ret_mes_OPV, df_ret_ano_OPV,
                df_sla_dia_pessoa, df_sla_mes_pessoa, df_sla_ano_pessoa,
                df_sla_dia_grupo, df_sla_mes_grupo, df_sla_ano_grupo,
                df_sla_dia_OPV, df_sla_mes_OPV, df_sla_ano_OPV,
                df_tmr_dia_pessoa, df_tmr_mes_pessoa, df_tmr_ano_pessoa,
                df_tmr_dia_grupo, df_tmr_mes_grupo, df_tmr_ano_grupo,
                df_tmr_dia_OPV, df_tmr_mes_OPV, df_tmr_ano_OPV,
                df_is_dia_pessoa, df_is_mes_pessoa, df_is_ano_pessoa,
                df_is_dia_grupo, df_is_mes_grupo, df_is_ano_grupo,
                df_is_dia_OPV, df_is_mes_OPV, df_is_ano_OPV)

    # Definir todas as bases principais que vamos usar
    (df_prod_dia_pessoa, df_prod_mes_pessoa, df_prod_ano_pessoa,
    df_prod_dia_grupo, df_prod_mes_grupo, df_prod_ano_grupo,
    df_prod_dia_OPV, df_prod_mes_OPV, df_prod_ano_OPV,
    df_ret_dia_pessoa, df_ret_mes_pessoa, df_ret_ano_pessoa,
    df_ret_dia_grupo, df_ret_mes_grupo, df_ret_ano_grupo,
    df_ret_dia_OPV, df_ret_mes_OPV, df_ret_ano_OPV,
    df_sla_dia_pessoa, df_sla_mes_pessoa, df_sla_ano_pessoa,
    df_sla_dia_grupo, df_sla_mes_grupo, df_sla_ano_grupo,
    df_sla_dia_OPV, df_sla_mes_OPV, df_sla_ano_OPV,
    df_tmr_dia_pessoa, df_tmr_mes_pessoa, df_tmr_ano_pessoa,
    df_tmr_dia_grupo, df_tmr_mes_grupo, df_tmr_ano_grupo,
    df_tmr_dia_OPV, df_tmr_mes_OPV, df_tmr_ano_OPV,
    df_is_dia_pessoa, df_is_mes_pessoa, df_is_ano_pessoa,
    df_is_dia_grupo, df_is_mes_grupo, df_is_ano_grupo,
    df_is_dia_OPV, df_is_mes_OPV, df_is_ano_OPV) = aplicar_filtros(bases, start_date, end_date)

    #-#-#-#-#-# PRÉ-ABAS #-#-#-#-#-#

    def tab_produtividade():
        st.subheader("Produtividade")
            
        ##### GRÁFICOS E TABELAS #####

        ### LINHA 1 ###
        
        c1, c2 = st.columns([5,1])
        
        with c1:
            # Gráfico de linhas de 'Produtividade' aberto por 'Data' do OPV
            df_filtrado = df_prod_dia_OPV.copy()
            M300 = 44
            y_max = df_filtrado["Produtividade"].max()*1.1
            fig = px.line(
                df_filtrado,
                x="Data",
                y="Produtividade",
                color_discrete_sequence=["green"],
                title="Produtividade OPV"
            )
            fig.update_layout(title={'x':0.5},
                            legend=dict(
                            orientation="h",      # horizontal
                            yanchor="bottom",     # âncora na parte inferior
                            y=0.95,               # posição vertical (negativo para fora do gráfico)
                            xanchor="center",     # âncora centralizada
                            x=0.95                 # posição horizontal (meio do gráfico)
                            ))
            fig.update_yaxes(range=[0, y_max])

            # Adiciona linha amarela pontilhada no valor M300
            fig.add_trace(
                go.Scatter(
                    x=[df_filtrado["Data"].min(), df_filtrado["Data"].max()],
                    y=[M300, M300],
                    mode="lines",
                    name="Meta M300",
                    line=dict(color="yellow", width=2, dash="dot")
                )
            )

            st.plotly_chart(fig, use_container_width=True, key="prod_chart1")
        
        with c2:
            # um quadro mostrando a média da produtividade OPV do periodo selecionado
            prod_media = df_prod_dia_OPV["Produtividade"].mean()
            meta = 44
            delta = prod_media - meta
            if prod_media >= meta:
                cor_numero = "#21ba45"  # verde
                cor_borda = "#21ba45"
                seta = "&#9650;"  # seta para cima
            else:
                cor_numero = "#db2828"  # vermelho
                cor_borda = "#db2828"
                seta = "&#9660;"  # seta para baixo

            st.markdown(
                f"""
                <div style="
                    height: 100%;
                    min-height: 400px; /* ajuste conforme necessário */
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                ">
                    <div style="
                        background-color: #fff;
                        border-radius: 16px;
                        border: 4px solid {cor_borda};
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        padding: 24px 16px;
                        min-width: 120px;
                        min-height: 180px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                    ">
                        <span style="font-size: 3rem; color: {cor_numero}; font-weight: bold;">{prod_media:.1f}</span>
                        <span style="font-size: 1rem; color: {cor_numero}; font-weight: bold;">
                            {seta} {delta:+.1f}
                        </span>
                        <span style="font-size: 1rem; color: #aaa;">Meta: {meta}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        ### LINHA 2 ###
        
        # Gráfico de linhas de 'Produtividade' aberto por 'Data' e 'Grupo_Vendedor'
        df_filtrado = df_prod_dia_grupo.copy()
        df_filtrado = filtrar_grupos(df_filtrado, grupos_sel)

        fig = px.line(
            df_filtrado,
            x="Data",
            y="Produtividade",
            color="Grupo_Vendedor",
            title="Produtividade por Data e Grupo"
        )
        fig.update_layout(title={'x':0.4})  # Centraliza o título
        fig.update_yaxes(range=[0, df_filtrado["Produtividade"].max()*1.1])  # Eixo Y começa em 0
        st.plotly_chart(fig, use_container_width=True, key="prod_chart2")
        
        ### LINHA 3 ###
        
        # Gráfico Barras Laterais Ranking Produtividade média por mês por pessoa, ordenado do maior para o menor
        st.subheader("Média de Produtividade por Analista")
        c1, c2, c3 = st.columns([1,1,1])
        
        # Filtrar df_prod_dia_pessoa pelo período selecionado
        df_filtrado = df_prod_dia_pessoa.copy()
        
        with c1:
            # Filtrar o grupo 'SUBGRUPO50'
            df1 = df_filtrado[df_filtrado["Grupo_Vendedor"] == "SUBGRUPO50"]
            
            # Calcular média de produtividade por analista
            df_media = df1.groupby("Tratado_Por")["Produtividade"].mean().sort_values(ascending=True).reset_index()
            
            # Gráfico de barra lateral
            fig_bar = px.bar(
                df_media,
                x="Produtividade",
                y="Tratado_Por",
                orientation="h",
                title="SUBGRUPO50",
                text="Produtividade"
            )
            fig_bar.update_traces(
                textposition="inside",  # Coloca o texto dentro da barra
                insidetextanchor="end",  # Fixa o texto na extremidade mais distante da base
                texttemplate='%{x:.1f}'
            )
            fig_bar.update_layout(title={'x':0.5})  # Centraliza o título
            st.plotly_chart(fig_bar, use_container_width=True, key="prod_chart3")
        
        with c2:

            # Filtrar o 'SUBGRUPO48'
            df2 = df_filtrado[df_filtrado["Grupo_Vendedor"] == "SUBGRUPO48"]
                        
            # Calcular média de produtividade por analista
            df_media = df2.groupby("Tratado_Por")["Produtividade"].mean().sort_values(ascending=True).reset_index()
            
            # Gráfico de barra lateral
            fig_bar = px.bar(
                df_media,
                x="Produtividade",
                y="Tratado_Por",
                orientation="h",
                title="SUBGRUPO48",
                text="Produtividade"
            )
            fig_bar.update_traces(
                textposition="inside",  # Coloca o texto dentro da barra
                insidetextanchor="end",  # Fixa o texto na extremidade mais distante da base
                texttemplate='%{x:.1f}'
            )
            fig_bar.update_layout(title={'x':0.5})  # Centraliza o título
            st.plotly_chart(fig_bar, use_container_width=True, key="prod_chart4")
            
        with c3:

            # Filtrar o grupo 'SUBGRUPO45'
            df3 = df_filtrado[df_filtrado["Grupo_Vendedor"] == "SUBGRUPO45"]
            
            # Calcular média de produtividade por analista
            df_media = df3.groupby("Tratado_Por")["Produtividade"].mean().sort_values(ascending=True).reset_index()
            
            # Gráfico de barra lateral
            fig_bar = px.bar(
                df_media,
                x="Produtividade",
                y="Tratado_Por",
                orientation="h",
                title="SUBGRUPO45",
                text="Produtividade"
            )
            fig_bar.update_traces(
                textposition="inside",  # Coloca o texto dentro da barra
                insidetextanchor="end",  # Fixa o texto na extremidade mais distante da base
                texttemplate='%{x:.1f}'
            )
            fig_bar.update_layout(title={'x':0.5})  # Centraliza o título
            st.plotly_chart(fig_bar, use_container_width=True, key="prod_chart5")
        
        ### LINHA 4 ###
        
        # Produção por Dia
        st.subheader("Base Produção por Dia por Pessoa")

        # Tabela de Produção por Dia
        df = df_prod_dia_pessoa.copy()
        df = filtrar_data(df, start_date, end_date)
        df = filtrar_grupos(df, grupos_sel)
        st.write(df)

    def tab_retrabalho():
        st.subheader("Retrabalho")
        st.badge("⚠️ Essa aba ainda está sob validação de dados!", color="orange")
        ##### GRÁFICOS E TABELAS #####

        ### LINHA 1 ###
        
        c1, c2 = st.columns([5,1])
        
        st.badge("Em breve um botão para selecionar o delta de tempo de suavização da curva (7, 20, 60, 120, 360)", color="blue")
        
        with c1:
            df_filtrado = df_ret_dia_OPV.copy()
            # Criar indicador 'Retrabalho (%)' (Evita divisão por zero)
            df_filtrado["Retrabalho (%)"] = np.where(
                df_filtrado["Produtividade"] != 0,
                (df_filtrado["Retrabalho"] / df_filtrado["Produtividade"]) * 100,
                np.nan
            )
            # Gráfico de linhas de 'Retrabalho' aberto por 'Data' do OPV
            M300 = 13.3
            y_max = df_filtrado["Retrabalho (%)"].max()*1.1
            if M300 > y_max:
                y_max = M300 * 1.1
            fig = px.line(
                df_filtrado,
                x="Data",
                y="Retrabalho (%)",
                color_discrete_sequence=["green"],
                title="Retrabalho OPV"
            )
            fig.update_layout(title={'x':0.5},
                            legend=dict(
                            orientation="h",      # horizontal
                            yanchor="bottom",     # âncora na parte inferior
                            y=0.95,               # posição vertical (negativo para fora do gráfico)
                            xanchor="center",     # âncora centralizada
                            x=0.85                 # posição horizontal (meio do gráfico)
                            ))
            fig.update_yaxes(range=[0, y_max])

            # Adiciona linha amarela pontilhada no valor M300
            fig.add_trace(
                go.Scatter(
                    x=[df_filtrado["Data"].min(), df_filtrado["Data"].max()],
                    y=[M300, M300],
                    mode="lines",
                    name="Meta M300",
                    line=dict(color="yellow", width=2, dash="dot")
                )
            )
            
            # Adiciona linha de tendência dos últimos n dias
            n_dias = 120
            df_tendencia = df_filtrado.sort_values("Data").tail(n_dias)

            if len(df_tendencia) > 2:
                x_num = (df_tendencia["Data"] - df_tendencia["Data"].min()).dt.days
                y = df_tendencia["Retrabalho (%)"]
                # LOWESS suavização
                lowess_result = lowess(y, x_num, frac=0.5)
                fig.add_trace(
                    go.Scatter(
                        x=[df_tendencia["Data"].iloc[int(i)] for i in range(len(lowess_result))],
                        y=lowess_result[:, 1],
                        mode="lines",
                        name=f"Tendência Suavizada {n_dias} dias (LOWESS)",
                        line=dict(color="red", dash="dot")
                    )
                )

            st.plotly_chart(fig, use_container_width=True, key="ret_chart1")
            
        with c2:
            df_filtrado = df_ret_dia_OPV.copy()
            # Agrupa tudo em uma única linha somando 'Produtividade' e 'Retrabalho'
            df_agrupado = df_filtrado[['Produtividade', 'Retrabalho']].sum().to_frame().T
            # Criar indicador 'Retrabalho (%)' (Evita divisão por zero)
            df_agrupado["Retrabalho (%)"] = np.where(
                df_agrupado["Produtividade"] != 0,
                (df_agrupado["Retrabalho"] / df_agrupado["Produtividade"]) * 100,
                np.nan
            )
            # um quadro mostrando a média da produtividade OPV do periodo selecionado
            prod_media = df_agrupado["Retrabalho (%)"].mean()
            M300 = 13.3
            delta = prod_media - M300
            if prod_media <= M300:
                cor_numero = "#21ba45"  # verde
                cor_borda = "#21ba45"
                seta = "&#9660;"  # seta para cima
            else:
                cor_numero = "#db2828"  # vermelho
                cor_borda = "#db2828"
                seta = "&#9650;"  # seta para baixo

            st.markdown(
                f"""
                <div style="
                    height: 100%;
                    min-height: 400px; /* ajuste conforme necessário */
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                ">
                    <div style="
                        background-color: #fff;
                        border-radius: 16px;
                        border: 4px solid {cor_borda};
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        padding: 24px 16px;
                        min-width: 120px;
                        min-height: 180px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                    ">
                        <span style="font-size: 3rem; color: {cor_numero}; font-weight: bold;">{prod_media:.1f}</span>
                        <span style="font-size: 1rem; color: {cor_numero}; font-weight: bold;">
                            {seta} {delta:+.1f}
                        </span>
                        <span style="font-size: 1rem; color: #aaa;">Meta: {M300}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        ### LINHA 2 ###
        
        df_filtrado = df_ret_dia_grupo.copy()
        df_filtrado = filtrar_grupos(df_filtrado, grupos_sel)
        
        # Criar indicador 'Retrabalho (%)' (Evita divisão por zero)
        df_filtrado["Retrabalho (%)"] = np.where(
            df_filtrado["Produtividade"] != 0,
            (df_filtrado["Retrabalho"] / df_filtrado["Produtividade"]) * 100,
            np.nan
        )

        fig = px.line(
            df_filtrado,
            x="Data",
            y="Retrabalho (%)",
            color="Grupo_Vendedor",
            title="Retrabalho por Data e Grupo"
        )
        fig.update_layout(title={'x':0.4})  # Centraliza o título
        fig.update_yaxes(range=[0, df_filtrado["Retrabalho (%)"].max()*1.1])  # Eixo Y começa em 0
        st.plotly_chart(fig, use_container_width=True, key="ret_chart2")
        
        ### LINHA 3 ###
        
        # Gráfico Barras Laterais Ranking Produtividade média por mês por pessoa, ordenado do maior para o menor
        st.subheader("Média de Retrabalho por Analista")
        c1, c2, c3 = st.columns([1,1,1])
        
        # Filtrar df_prod_dia_pessoa pelo período selecionado
        df_filtrado = df_ret_dia_pessoa.copy()
        
        with c1:
            # Filtrar o grupo 'SUBGRUPO50'
            df1 = df_filtrado[df_filtrado["Grupo_Vendedor"] == "SUBGRUPO50"]
            
            # Calcular média de produtividade e retrabalho por analista
            df_media = df1.groupby("Tratado_Por")[["Produtividade","Retrabalho"]].sum().reset_index()
            
            # Criar indicador 'Retrabalho (%)' (Evita divisão por zero)
            df_media["Retrabalho (%)"] = np.where(
                df_media["Produtividade"] != 0,
                (df_media["Retrabalho"] / df_media["Produtividade"]) * 100,
                np.nan
            )
            
            # Ordenar por Retrabalho (%)
            df_media = df_media.sort_values(by="Retrabalho (%)", ascending=False)

            # Gráfico de barra lateral
            fig_bar = px.bar(
                df_media,
                x="Retrabalho (%)",
                y="Tratado_Por",
                orientation="h",
                title="SUBGRUPO50",
                text="Retrabalho (%)"
            )
            fig_bar.update_traces(
                textposition="inside",  # Coloca o texto dentro da barra
                insidetextanchor="end",  # Fixa o texto na extremidade mais distante da base
                texttemplate='%{x:.1f}%'
            )
            fig_bar.update_layout(title={'x':0.5})  # Centraliza o título
            st.plotly_chart(fig_bar, use_container_width=True, key="ret_chart3")
        
        with c2:

            # Filtrar o grupo 'SUBGRUPO48'
            df2 = df_filtrado[df_filtrado["Grupo_Vendedor"] == "SUBGRUPO48"]
                        
            # Calcular média de produtividade e retrabalho por analista
            df_media = df2.groupby("Tratado_Por")[["Produtividade","Retrabalho"]].sum().reset_index()
            
            # Criar indicador 'Retrabalho (%)' (Evita divisão por zero)
            df_media["Retrabalho (%)"] = np.where(
                df_media["Produtividade"] != 0,
                (df_media["Retrabalho"] / df_media["Produtividade"]) * 100,
                np.nan
            )
            
            # Ordenar por Retrabalho (%)
            df_media = df_media.sort_values(by="Retrabalho (%)", ascending=False)

            # Gráfico de barra lateral
            fig_bar = px.bar(
                df_media,
                x="Retrabalho (%)",
                y="Tratado_Por",
                orientation="h",
                title="SUBGRUPO48",
                text="Retrabalho (%)"
            )
            fig_bar.update_traces(
                textposition="inside",  # Coloca o texto dentro da barra
                insidetextanchor="end",  # Fixa o texto na extremidade mais distante da base
                texttemplate='%{x:.1f}%'
            )
            fig_bar.update_layout(title={'x':0.5})  # Centraliza o título
            st.plotly_chart(fig_bar, use_container_width=True, key="ret_chart4")
            
        with c3:

            # Filtrar o grupo 'SUBGRUPO45'
            df3 = df_filtrado[df_filtrado["Grupo_Vendedor"] == "SUBGRUPO45"]
            
            # Calcular média de produtividade e retrabalho por analista
            df_media = df3.groupby("Tratado_Por")[["Produtividade","Retrabalho"]].sum().reset_index()
            
            # Criar indicador 'Retrabalho (%)' (Evita divisão por zero)
            df_media["Retrabalho (%)"] = np.where(
                df_media["Produtividade"] != 0,
                (df_media["Retrabalho"] / df_media["Produtividade"]) * 100,
                np.nan
            )
            
            # Ordenar por Retrabalho (%)
            df_media = df_media.sort_values(by="Retrabalho (%)", ascending=False)

            # Gráfico de barra lateral
            fig_bar = px.bar(
                df_media,
                x="Retrabalho (%)",
                y="Tratado_Por",
                orientation="h",
                title="SUBGRUPO45",
                text="Retrabalho (%)"
            )
            fig_bar.update_traces(
                textposition="inside",  # Coloca o texto dentro da barra
                insidetextanchor="end",  # Fixa o texto na extremidade mais distante da base
                texttemplate='%{x:.1f}%'
            )
            fig_bar.update_layout(title={'x':0.5})  # Centraliza o título
            st.plotly_chart(fig_bar, use_container_width=True, key="ret_chart5")
        
        ### LINHA 3 ###
        
        # Retrabalho por Dia
        st.subheader("Base Retrabalho por Dia por Pessoa")

        df_filtrado = df_ret_dia_pessoa.copy()
        st.write(df_filtrado)

    def tab_sla():
        st.subheader("SLA")
        
        ##### GRÁFICOS E TABELAS #####

        ### LINHA 1 ###

        c1, c2 = st.columns([5,1])
        
        with c1:
            df_filtrado = df_sla_dia_OPV.copy()
            # Criar indicador 'SLA (%)' (Evita divisão por zero)
            df_filtrado["SLA (%)"] = np.where(
                df_filtrado["Etapas_Concluidas"] != 0,
                (df_filtrado["Etapas_Prazo"] / df_filtrado["Etapas_Concluidas"]) * 100,
                np.nan
            )
            # Gráfico de linhas de 'SLA' aberto por 'Data' do OPV
            M300 = 95.0
            if 100 > df_filtrado["SLA (%)"].max()*1.1:
                y_max = df_filtrado["SLA (%)"].max()*1.1
            else:
                y_max = 100
            y_min = df_filtrado["SLA (%)"].min()*0.95
            if M300 > y_max:
                y_max = M300 * 1.1
            if M300 < y_min:
                y_min = M300 * 0.9
            fig = px.line(
                df_filtrado,
                x="Data",
                y="SLA (%)",
                color_discrete_sequence=["green"],
                title="SLA OPV"
            )
            fig.update_layout(title={'x':0.5},
                            legend=dict(
                            orientation="h",      # horizontal
                            yanchor="bottom",     # âncora na parte inferior
                            y=0.95,               # posição vertical (negativo para fora do gráfico)
                            xanchor="center",     # âncora centralizada
                            x=0.95                 # posição horizontal (meio do gráfico)
                            ))
            fig.update_yaxes(range=[y_min, y_max])

            # Adiciona linha amarela pontilhada no valor M300
            fig.add_trace(
                go.Scatter(
                    x=[df_filtrado["Data"].min(), df_filtrado["Data"].max()],
                    y=[M300, M300],
                    mode="lines",
                    name="Meta M300",
                    line=dict(color="yellow", width=2, dash="dot")
                )
            )
            
            st.plotly_chart(fig, use_container_width=True, key="sla_chart1")
            
        with c2:
            df_filtrado = df_sla_dia_OPV.copy()
            # Agrupa tudo em uma única linha somando 'Etapas_Concluidas' e 'Etapas_Prazo'
            df_agrupado = df_filtrado[['Etapas_Concluidas', 'Etapas_Prazo']].sum().to_frame().T
            # Criar indicador 'SLA (%)' (Evita divisão por zero)
            df_agrupado["SLA (%)"] = np.where(
                df_agrupado["Etapas_Prazo"] != 0,
                (df_agrupado["Etapas_Prazo"] / df_agrupado["Etapas_Concluidas"]) * 100,
                np.nan
            )
            # um quadro mostrando a média da produtividade OPV do periodo selecionado
            prod_media = df_agrupado["SLA (%)"].mean()
            M300 = 95.0
            delta = prod_media - M300
            if prod_media >= M300:
                cor_numero = "#21ba45"  # verde
                cor_borda = "#21ba45"
                seta = "&#9650;"  # seta para cima
            else:
                cor_numero = "#db2828"  # vermelho
                cor_borda = "#db2828"
                seta = "&#9660;"  # seta para baixo

            st.markdown(
                f"""
                <div style="
                    height: 100%;
                    min-height: 400px; /* ajuste conforme necessário */
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                ">
                    <div style="
                        background-color: #fff;
                        border-radius: 16px;
                        border: 4px solid {cor_borda};
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        padding: 24px 16px;
                        min-width: 120px;
                        min-height: 180px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                    ">
                        <span style="font-size: 3rem; color: {cor_numero}; font-weight: bold;">{prod_media:.1f}</span>
                        <span style="font-size: 1rem; color: {cor_numero}; font-weight: bold;">
                            {seta} {delta:+.1f}
                        </span>
                        <span style="font-size: 1rem; color: #aaa;">Meta: {M300}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        ### LINHA 2 ###
        
        df_filtrado = df_sla_dia_grupo.copy()
        df_filtrado = filtrar_grupos(df_filtrado, grupos_sel)
        
        # Criar indicador 'SLA (%)' (Evita divisão por zero)
        df_filtrado["SLA (%)"] = np.where(
            df_filtrado["Etapas_Concluidas"] != 0,
            (df_filtrado["Etapas_Prazo"] / df_filtrado["Etapas_Concluidas"]) * 100,
            np.nan
        )

        # achar o menor ponto de SLA (%)
        y_min = df_filtrado["SLA (%)"].min()*0.95

        fig = px.line(
            df_filtrado,
            x="Data",
            y="SLA (%)",
            color="Grupo_Vendedor",
            title="SLA por Data e Grupo"
        )
        fig.update_layout(title={'x':0.4})  # Centraliza o título
        fig.update_yaxes(range=[y_min, 100])  # Eixo Y começa em 0
        st.plotly_chart(fig, use_container_width=True, key="sla_chart2")
        
        ### LINHA 3 ###
        
        # Gráfico Barras Laterais Ranking Produtividade média por mês por pessoa, ordenado do maior para o menor
        st.subheader("Média de SLA (%) por Analista")
        
        c1, c2, c3 = st.columns([1,1,1])
        
        # Filtrar df_prod_dia_pessoa pelo período selecionado
        df_filtrado = df_sla_dia_pessoa.copy()

        with c1:
            # Filtrar o grupo 'SUBGRUPO50'
            df1 = df_filtrado[df_filtrado["Grupo_Vendedor"] == "SUBGRUPO50"]
            
            # Calcular média de produtividade e retrabalho por analista
            df_media = df1.groupby("Tratado_Por")[["Etapas_Concluidas","Etapas_Prazo"]].sum().reset_index()

            # Criar indicador 'SLA (%)' (Evita divisão por zero)
            df_media["SLA (%)"] = np.where(
                df_media["Etapas_Concluidas"] != 0,
                (df_media["Etapas_Prazo"] / df_media["Etapas_Concluidas"]) * 100,
                np.nan
            )

            # Ordenar por SLA (%)
            df_media = df_media.sort_values(by="SLA (%)", ascending=True)

            # Gráfico de barra lateral
            fig_bar = px.bar(
                df_media,
                x="SLA (%)",
                y="Tratado_Por",
                orientation="h",
                title="SUBGRUPO50",
                text="SLA (%)"
            )
            fig_bar.update_traces(
                textposition="inside",  # Coloca o texto dentro da barra
                insidetextanchor="end",  # Fixa o texto na extremidade mais distante da base
                texttemplate='%{x:.1f}%'
            )
            fig_bar.update_layout(title={'x':0.5})  # Centraliza o título
            st.plotly_chart(fig_bar, use_container_width=True, key="sla_chart3")
        
        with c2:

            # Filtrar o grupo 'SUBGRUPO48'
            df2 = df_filtrado[df_filtrado["Grupo_Vendedor"] == "SUBGRUPO48"]
                        
            # Calcular média de produtividade e retrabalho por analista
            df_media = df2.groupby("Tratado_Por")[["Etapas_Concluidas","Etapas_Prazo"]].sum().reset_index()

            # Criar indicador 'SLA (%)' (Evita divisão por zero)
            df_media["SLA (%)"] = np.where(
                df_media["Etapas_Concluidas"] != 0,
                (df_media["Etapas_Prazo"] / df_media["Etapas_Concluidas"]) * 100,
                np.nan
            )

            # Ordenar por SLA (%)
            df_media = df_media.sort_values(by="SLA (%)", ascending=True)

            # Gráfico de barra lateral
            fig_bar = px.bar(
                df_media,
                x="SLA (%)",
                y="Tratado_Por",
                orientation="h",
                title="SUBGRUPO48",
                text="SLA (%)"
            )
            fig_bar.update_traces(
                textposition="inside",  # Coloca o texto dentro da barra
                insidetextanchor="end",  # Fixa o texto na extremidade mais distante da base
                texttemplate='%{x:.1f}%'
            )
            fig_bar.update_layout(title={'x':0.5})  # Centraliza o título
            st.plotly_chart(fig_bar, use_container_width=True, key="sla_chart4")
            
        with c3:

            # Filtrar o grupo 'SUBGRUPO45'
            df3 = df_filtrado[df_filtrado["Grupo_Vendedor"] == "SUBGRUPO45"]
            
            # Calcular média de Etapas Concluidas e Etapas no prazo por analista
            df_media = df3.groupby("Tratado_Por")[["Etapas_Concluidas","Etapas_Prazo"]].sum().reset_index()

            # Criar indicador 'SLA (%)' (Evita divisão por zero)
            df_media["SLA (%)"] = np.where(
                df_media["Etapas_Concluidas"] != 0,
                (df_media["Etapas_Prazo"] / df_media["Etapas_Concluidas"]) * 100,
                np.nan
            )

            # Ordenar por SLA (%)
            df_media = df_media.sort_values(by="SLA (%)", ascending=True)

            # Gráfico de barra lateral
            fig_bar = px.bar(
                df_media,
                x="SLA (%)",
                y="Tratado_Por",
                orientation="h",
                title="SUBGRUPO45",
                text="SLA (%)"
            )
            fig_bar.update_traces(
                textposition="inside",  # Coloca o texto dentro da barra
                insidetextanchor="end",  # Fixa o texto na extremidade mais distante da base
                texttemplate='%{x:.1f}%'
            )
            fig_bar.update_layout(title={'x':0.5})  # Centraliza o título
            st.plotly_chart(fig_bar, use_container_width=True, key="sla_chart5")
        
        ### LINHA 3 ###

        # SLA por Dia
        st.subheader("Base SLA por Dia por Pessoa")

        df_filtrado = df_sla_dia_pessoa.copy()
        st.write(df_filtrado)

    def tab_tmr():
        st.subheader("TMR")
        
        ##### GRÁFICOS E TABELAS #####

        ### LINHA 1 ###
        
        df_filtrado = df_tmr_dia_OPV.copy()
       
        # Agrupa por Data somando Qtd_Etapas e TMR_Horas
        df_filtrado = df_filtrado.groupby("Data")[["Qtd_Etapas", "TMR_Horas"]].sum().reset_index()

        # Converte 'TMR_Horas' para timedelta
        df_filtrado["TMR_Horas"] = pd.to_timedelta(
            df_filtrado["TMR_Horas"],
            unit="h"
        )

        # Calcula TMR médio por etapa (timedelta)
        df_filtrado["TMR_medio_td"] = (df_filtrado["TMR_Horas"] / df_filtrado["Qtd_Etapas"]).where(
            df_filtrado["Qtd_Etapas"] != 0, pd.NaT
        )

        # Coluna numérica para gráfico (em horas)
        df_filtrado["TMR_medio_horas"] = df_filtrado["TMR_medio_td"] / pd.Timedelta(hours=1)

        df_filtrado["TMR_medio_fmt"] = df_filtrado["TMR_medio_td"].apply(format_timedelta)

        df_final_tmr = df_filtrado.copy()
        
        c1, c2 = st.columns([5,1])
        
        with c1:
            
            df_filtrado = df_final_tmr.copy()

            # Define limites do eixo Y
            y_max = df_filtrado["TMR_medio_horas"].max() * 1.1

            # Cria gráfico
            fig = px.line(
                df_filtrado,
                x="Data",
                y="TMR_medio_horas",  # coluna numérica!
                title="TMR OPV",
                hover_data={"TMR_medio_fmt": True}  # mostra formatado no hover
            )

            fig.update_layout(title={'x':0.5})
            fig.update_yaxes(
                range=[0, y_max],
                title="TMR (h)",
                tickformat=".2f"
            )

            # Opcional: mostra ticks formatados (apenas alguns para não poluir)
            num_ticks = 6
            ticks = np.linspace(0, y_max, num_ticks)
            tick_labels = [format_timedelta(pd.Timedelta(hours=t)) for t in ticks]
            fig.update_yaxes(tickvals=ticks, ticktext=tick_labels)

            st.plotly_chart(fig, use_container_width=True, key="tmr_chart1")
            
            
        with c2:
            # Quadro mostrando TMR médio formatado e delta em relação à meta
            tmr_medio_td = df_final_tmr["TMR_medio_td"].mean()
            tmr_medio_fmt = format_timedelta(tmr_medio_td)
            meta_td = pd.Timedelta(hours=1/12)
            meta_fmt = format_timedelta(meta_td)
            delta_td = tmr_medio_td - meta_td
            delta_horas = delta_td.total_seconds() / 3600 if pd.notnull(delta_td) else np.nan
            if tmr_medio_td <= meta_td:
                cor_numero = "#21ba45"  # verde
                cor_borda = "#21ba45"
                seta = "&#9660;"  # seta para baixo
            else:
                cor_numero = "#db2828"  # vermelho
                cor_borda = "#db2828"
                seta = "&#9650;"  # seta para cima

            st.markdown(
                f"""
                <div style="
                    height: 100%;
                    min-height: 400px; /* ajuste conforme necessário */
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                ">
                    <div style="
                        background-color: #fff;
                        border-radius: 16px;
                        border: 4px solid {cor_borda};
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        padding: 24px 16px;
                        min-width: 120px;
                        min-height: 180px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                    ">
                        <span style="font-size: 3rem; color: {cor_numero}; font-weight: bold;">{tmr_medio_fmt}</span>
                        <span style="font-size: 1rem; color: {cor_numero}; font-weight: bold;">
                            {seta} {delta_horas:+.2f}h
                        </span>
                        <span style="font-size: 1rem; color: #aaa;">Meta: {meta_fmt}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        ### LINHA 2 ###
        
        st.write(df_final_tmr)

    def tab_is():



        st.header("Índice de Solução")
        ##### GRÁFICOS E TABELAS #####

        # Criar indicador 'IS (%)' (Evita divisão por zero)
        df_filtrado = df_is_dia_OPV.copy()
        
        ### LINHA 1 ###
        c1, c2 = st.columns([5,1])
        with c1:
            # Gráfico de Índice de Solução Diário (%) por Total

            df_filtrado = df_is_mes_OPV.copy()
            # Filtrar apenas linhas válidas
            df_valid = df_filtrado[df_filtrado["NPS_Resolvido"].isin(["Sim", "Não"])]
            # Agrupar por MesAno, Canal e NPS_Resolvido, somando Contador
            df_sum = df_valid.groupby(["MesAno", "NPS_Resolvido"], as_index=False)["Contador"].sum()
            # Pivot para Sim/Não
            df_pivot = df_sum.pivot_table(index=["MesAno"], columns="NPS_Resolvido", values="Contador", fill_value=0).reset_index()
            # Calcular IS (%) por mês
            df_pivot["IS (%)"] = np.where(
                (df_pivot.get("Sim", 0) + df_pivot.get("Não", 0)) != 0,
                df_pivot.get("Sim", 0) / (df_pivot.get("Sim", 0) + df_pivot.get("Não", 0)) * 100,
                np.nan
            )
            # Calcular linha total (independente do canal)
            df_total = df_sum.groupby(["MesAno", "NPS_Resolvido"], as_index=False)["Contador"].sum()
            df_total_pivot = df_total.pivot_table(index="MesAno", columns="NPS_Resolvido", values="Contador", fill_value=0).reset_index()
            df_total_pivot["IS (%)"] = np.where(
                (df_total_pivot.get("Sim", 0) + df_total_pivot.get("Não", 0)) != 0,
                df_total_pivot.get("Sim", 0) / (df_total_pivot.get("Sim", 0) + df_total_pivot.get("Não", 0)) * 100,
                np.nan
            )
            # Gráfico de barras do total (sem abertura por canal)
            fig = px.bar(
                df_pivot,
                x="MesAno",
                y="IS (%)",
                title="Índice de Solução Mensal (%) - Total"
            )
            # Linha de referência horizontal 85%
            fig.add_shape(
                type="line",
                x0=min(df_total_pivot["MesAno"]),
                x1=max(df_total_pivot["MesAno"]),
                y0=85,
                y1=85,
                line=dict(color="yellow", width=2, dash="dot"),
                xref="x",
                yref="y"
            )
            fig.update_layout(
                xaxis_title="Mês/Ano",
                yaxis_title="IS (%)",
                yaxis=dict(range=[0, 100], tickformat=".0f%%"),
                template="plotly_white",
                legend=dict(orientation="h", x=0.5, xanchor="center", y=1.1),
                margin=dict(l=40, r=40, t=60, b=40)
            )
            st.plotly_chart(fig, use_container_width=True, key="is_chart1")
        
        with c2:
            # Quadro mostrando a média do índice de solução mensal
            is_media = df_pivot["IS (%)"].mean()
            meta = 85
            delta = is_media - meta
            if is_media >= meta:
                cor_numero = "#21ba45"  # verde
                cor_borda = "#21ba45"
                seta = "&#9650;"  # seta para cima
            else:
                cor_numero = "#db2828"  # vermelho
                cor_borda = "#db2828"
                seta = "&#9660;"  # seta para baixo

            st.markdown(
                f"""
                <div style="
                    height: 100%;
                    min-height: 400px; /* ajuste conforme necessário */
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                ">
                    <div style="
                        background-color: #fff;
                        border-radius: 16px;
                        border: 4px solid {cor_borda};
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        padding: 24px 16px;
                        min-width: 120px;
                        min-height: 180px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                    ">
                        <span style="font-size: 3rem; color: {cor_numero}; font-weight: bold;">{is_media:.1f}%</span>
                        <span style="font-size: 1rem; color: {cor_numero}; font-weight: bold;">
                            {seta} {delta:+.1f}
                        </span>
                        <span style="font-size: 1rem; color: #aaa;">Meta: {meta}%</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        ### LINHA 2 ###

        # Gráfico de Índice de Solução Diário (%) por canal

        df_filtrado = df_is_mes_OPV.copy()
        # Filtrar apenas linhas válidas
        df_valid = df_filtrado[df_filtrado["NPS_Resolvido"].isin(["Sim", "Não"])]
        # Agrupar por MesAno, Canal e NPS_Resolvido, somando Contador
        df_sum = df_valid.groupby(["MesAno", "Canal", "NPS_Resolvido"], as_index=False)["Contador"].sum()
        # Pivot para Sim/Não
        df_pivot = df_sum.pivot_table(index=["MesAno", "Canal"], columns="NPS_Resolvido", values="Contador", fill_value=0).reset_index()
        # Calcular IS (%) por canal/mês
        df_pivot["IS (%)"] = np.where(
            (df_pivot.get("Sim", 0) + df_pivot.get("Não", 0)) != 0,
            df_pivot.get("Sim", 0) / (df_pivot.get("Sim", 0) + df_pivot.get("Não", 0)) * 100,
            np.nan
        )
        # Calcular linha total (independente do canal)
        df_total = df_sum.groupby(["MesAno", "NPS_Resolvido"], as_index=False)["Contador"].sum()
        df_total_pivot = df_total.pivot_table(index="MesAno", columns="NPS_Resolvido", values="Contador", fill_value=0).reset_index()
        df_total_pivot["IS (%)"] = np.where(
            (df_total_pivot.get("Sim", 0) + df_total_pivot.get("Não", 0)) != 0,
            df_total_pivot.get("Sim", 0) / (df_total_pivot.get("Sim", 0) + df_total_pivot.get("Não", 0)) * 100,
            np.nan
        )
        # Gráfico de barras por canal
        fig = px.bar(
            df_pivot,
            x="MesAno",
            y="IS (%)",
            color="Canal",
            barmode="group",
            title="Índice de Solução Mensal (%) por Canal"
        )
        # Linha de referência horizontal 85%
        fig.add_shape(
            type="line",
            x0=min(df_total_pivot["MesAno"]),
            x1=max(df_total_pivot["MesAno"]),
            y0=85,
            y1=85,
            line=dict(color="yellow", width=2, dash="dot"),
            xref="x",
            yref="y"
        )
        fig.update_layout(
            xaxis_title="Mês/Ano",
            yaxis_title="IS (%)",
            yaxis=dict(range=[0, 100], tickformat=".0f%%"),
            template="plotly_white",
            legend=dict(orientation="h", x=0.5, xanchor="center", y=1.1),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True, key="is_chart2")

        ### LINHA 3 ###

        pass

        ### LINHA 4 ###

        df_filtrado = df_is_dia_pessoa.copy()
        st.write(df_filtrado)

    #-#-#-#-#-# ABAS #-#-#-#-#-#
    
    # Criação das abas
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Produtividade", "♻️ Retrabalho",
    "🟢 SLA", "⏱️ TMR", "😊 Índice de Solução"
    ])
    
    # Aba Produtividade
    with tab1:
        tab_produtividade()

    # Aba Retrabalho
    with tab2:
        tab_retrabalho()
        
    # Aba SLA
    with tab3:
        tab_sla()
        
    # Aba TMR
    with tab4:
        tab_tmr()
        
    # Aba Índice de Solução/NPS
    with tab5:
        tab_is()
        
if __name__ == "__main__":
    main()