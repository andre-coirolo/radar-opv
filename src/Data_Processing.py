import pandas as pd
import os
import streamlit as st

# BASES AUXILIARES

def Qi_real(base):
    df = pd.read_excel(os.path.join(base, 'tbl_qi_real.xlsx'),sheet_name="TBL_QI_REAL") # Importar base de dados Qi_Real

    # Filtrar 'Ano' acima de 2024
    df = df[df['Ano'] >= 2024]
    
    # Filtrar 'Funcao' diferente de 'SUPERVISOR'
    df = df[df['Funcao'] != 'SUPERVISOR']

    # Filtrar colunas relevantes
    df = df[['Concatenar','MesRetorno','Ano','Nome','Gr_Vendedor','STATUS_ATUAL','Supervisor','Email']]
    
    # Renomear colunas
    df = df.rename(columns={
        'Concatenar': 'Concatenar',
        'MesRetorno': 'Mes',
        'Ano': 'Ano',
        'Nome': 'Agente',
        'Gr_Vendedor': 'Grupo_Vendedor',
        'STATUS_ATUAL': 'Status_Atual',
        'Supervisor': 'Supervisor',
        'Email': 'Email'
    })
    
    df['Email'] = df['Email'].str.lower() # Colocar email em minúsculo
    
    return df

def Metas(base):
    df = pd.read_excel(os.path.join(base, 'Metas.xlsx')) # Importar base de dados Metas
    # Filtrar apenas as linhas que 'Nome' não é nulo
    df = df[df['Nome'].notna()] 
    
    return df

def Base_Devolutiva(base):
    # Importar base de Devolutiva para mapear os analistas
    df_Devolutiva = pd.read_excel(os.path.join(base, 'Base_Devolutiva.xlsx'))
    # Ver qual foi o último analista que atendeu o CAP (levando em consideração o maior 'Num. Etapa' de cada CAP)
    df_Devolutiva = df_Devolutiva[['Num. Solicitação','Tratado Por (Etapa)','Num. Etapa', 'Serviço','Etapa','Causa Raiz']]
    df_Devolutiva = df_Devolutiva.sort_values(by=['Num. Solicitação', 'Num. Etapa'], ascending=[True, False])
    df_Devolutiva = df_Devolutiva.drop_duplicates(subset=['Num. Solicitação'], keep='first')
    df_Devolutiva = df_Devolutiva.rename(columns={
        'Num. Solicitação': 'CAP',
        'Tratado Por (Etapa)': 'Analista'
    })
    
    return df_Devolutiva

# BASES DE DADOS

def Base_ProdRetr(base, qi_real):
    df = pd.read_excel(os.path.join(base, 'Base_AvancaVC_OPV.xlsx')) # Importar base de dados Retrabalho 
    df = df[df['Serviço_Morto?'] == 'Não_Morto'] # Filtrar apenas os Não Mortos
    df = df[['Data Conclusão Etapa','Serviço','Etapa','Num. Solicitação','Responsável Etapa','tbl_CAP_WorkflowProgress.ModifiedByName','Etapas concluídas','Retrabalho']] # Filtrar apenas os dados relevantes
    df = df.rename(columns={
        'Data Conclusão Etapa': 'Data',
        'Serviço': 'Servico',
        'Etapa': 'Etapa',
        'Num. Solicitação': 'Num_Solicitacao',
        'Responsável Etapa': 'Responsavel_Etapa',
        'tbl_CAP_WorkflowProgress.ModifiedByName': 'Tratado_Por',
        'Etapas concluídas': 'Produtividade',
        'Retrabalho': 'Retrabalho'
    })
    
    df2 = pd.read_excel(os.path.join(base, 'Base_AvancaVC_OPV_Morto.xlsx')) # Importar base de dados Retrabalho Morto
    df2['Value'] = pd.to_numeric(df2['Value'], errors = 'coerce') # Converter a coluna 'Value' para float
    df2 = df2[df2['Value'] < 1000] # Filtrar erros de preenchimento (as vezes colocam número de chamado)
    df2 = df2[['Data Conclusão Etapa','Serviço','Etapa','Num. Solicitação','Responsável Etapa','tbl_CAP_WorkflowProgress.ModifiedByName','Value','Retrabalho']] # Filtrar apenas os Não Mortos
    df2 = df2.rename(columns={
        'Data Conclusão Etapa': 'Data',
        'Serviço': 'Servico',
        'Etapa': 'Etapa',
        'Num. Solicitação': 'Num_Solicitacao',
        'Responsável Etapa': 'Responsavel_Etapa',
        'tbl_CAP_WorkflowProgress.ModifiedByName': 'Tratado_Por',
        'Value': 'Produtividade',
        'Retrabalho': 'Retrabalho'
    })
    
    df_total = pd.concat([df, df2], ignore_index=True) # Concatenar as duas bases
    
    ############################################################################
    # Arrumar o 'Tratado_por' caso o nome esteja diferente da QI
    df_total['Tratado_Por'] = df_total['Tratado_Por'].replace('XXXXXX', 'YYYYYY')
    # Ajustar os nomes da coluna 'Tratado_por' (title)
    df_total['Tratado_Por'] = df_total['Tratado_Por'].str.title()
    # Fazer o concatenado para fazer o merge com a base Qi_Real (Tratado_Por + Mes + Ano)
    df_total['Mes'] = df_total['Data'].dt.month
    df_total['Ano'] = df_total['Data'].dt.year
    df_total['Concatenar'] = df_total['Tratado_Por'] + df_total['Mes'].astype(str) + df_total['Ano'].astype(str)
    # Transformar o 'Concatenar' em uppercase
    df_total['Concatenar'] = df_total['Concatenar'].str.upper()
    
    # Cruzar com a Qi_Real para trazer o Grupo do Vendedor
    df_Qi_Real_0 = Qi_real(qi_real) # Importar base Qi_Real
    df_Qi_Real = df_Qi_Real_0[['Concatenar','Grupo_Vendedor']] # Selecionar apenas as colunas relevantes
    
    # Fazer o merge
    df_total = pd.merge(df_total, df_Qi_Real, left_on='Concatenar', right_on='Concatenar', how='left')
    
    # Drop na coluna 'Concatenar'
    df_total = df_total.drop(columns=['Concatenar'])
    ############################################################################
    
    return df_total

def Base_SLA(base, qi_real):
    df = pd.read_excel(os.path.join(base, 'Base_Avanca_SLA.xlsx'))
    df = df[['Data Conclusão Etapa','Responsável Etapa','Etapas no prazo','Etapas concluídas','Tratado Por (Etapa)']]
    df = df.rename(columns={
        'Data Conclusão Etapa': 'Data',
        'Responsável Etapa': 'Responsavel_Etapa',
        'Etapas no prazo': 'Etapas_Prazo',
        'Etapas concluídas': 'Etapas_Concluidas',
        'Tratado Por (Etapa)': 'Tratado_Por'
    })
    
    ############################################################################
    # Ajustar os nomes da coluna 'Tratado_por' (title)
    df['Tratado_Por'] = df['Tratado_Por'].str.title()
    # Fazer o concatenado para fazer o merge com a base Qi_Real (Tratado_Por + Mes + Ano)
    df['Mes'] = df['Data'].dt.month
    df['Ano'] = df['Data'].dt.year
    df['Concatenar'] = df['Tratado_Por'] + df['Mes'].astype(str) + df['Ano'].astype(str)
    # Transformar o 'Concatenar' em uppercase
    df['Concatenar'] = df['Concatenar'].str.upper()
    
    # Cruzar com a Qi_Real para trazer o Grupo do Vendedor
    df_Qi_Real_0 = Qi_real(qi_real) # Importar base Qi_Real
    df_Qi_Real = df_Qi_Real_0[['Concatenar','Grupo_Vendedor']] # Selecionar apenas as colunas relevantes
    
    # Fazer o merge
    df = pd.merge(df, df_Qi_Real, left_on='Concatenar', right_on='Concatenar', how='left')
    
    # Drop na coluna 'Concatenar'
    df = df.drop(columns=['Concatenar'])
    ############################################################################
    
    return df

def Base_TMR(base, qi_real):
    df = pd.read_excel(os.path.join(base, 'Base_Avanca_TMR.xlsx'))
    df = df[['Data Conclusão Etapa','Responsável Etapa','TMR Etapa Bloqueio','Tratado Por (Etapa)']]
    df = df.rename(columns={
        'Data Conclusão Etapa': 'Data',
        'Responsável Etapa': 'Responsavel_Etapa',
        'TMR Etapa Bloqueio': 'TMR_Horas',
        'Tratado Por (Etapa)': 'Tratado_Por'
    })
    
    ############################################################################
    # Ajustar os nomes da coluna 'Tratado_por' (title)
    df['Tratado_Por'] = df['Tratado_Por'].str.title()
    # Fazer o concatenado para fazer o merge com a base Qi_Real (Tratado_Por + Mes + Ano)
    df['Mes'] = df['Data'].dt.month
    df['Ano'] = df['Data'].dt.year
    df['Concatenar'] = df['Tratado_Por'] + df['Mes'].astype(str) + df['Ano'].astype(str)
    # Transformar o 'Concatenar' em uppercase
    df['Concatenar'] = df['Concatenar'].str.upper()
    
    # Cruzar com a Qi_Real para trazer o Grupo do Vendedor
    df_Qi_Real_0 = Qi_real(qi_real) # Importar base Qi_Real
    df_Qi_Real = df_Qi_Real_0[['Concatenar','Grupo_Vendedor']] # Selecionar apenas as colunas relevantes
    
    # Fazer o merge
    df = pd.merge(df, df_Qi_Real, left_on='Concatenar', right_on='Concatenar', how='left')
    
    # Drop na coluna 'Concatenar'
    df = df.drop(columns=['Concatenar'])
    ############################################################################
    
    # # forçar 'TMR_Horas' para número
    # df['TMR_Horas'] = pd.to_numeric(df['TMR_Horas'], errors='coerce')
    
    # criar uma coluna 'Contador' que é igual a 1
    df['Qtd_Etapas'] = 1
    
    return df

# BASES DE IS

def IS_URA(base):
    # Importar todas as bases da pasta de URA
    lista_arquivos = os.listdir(base)
    df_list = []
    for arquivo in lista_arquivos:
        caminho = os.path.join(base, arquivo)
        df = pd.read_csv(caminho, encoding='utf-8', sep=',')  # ajuste o encoding/separador
        df_list.append(df)
    df_final = pd.concat(df_list, ignore_index=True)

    # Selecionar apenas as colunas relevantes
    df = df_final[['CALL ID','CALLS','DISPOSITION','TALK TIME','Devolutiva','Custom.Numero_CAP','Custom.Transfer_NPS','Custom.NPS_Solicitacao','Custom.NPS_Nota','DATE','Custom.Analista']]
    
    # Formatar data para DD/MM/AAAA
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y/%m/%d', errors='coerce')
    df['DATE'] = df['DATE'].dt.strftime('%d/%m/%Y')
    df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%Y', errors='coerce')
    
    # Pegar tudo que contenha 'Cli' na coluna 'Devolutiva' e substituir por 'Cliente', pegar tudo que contenha 'Ve' e substituir por 'Vendedor' e o resto deixar em branco
    df['Devolutiva'] = df['Devolutiva'].apply(
    lambda x: 'Cliente' if 'cli' in str(x).lower() else ('Vendedor' if 've' in str(x).lower() else '')
    )
    
    # Tratar a coluna 'Custom.Numero_CAP' como numérica, forçando erros para NaN
    df['Custom.Numero_CAP'] = pd.to_numeric(df['Custom.Numero_CAP'], errors='coerce')
    # df = df[df['Custom.Numero_CAP'].notna()]  # Remover linhas  (deixei comentado porque acho que vai filtrar todas as linhas que não tiverem CAP, e talvez queira analisar essas linhas depois)
    
    # Criar uma coluna adicional 'CONTACTED' que se na 'DISPOSITION' tiver os resultados 'Atendido', 'Atendida' ou 'Atendido - NPS', então retorna 1, senão 0
    df['CONTACTED'] = df['DISPOSITION'].apply(
        lambda x: 1 if x in ['URA Pesquisa NPS', 'Protocolo Permanecera em Andamento', 'Cliente solicita novo contato', 'Contato de Finalizacao do Protocolo', ''] else 0
    )
    
    return df

def IS_Email(base):
    # Importar todas as bases da pasta de URA
    lista_arquivos = os.listdir(base)
    df_list = []
    # Abrir todos os arquivo .xlsx da pasta
    for arquivo in lista_arquivos:
        if arquivo.endswith('.xlsx'):
            caminho = os.path.join(base, arquivo)
            df = pd.read_excel(caminho)
            df_list.append(df)
        
    df_final = pd.concat(df_list, ignore_index=True)
    
    # Filtrar colunas relevantes
    df = df_final[['CAP','status','data envio','Nota','recomendacao','solicitacao','sugestao']]
    
    # Formatar data para DD/MM/AAAA
    df['data envio'] = pd.to_datetime(df['data envio'], format='%d/%m/%Y', errors='coerce')
    df['data envio'] = df['data envio'].dt.strftime('%d/%m/%Y')
    df['data envio'] = pd.to_datetime(df['data envio'], format='%d/%m/%Y', errors='coerce')
    
    return df

def IS_Final(base_URA, base_Email, base_Devolutiva, Base_Qi_real):
    df_URA = IS_URA(base_URA)
    df_Email = IS_Email(base_Email)
    
    ### Tratamento df_URA ###
    # Criação da coluna 'Canal' com valor fixo 'URA'
    df_URA['Canal'] = 'URA'
    
    # Selecionar apenas as colunas relevantes
    df_URA = df_URA[['CALLS','Custom.Numero_CAP','Canal','DATE','Custom.Analista','Custom.NPS_Solicitacao','Custom.NPS_Nota','Devolutiva']]
    
    # Renomear colunas
    df_URA = df_URA.rename(columns={
        'CALLS': 'Contador',
        'Custom.Numero_CAP': 'CAP',
        'Canal': 'Canal',
        'DATE': 'Data',
        'Custom.Analista': 'Analista',
        'Custom.NPS_Solicitacao': 'NPS_Resolvido',
        'Custom.NPS_Nota': 'NPS_Nota',
        'Devolutiva': 'Devolutiva'
    })
    
    # Ajustar nome do analista que está como email para o nome completo. Para fazer isso, preciso importar a Qi_Real e fazer um merge
    df_Qi_Real_0 = Qi_real(Base_Qi_real) # Importar base Qi_Real
    df_Qi_Real = df_Qi_Real_0[['Agente','Email']] # Selecionar apenas as colunas relevantes
    df_Qi_Real['Email'] = df_Qi_Real['Email'].str.title() # Ajustar o nome do email para bater os valores
    df_Qi_Real = df_Qi_Real.drop_duplicates(subset=['Email'], keep='first') # Remover duplicatas
    df_Qi_Real = df_Qi_Real[df_Qi_Real['Email'].notna()] # Filtrar apenas os analistas que tem email cadastrado
    # Merge com a base de URA para trazer o nome do analista (A chave considerada é o email)
    df_URA = pd.merge(df_URA, df_Qi_Real, left_on='Analista', right_on='Email', how='left')
    # Se o nome do analista estiver vazio, manter o valor original da coluna 'Analista', senão, substituir pelo valor da coluna 'Agente'
    df_URA['Analista'] = df_URA.apply(lambda row: row['Agente'] if pd.notna(row['Agente']) else row['Analista'], axis=1)
    df_URA = df_URA.drop(columns=['Agente','Email']) # Remover colunas desnecessárias
    
    ### Tratamento df_Email ###
    # Criação da coluna 'Canal' com valor fixo 'Email'
    df_Email['Canal'] = 'Email'
    
    # Criação da coluna 'Devolutiva' com valor fixo 'Cliente'
    df_Email['Devolutiva'] = 'Cliente'
    
    # Criar contador fixo 1
    df_Email['Contador'] = 1
    
    ## Criar coluna 'Analista'
    # Importar base de Devolutiva para mapear os analistas
    df_Devolutiva = Base_Devolutiva(base_Devolutiva)
    # Selecionar colunas relevantes
    df_Devolutiva_1 = df_Devolutiva[['CAP','Analista']]
    
    # Merge com a base de Email para trazer o Analista (A chave considerada é o CAP)
    df_Email = pd.merge(df_Email, df_Devolutiva_1, on='CAP', how='left')
    
    # Selecionar apenas as colunas relevantes
    df_Email = df_Email[['Contador','CAP','Canal','data envio','Analista','solicitacao','recomendacao','Devolutiva']]
    
    # Renomear colunas
    df_Email = df_Email.rename(columns={
        'Contador': 'Contador',
        'CAP': 'CAP',
        'Canal': 'Canal',
        'data envio': 'Data',
        'Analista': 'Analista',
        'solicitacao': 'NPS_Resolvido',
        'recomendacao': 'NPS_Nota',
        'Devolutiva': 'Devolutiva'
    })
    
    # Concatenar a df_URA com a df_Email na df_IS_Final
    df_IS_Final = pd.concat([df_URA, df_Email], ignore_index=True)
    
    # Selecionar as colunas relevantes para o merge
    df_Devolutiva_2 = df_Devolutiva[['CAP','Serviço','Causa Raiz']]
    
    # Dar merge com a base de Devolutiva para trazer Serviço e Causa Raiz (A chave considerada é o CAP)
    df_IS_Final = pd.merge(df_IS_Final, df_Devolutiva_2, on='CAP', how='left')
    
    # Antes do merge preciso ajustar o nome de alguns analistas que estão com nomes diferentes na base IS e na base de Qi_Real
    df_IS_Final['Analista'] = df_IS_Final['Analista'].replace({
        'XXXXXXXXXX': 'YYYYYYYYYYY'
    })
    
    # Criar coluna de concatenado AgenteMesAno para fazer o merge com a base Qi_Real
    df_IS_Final['Mes'] = df_IS_Final['Data'].dt.month
    df_IS_Final['Ano'] = df_IS_Final['Data'].dt.year
    df_IS_Final['Concatenar'] = df_IS_Final['Analista'] + df_IS_Final['Mes'].astype(str) + df_IS_Final['Ano'].astype(str)
    # Transformar o 'Concatenar' em uppercase
    df_IS_Final['Concatenar'] = df_IS_Final['Concatenar'].str.upper()
    
    # Trazer a coluna 'Grupo_Vendedor' da base Qi_Real (A chave considerada é o Analista)
    df_Qi_Real_2 = df_Qi_Real_0[['Concatenar','Grupo_Vendedor']] # Selecionar apenas as colunas relevantes
    df_IS_Final = pd.merge(df_IS_Final, df_Qi_Real_2, left_on='Concatenar', right_on='Concatenar', how='left')
    df_IS_Final = df_IS_Final.drop(columns=['Concatenar']) # Remover colunas desnecessárias
        
    # Ajustar os resultados da coluna 'NPS_Resolvido' = "Nao" para "Não"
    df_IS_Final['NPS_Resolvido'] = df_IS_Final['NPS_Resolvido'].str.title()
    df_IS_Final['NPS_Resolvido'] = df_IS_Final['NPS_Resolvido'].replace({'Nao': 'Não'})
    
    # Deixar o nome dos analistas em maiúsculo
    df_IS_Final['Analista'] = df_IS_Final['Analista'].str.title()
    
    # Por último, preciso retirar os CAPs que estão duplicados (mesmo CAP com Data diferente)
    # Para isso, vou considerar o CAP mais recente com algumas ressalvas: priorizar o que não está null no 'NPS_Resolvido' e depois priorizar o canal 'URA' em relação ao 'Email'. Teve resposta -> URA -> Data mais recente
    df_IS_Final['NPS_Resolvido_Preenchido'] = df_IS_Final['NPS_Resolvido'].apply(lambda x: 1 if pd.notna(x) and x != '' else 0) # Criar uma coluna auxiliar que indique se o 'NPS_Resolvido' está preenchido ou não (1 para preenchido, 0 para vazio)
    df_IS_Final = df_IS_Final.sort_values(by=['CAP', 'NPS_Resolvido_Preenchido', 'Canal', 'Data'], ascending=[True, False, False, True])
    # Dropar CAPs duplicados, mantendo o primeiro (que é o mais recente e com resposta)
    df_IS_Final = df_IS_Final.drop_duplicates(subset=['CAP'], keep='first')
    # Dropar a coluna auxiliar
    df_IS_Final = df_IS_Final.drop(columns=['NPS_Resolvido_Preenchido'])
    
    return df_IS_Final

# LOAD DE TODAS AS BASES (com cache no streamlit)

@st.cache_data # Habilitar cache para melhorar a UX
def Load_Bases(b_QI,b_Metas,b_ProdRet,b_SLA,b_TMR,b_ISURA,b_ISEmail,b_Devolutiva):
        
    # df_DU_Brasil = Dia_Referencia(b_DU)
    df_Qireal = Qi_real(b_QI)
    df_Metas = Metas(b_Metas)
    df_ProdRet = Base_ProdRetr(b_ProdRet, b_QI)
    df_SLA = Base_SLA(b_SLA, b_QI)
    df_TMR = Base_TMR(b_TMR, b_QI)
    df_IS_Final = IS_Final(b_ISURA, b_ISEmail, b_Devolutiva, b_QI)
    
    # Printar se todas as bases foram carregadas corretamente
    print("Bases carregadas com sucesso!")
    
    return df_Qireal, df_Metas, df_ProdRet, df_SLA, df_TMR, df_IS_Final
