import pandas as pd

# PRODUTIVIDADE

def Prod_Pessoa(dfProdRetr):
    # Copiar dataframes para evitar alterações nos originais
    df_prod_dia_pessoa = dfProdRetr.copy()
    
    # Filtrar apenas os 'Grupo_Vendedor' iguais a 'SUBGRUPO48', 'SUBGRUPO45' e 'SUBGRUPO50'
    grupos_opv = ['SUBGRUPO48', 'SUBGRUPO45', 'SUBGRUPO50']
    df_prod_dia_pessoa = df_prod_dia_pessoa[df_prod_dia_pessoa['Grupo_Vendedor'].isin(grupos_opv)]
    
        
    # Agrupar por 'Tratado_Por' e por 'Data' somando 'Produtividade'
    df_prod_dia_pessoa = df_prod_dia_pessoa.groupby(['Tratado_Por', 'Data', 'Grupo_Vendedor']).agg({
        'Produtividade': 'sum'
    }).reset_index()
    
    # Considerar apenas os dias das pessoas se elas fecharam mais de 5 chamados (filtrar)
    df_prod_dia_pessoa = df_prod_dia_pessoa[df_prod_dia_pessoa['Produtividade'] > 5]
    
    # Vou abrir a data por mês e ano
    df_prod_dia_pessoa['Ano'] = df_prod_dia_pessoa['Data'].dt.year
    df_prod_dia_pessoa['Mes'] = df_prod_dia_pessoa['Data'].dt.month

    # Mês
    df_prod_mes_pessoa = df_prod_dia_pessoa.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Ano', 'Mes']).agg({
        'Produtividade': 'mean'
    }).reset_index()
    
    # Ano
    df_prod_ano_pessoa = df_prod_dia_pessoa.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Ano']).agg({
        'Produtividade': 'mean'
    }).reset_index()
    
    return df_prod_dia_pessoa, df_prod_mes_pessoa, df_prod_ano_pessoa

def Prod_Grupo(dfProdRetr):
    # Copiar dataframes para evitar alterações nos originais
    df_prod_dia_grupo = dfProdRetr.copy()
    
    # Filtrar apenas os 'Grupo_Vendedor' iguais a 'SUBGRUPO48', 'SUBGRUPO45' e 'SUBGRUPO50'
    grupos_opv = ['SUBGRUPO48', 'SUBGRUPO45', 'SUBGRUPO50']
    df_prod_dia_grupo = df_prod_dia_grupo[df_prod_dia_grupo['Grupo_Vendedor'].isin(grupos_opv)]
        
    # Agrupar por 'Tratado_Por' e por 'Data' somando 'Produtividade'
    df_prod_dia_grupo = df_prod_dia_grupo.groupby(['Tratado_Por','Data','Grupo_Vendedor']).agg({
        'Produtividade': 'sum'
    }).reset_index()
    
    # Considerar apenas os dias das pessoas se elas fecharam mais de 5 chamados (filtrar)
    df_prod_dia_grupo = df_prod_dia_grupo[df_prod_dia_grupo['Produtividade'] > 5]
    
    # Até aqui eu tenho a produtividade da 'df_prod_dia_pessoa'. A partir daqui eu vou agrupar por Grupo_vendedor
    
    # Produtividade por grupo
    df_prod_dia_grupo = df_prod_dia_grupo.groupby(['Data','Grupo_Vendedor']).agg({
        'Produtividade': 'mean'
    }).reset_index()
    
    # agora vou separar a data em mês e ano e agrupar por mes e agrupar por ano
    df_prod_dia_grupo['Ano'] = df_prod_dia_grupo['Data'].dt.year
    df_prod_dia_grupo['Mes'] = df_prod_dia_grupo['Data'].dt.month

    df_prod_mes_grupo = df_prod_dia_grupo.groupby(['Grupo_Vendedor', 'Ano', 'Mes']).agg({
        'Produtividade': 'mean'
    }).reset_index()
    
    df_prod_ano_grupo = df_prod_dia_grupo.groupby(['Grupo_Vendedor', 'Ano']).agg({
        'Produtividade': 'mean'
    }).reset_index()

    return df_prod_dia_grupo, df_prod_mes_grupo, df_prod_ano_grupo

def Prod_OPV(dfProdRetr):
    # Copiar dataframes para evitar alterações nos originais
    df_prod_dia_OPV = dfProdRetr.copy()
    
    # Filtrar apenas os 'Grupo_Vendedor' iguais a 'SUBGRUPO48', 'SUBGRUPO45' e 'SUBGRUPO50'
    grupos_opv = ['SUBGRUPO48', 'SUBGRUPO45', 'SUBGRUPO50']
    df_prod_dia_OPV = df_prod_dia_OPV[df_prod_dia_OPV['Grupo_Vendedor'].isin(grupos_opv)]
        
    # Agrupar por 'Tratado_Por' e por 'Data' somando 'Produtividade'
    df_prod_dia_OPV = df_prod_dia_OPV.groupby(['Tratado_Por','Data','Grupo_Vendedor']).agg({
        'Produtividade': 'sum'
    }).reset_index()
    
    # Considerar apenas os dias das pessoas se elas fecharam mais de 5 chamados (filtrar)
    df_prod_dia_OPV = df_prod_dia_OPV[df_prod_dia_OPV['Produtividade'] > 5]
    
    # Até aqui eu tenho a produtividade da 'df_prod_dia_pessoa'. A partir daqui eu vou agrupar por data para ter o total do opv
    
    # Produtividade por OPV
    df_prod_dia_OPV = df_prod_dia_OPV.groupby(['Data']).agg({
        'Produtividade': 'mean'
    }).reset_index()
    
    # agora vou separar a data em mês e ano e agrupar por mes e agrupar por ano
    df_prod_dia_OPV['Ano'] = df_prod_dia_OPV['Data'].dt.year
    df_prod_dia_OPV['Mes'] = df_prod_dia_OPV['Data'].dt.month

    df_prod_mes_OPV = df_prod_dia_OPV.groupby(['Ano', 'Mes']).agg({
        'Produtividade': 'mean'
    }).reset_index()
    
    df_prod_ano_OPV = df_prod_dia_OPV.groupby(['Ano']).agg({
        'Produtividade': 'mean'
    }).reset_index()
    
    return df_prod_dia_OPV, df_prod_mes_OPV, df_prod_ano_OPV

# RETRABALHO

def Ret_Pessoa(dfProdRetr):
    # Copiar dataframes para evitar alterações nos originais
    df_ret_dia_pessoa = dfProdRetr.copy()
    
    # Filtrar apenas os 'Grupo_Vendedor' iguais a 'SUBGRUPO48', 'SUBGRUPO45' e 'SUBGRUPO50'
    grupos_opv = ['SUBGRUPO48', 'SUBGRUPO45', 'SUBGRUPO50']
    df_ret_dia_pessoa = df_ret_dia_pessoa[df_ret_dia_pessoa['Grupo_Vendedor'].isin(grupos_opv)]
    
        
    # Agrupar por 'Tratado_Por' e por 'Data' somando 'Produtividade' e 'Retrabalho'
    df_ret_dia_pessoa = df_ret_dia_pessoa.groupby(['Tratado_Por', 'Data', 'Grupo_Vendedor']).agg({
        'Produtividade': 'sum',
        'Retrabalho': 'sum'
    }).reset_index()
    
    # # Considerar apenas os dias das pessoas se elas fecharam mais de 5 chamados (filtrar) # Comentado porque no retrabalho não tem essa regra
    # df_prod_dia_pessoa = df_prod_dia_pessoa[df_prod_dia_pessoa['Produtividade'] > 5]
    
    # Vou abrir a data por mês e ano
    df_ret_dia_pessoa['Ano'] = df_ret_dia_pessoa['Data'].dt.year
    df_ret_dia_pessoa['Mes'] = df_ret_dia_pessoa['Data'].dt.month

    # Mês
    df_ret_mes_pessoa = df_ret_dia_pessoa.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Ano', 'Mes']).agg({
        'Produtividade': 'sum',
        'Retrabalho': 'sum'
    }).reset_index()
    
    # Ano
    df_ret_ano_pessoa = df_ret_dia_pessoa.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Ano']).agg({
        'Produtividade': 'sum',
        'Retrabalho': 'sum'
    }).reset_index()
    
    return df_ret_dia_pessoa, df_ret_mes_pessoa, df_ret_ano_pessoa

def Ret_Grupo(dfProdRetr):
    # Copiar dataframes para evitar alterações nos originais
    df_ret_dia_grupo = dfProdRetr.copy()
    
    # Filtrar apenas os 'Grupo_Vendedor' iguais a 'SUBGRUPO48', 'SUBGRUPO45' e 'SUBGRUPO50'
    grupos_opv = ['SUBGRUPO48', 'SUBGRUPO45', 'SUBGRUPO50']
    df_ret_dia_grupo = df_ret_dia_grupo[df_ret_dia_grupo['Grupo_Vendedor'].isin(grupos_opv)]
        
    # Agrupar por 'Tratado_Por' e por 'Data' somando 'Produtividade'
    df_ret_dia_grupo = df_ret_dia_grupo.groupby(['Tratado_Por','Data','Grupo_Vendedor']).agg({
        'Produtividade': 'sum',
        'Retrabalho': 'sum'
    }).reset_index()
    
    # # Considerar apenas os dias das pessoas se elas fecharam mais de 5 chamados (filtrar) # Comentado porque no retrabalho não tem essa regra
    # df_ret_dia_grupo = df_ret_dia_grupo[df_ret_dia_grupo['Produtividade'] > 5]
    
    # Até aqui eu tenho o retrabalho da 'df_ret_dia_pessoa'. A partir daqui eu vou agrupar por Grupo_vendedor
    
    # Retrabalho por grupo
    df_ret_dia_grupo = df_ret_dia_grupo.groupby(['Data','Grupo_Vendedor']).agg({
        'Produtividade': 'sum',
        'Retrabalho': 'sum'
    }).reset_index()
    
    # agora vou separar a data em mês e ano e agrupar por mes e agrupar por ano
    df_ret_dia_grupo['Ano'] = df_ret_dia_grupo['Data'].dt.year
    df_ret_dia_grupo['Mes'] = df_ret_dia_grupo['Data'].dt.month

    df_ret_mes_grupo = df_ret_dia_grupo.groupby(['Grupo_Vendedor', 'Ano', 'Mes']).agg({
        'Produtividade': 'sum',
        'Retrabalho': 'sum'
    }).reset_index()
    
    df_ret_ano_grupo = df_ret_dia_grupo.groupby(['Grupo_Vendedor', 'Ano']).agg({
        'Produtividade': 'sum',
        'Retrabalho': 'sum'
    }).reset_index()

    return df_ret_dia_grupo, df_ret_mes_grupo, df_ret_ano_grupo

def Ret_OPV(dfProdRetr):
    # Copiar dataframes para evitar alterações nos originais
    df_ret_dia_OPV = dfProdRetr.copy()
    
    # Filtrar apenas os 'Grupo_Vendedor' iguais a 'SUBGRUPO48', 'SUBGRUPO45' e 'SUBGRUPO50'
    grupos_opv = ['SUBGRUPO48', 'SUBGRUPO45', 'SUBGRUPO50']
    df_ret_dia_OPV = df_ret_dia_OPV[df_ret_dia_OPV['Grupo_Vendedor'].isin(grupos_opv)]
        
    # Agrupar por 'Tratado_Por' e por 'Data' somando 'Produtividade' e 'Retrabalho'
    df_ret_dia_OPV = df_ret_dia_OPV.groupby(['Tratado_Por','Data','Grupo_Vendedor']).agg({
        'Produtividade': 'sum',
        'Retrabalho': 'sum'
    }).reset_index()
    
    # # Considerar apenas os dias das pessoas se elas fecharam mais de 5 chamados (filtrar) # Comentado porque no retrabalho não tem essa regra
    # df_ret_dia_OPV = df_ret_dia_OPV[df_ret_dia_OPV['Produtividade'] > 5]

    # Até aqui eu tenho o retrabalho da 'df_ret_dia_OPV'. A partir daqui eu vou agrupar por data para ter o total do opv

    # Produtividade por OPV
    df_ret_dia_OPV = df_ret_dia_OPV.groupby(['Data']).agg({
        'Produtividade': 'sum',
        'Retrabalho': 'sum'
    }).reset_index()
    
    # agora vou separar a data em mês e ano e agrupar por mes e agrupar por ano
    df_ret_dia_OPV['Ano'] = df_ret_dia_OPV['Data'].dt.year
    df_ret_dia_OPV['Mes'] = df_ret_dia_OPV['Data'].dt.month

    df_ret_mes_OPV = df_ret_dia_OPV.groupby(['Ano', 'Mes']).agg({
        'Produtividade': 'sum',
        'Retrabalho': 'sum'
    }).reset_index()

    df_ret_ano_OPV = df_ret_dia_OPV.groupby(['Ano']).agg({
        'Produtividade': 'sum',
        'Retrabalho': 'sum'
    }).reset_index()

    return df_ret_dia_OPV, df_ret_mes_OPV, df_ret_ano_OPV

# SLA

def SLA_Pessoa(dfSLA):
    # Copiar dataframes para evitar alterações nos originais
    df_sla_dia_pessoa = dfSLA.copy()
    
    # Agrupar por 'Tratado_Por', 'Grupo_vendedor" e 'Data' somando 'Etapas_Prazo' e 'Etapas_Concluidas'
    df_sla_dia_pessoa = df_sla_dia_pessoa.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Data']).agg({
        'Etapas_Prazo': 'sum',
        'Etapas_Concluidas': 'sum'
    }).reset_index()

    # Vou abrir a data por mês e ano
    df_sla_dia_pessoa['Ano'] = df_sla_dia_pessoa['Data'].dt.year
    df_sla_dia_pessoa['Mes'] = df_sla_dia_pessoa['Data'].dt.month

    # Mês
    df_sla_mes_pessoa = df_sla_dia_pessoa.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Ano', 'Mes']).agg({
        'Etapas_Prazo': 'sum',
        'Etapas_Concluidas': 'sum'
    }).reset_index()

    # Ano
    df_sla_ano_pessoa = df_sla_dia_pessoa.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Ano']).agg({
        'Etapas_Prazo': 'sum',
        'Etapas_Concluidas': 'sum'
    }).reset_index()

    return df_sla_dia_pessoa, df_sla_mes_pessoa, df_sla_ano_pessoa

def SLA_Grupo(dfSLA):
    # Copiar dataframes para evitar alterações nos originais
    df_sla_dia_grupo = dfSLA.copy()
    
    # Agrupar por 'Tratado_Por', 'Grupo_vendedor" e 'Data' somando 'Etapas_Prazo' e 'Etapas_Concluidas'
    df_sla_dia_grupo = df_sla_dia_grupo.groupby(['Grupo_Vendedor', 'Data']).agg({
        'Etapas_Prazo': 'sum',
        'Etapas_Concluidas': 'sum'
    }).reset_index()

    # Vou abrir a data por mês e ano
    df_sla_dia_grupo['Ano'] = df_sla_dia_grupo['Data'].dt.year
    df_sla_dia_grupo['Mes'] = df_sla_dia_grupo['Data'].dt.month

    # Mês
    df_sla_mes_grupo = df_sla_dia_grupo.groupby(['Grupo_Vendedor', 'Ano', 'Mes']).agg({
        'Etapas_Prazo': 'sum',
        'Etapas_Concluidas': 'sum'
    }).reset_index()

    # Ano
    df_sla_ano_grupo = df_sla_dia_grupo.groupby(['Grupo_Vendedor', 'Ano']).agg({
        'Etapas_Prazo': 'sum',
        'Etapas_Concluidas': 'sum'
    }).reset_index()

    return df_sla_dia_grupo, df_sla_mes_grupo, df_sla_ano_grupo

def SLA_OPV(dfSLA):
    # Copiar dataframes para evitar alterações nos originais
    df_sla_dia_OPV = dfSLA.copy()

    # Agrupar por 'Tratado_Por', 'Grupo_vendedor" e 'Data' somando 'Etapas_Prazo' e 'Etapas_Concluidas'
    df_sla_dia_OPV = df_sla_dia_OPV.groupby(['Responsavel_Etapa', 'Data']).agg({
        'Etapas_Prazo': 'sum',
        'Etapas_Concluidas': 'sum'
    }).reset_index()

    # Vou abrir a data por mês e ano
    df_sla_dia_OPV['Ano'] = df_sla_dia_OPV['Data'].dt.year
    df_sla_dia_OPV['Mes'] = df_sla_dia_OPV['Data'].dt.month

    # Mês
    df_sla_mes_OPV = df_sla_dia_OPV.groupby(['Responsavel_Etapa', 'Ano', 'Mes']).agg({
        'Etapas_Prazo': 'sum',
        'Etapas_Concluidas': 'sum'
    }).reset_index()

    # Ano
    df_sla_ano_OPV = df_sla_dia_OPV.groupby(['Responsavel_Etapa', 'Ano']).agg({
        'Etapas_Prazo': 'sum',
        'Etapas_Concluidas': 'sum'
    }).reset_index()

    return df_sla_dia_OPV, df_sla_mes_OPV, df_sla_ano_OPV

# TMR

def TMR_Pessoa(dfTMR, remover_outlier_tmr):
    # Copiar dataframes para evitar alterações nos originais
    df_tmr_dia_pessoa = dfTMR.copy()
    
    # No avança de 2025 estamos considerando apenas as etapas de TMR < 01:00:00
    if remover_outlier_tmr == True:
        tmr_maximo_considerado = pd.Timedelta(hours=1)
        df_tmr_dia_pessoa = df_tmr_dia_pessoa[df_tmr_dia_pessoa['TMR_Horas'] < tmr_maximo_considerado]

    # Agrupar por 'Tratado_Por', 'Grupo_vendedor" e 'Data' somando 'Qtd_Etapas' e 'TMR_Horas'
    df_tmr_dia_pessoa = df_tmr_dia_pessoa.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Data']).agg({
        'Qtd_Etapas': 'sum',
        'TMR_Horas': 'sum'
    }).reset_index()

    # Vou abrir a data por mês e ano
    df_tmr_dia_pessoa['Ano'] = df_tmr_dia_pessoa['Data'].dt.year
    df_tmr_dia_pessoa['Mes'] = df_tmr_dia_pessoa['Data'].dt.month

    # Mês
    df_tmr_mes_pessoa = df_tmr_dia_pessoa.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Ano', 'Mes']).agg({
        'Qtd_Etapas': 'sum',
        'TMR_Horas': 'sum'
    }).reset_index()

    # Ano
    df_tmr_ano_pessoa = df_tmr_dia_pessoa.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Ano']).agg({
        'Qtd_Etapas': 'sum',
        'TMR_Horas': 'sum'
    }).reset_index()

    return df_tmr_dia_pessoa, df_tmr_mes_pessoa, df_tmr_ano_pessoa

def TMR_Grupo(dfTMR, remover_outlier_tmr):
    # Copiar dataframes para evitar alterações nos originais
    df_tmr_dia_grupo = dfTMR.copy()

    # No avança de 2025 estamos considerando apenas as etapas de TMR < 01:00:00
    if remover_outlier_tmr == True:
        tmr_maximo_considerado = pd.Timedelta(hours=1)
        df_tmr_dia_grupo = df_tmr_dia_grupo[df_tmr_dia_grupo['TMR_Horas'] < tmr_maximo_considerado]

    # Agrupar por 'Grupo_Vendedor' e 'Data' somando 'Qtd_Etapas' e 'TMR_Horas'
    df_tmr_dia_grupo = df_tmr_dia_grupo.groupby(['Grupo_Vendedor', 'Data']).agg({
        'Qtd_Etapas': 'sum',
        'TMR_Horas': 'sum'
    }).reset_index()

    # Vou abrir a data por mês e ano
    df_tmr_dia_grupo['Ano'] = df_tmr_dia_grupo['Data'].dt.year
    df_tmr_dia_grupo['Mes'] = df_tmr_dia_grupo['Data'].dt.month

    # Mês
    df_tmr_mes_grupo = df_tmr_dia_grupo.groupby(['Grupo_Vendedor', 'Ano', 'Mes']).agg({
        'Qtd_Etapas': 'sum',
        'TMR_Horas': 'sum'
    }).reset_index()

    # Ano
    df_tmr_ano_grupo = df_tmr_dia_grupo.groupby(['Grupo_Vendedor', 'Ano']).agg({
        'Qtd_Etapas': 'sum',
        'TMR_Horas': 'sum'
    }).reset_index()

    return df_tmr_dia_grupo, df_tmr_mes_grupo, df_tmr_ano_grupo

def TMR_OPV(dfTMR, remover_outlier_tmr):
    # Copiar dataframes para evitar alterações nos originais
    df_tmr_dia_OPV = dfTMR.copy()

    # No avança de 2025 estamos considerando apenas as etapas de TMR < 01:00:00
    if remover_outlier_tmr == True:
        tmr_maximo_considerado = pd.Timedelta(hours=1)
        df_tmr_dia_OPV = df_tmr_dia_OPV[df_tmr_dia_OPV['TMR_Horas'] < tmr_maximo_considerado]

    # Agrupar por 'Tratado_Por', 'Grupo_vendedor" e 'Data' somando 'Qtd_Etapas' e 'TMR_Horas'
    df_tmr_dia_OPV = df_tmr_dia_OPV.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Data']).agg({
        'Qtd_Etapas': 'sum',
        'TMR_Horas': 'sum'
    }).reset_index()

    # Vou abrir a data por mês e ano
    df_tmr_dia_OPV['Ano'] = df_tmr_dia_OPV['Data'].dt.year
    df_tmr_dia_OPV['Mes'] = df_tmr_dia_OPV['Data'].dt.month

    # Mês
    df_tmr_mes_OPV = df_tmr_dia_OPV.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Ano', 'Mes']).agg({
        'Qtd_Etapas': 'sum',
        'TMR_Horas': 'sum'
    }).reset_index()

    # Ano
    df_tmr_ano_OPV = df_tmr_dia_OPV.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Ano']).agg({
        'Qtd_Etapas': 'sum',
        'TMR_Horas': 'sum'
    }).reset_index()

    return df_tmr_dia_OPV, df_tmr_mes_OPV, df_tmr_ano_OPV

# IS

def IS_Pessoa(dfIS):
    # Copiar dataframes para evitar alterações nos originais
    df_is_dia_pessoa = dfIS.copy()

    # Trocar o nome da coluna 'Analista' por 'Tratado_Por' para padronizar com o resto das outras bases
    df_is_dia_pessoa = df_is_dia_pessoa.rename(columns={
        'Analista': 'Tratado_Por'
    })

    # Filtrando os 'Clientes' na coluna 'Devolutiva'
    df_is_dia_pessoa = df_is_dia_pessoa[df_is_dia_pessoa['Devolutiva'] == 'Cliente']
    
    # Filtrar os 'CAP' que não estão nulos
    df_is_dia_pessoa = df_is_dia_pessoa[df_is_dia_pessoa['CAP'].notna()]

    # Filtrar apenas os 'Grupo_Vendedor' que não é igual a NaN
    df_is_dia_pessoa = df_is_dia_pessoa[df_is_dia_pessoa['Grupo_Vendedor'].notna()]
    
    # Agrupar por 'Tratado_Por', 'Grupo_Vendedor' e 'Data' somando 'Qtd_Etapas' e 'TMR_Horas'
    df_is_dia_pessoa = df_is_dia_pessoa.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Data', 'NPS_Resolvido', 'Canal']).agg({
        'Contador': 'sum',
        'NPS_Nota': 'sum'
    }).reset_index()

    # Vou abrir a data por mês e ano
    df_is_dia_pessoa['Ano'] = df_is_dia_pessoa['Data'].dt.year
    df_is_dia_pessoa['Mes'] = df_is_dia_pessoa['Data'].dt.month

    # Mês
    df_is_mes_pessoa = df_is_dia_pessoa.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Mes', 'Ano', 'NPS_Resolvido', 'Canal']).agg({
        'Contador': 'sum',
        'NPS_Nota': 'sum'
    }).reset_index()

    # Ano
    df_is_ano_pessoa = df_is_dia_pessoa.groupby(['Tratado_Por', 'Grupo_Vendedor', 'Ano', 'NPS_Resolvido', 'Canal']).agg({
        'Contador': 'sum',
        'NPS_Nota': 'sum'
    }).reset_index()

    return df_is_dia_pessoa, df_is_mes_pessoa, df_is_ano_pessoa

def IS_Grupo(dfIS):
    # Copiar dataframes para evitar alterações nos originais
    df_is_dia_grupo = dfIS.copy()

    # Filtrando os 'Clientes' na coluna 'Devolutiva'
    df_is_dia_grupo = df_is_dia_grupo[df_is_dia_grupo['Devolutiva'] == 'Cliente']

    # Filtrar os 'CAP' que não estão nulos
    df_is_dia_grupo = df_is_dia_grupo[df_is_dia_grupo['CAP'].notna()]

    # Filtrar apenas os 'Grupo_Vendedor' que não é igual a NaN
    df_is_dia_grupo = df_is_dia_grupo[df_is_dia_grupo['Grupo_Vendedor'].notna()]
    
    # Agrupar por 'Grupo_Vendedor' e 'Data' somando 'Qtd_Etapas' e 'TMR_Horas'
    df_is_dia_grupo = df_is_dia_grupo.groupby(['Grupo_Vendedor', 'Data', 'NPS_Resolvido', 'Canal']).agg({
        'Contador': 'sum',
        'NPS_Nota': 'sum'
    }).reset_index()

    # Vou abrir a data por mês e ano
    df_is_dia_grupo['Ano'] = df_is_dia_grupo['Data'].dt.year
    df_is_dia_grupo['Mes'] = df_is_dia_grupo['Data'].dt.month

    # Mês
    df_is_mes_grupo = df_is_dia_grupo.groupby(['Grupo_Vendedor', 'Mes', 'Ano', 'NPS_Resolvido', 'Canal']).agg({
        'Contador': 'sum',
        'NPS_Nota': 'sum'
    }).reset_index()

    # Ano
    df_is_ano_grupo = df_is_dia_grupo.groupby(['Grupo_Vendedor', 'Ano', 'NPS_Resolvido', 'Canal']).agg({
        'Contador': 'sum',
        'NPS_Nota': 'sum'
    }).reset_index()

    return df_is_dia_grupo, df_is_mes_grupo, df_is_ano_grupo

def IS_OPV(dfIS):
    # Copiar dataframes para evitar alterações nos originais
    df_is_dia_opv = dfIS.copy()

    # Filtrando os 'Clientes' na coluna 'Devolutiva'
    df_is_dia_opv = df_is_dia_opv[df_is_dia_opv['Devolutiva'] == 'Cliente']

    # Filtrar os 'CAP' que não estão nulos
    df_is_dia_opv = df_is_dia_opv[df_is_dia_opv['CAP'].notna()]
    
    # Filtrar apenas os 'Grupo_Vendedor' que não é igual a NaN
    df_is_dia_opv = df_is_dia_opv[df_is_dia_opv['Grupo_Vendedor'].notna()]

    # Agrupar por 'Grupo_Vendedor' e 'Data' somando 'Qtd_Etapas' e 'TMR_Horas'
    df_is_dia_opv = df_is_dia_opv.groupby(['Data', 'NPS_Resolvido', 'Canal']).agg({
        'Contador': 'sum',
        'NPS_Nota': 'sum'
    }).reset_index()

    # Vou abrir a data por mês e ano
    df_is_dia_opv['Ano'] = df_is_dia_opv['Data'].dt.year
    df_is_dia_opv['Mes'] = df_is_dia_opv['Data'].dt.month

    # Mês
    df_is_mes_opv = df_is_dia_opv.groupby(['Mes', 'Ano', 'NPS_Resolvido', 'Canal']).agg({
        'Contador': 'sum',
        'NPS_Nota': 'sum'
    }).reset_index()

    # Ano
    df_is_ano_opv = df_is_dia_opv.groupby(['Ano', 'NPS_Resolvido', 'Canal']).agg({
        'Contador': 'sum',
        'NPS_Nota': 'sum'
    }).reset_index()

    return df_is_dia_opv, df_is_mes_opv, df_is_ano_opv
