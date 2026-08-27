# 📊 Radar OPV

Dashboard interativo desenvolvido em **Python + Streamlit** para acompanhamento e análise de indicadores operacionais, permitindo explorar métricas por período, grupo e diferentes dimensões de desempenho.

O projeto foi pensado para transformar dados operacionais em informações visuais e acionáveis, facilitando a identificação de tendências, desvios em relação às metas e diferenças de desempenho entre grupos e colaboradores.

A proposta é permitir que diferentes níveis de análise — do acompanhamento geral ao detalhamento por grupo e colaborador — estejam disponíveis em um único ambiente.

> **Dados melhores → análises melhores → decisões melhores.**

---

## 📸 Preview

Abaixo estão algumas imagens do dashboard, mostrando algumas das abas e funcionalidades contidas no projeto!

### Retrabalho

Visualização da evolução do indicador de retrabalho ao longo do tempo, incluindo tendência suavizada, meta e comparação entre grupos.

![Retrabalho OPV](assets/screenshots/retrabalho-selecionado.png)

### Índice de Solução

Acompanhamento do Índice de Solução mensal, com comparação contra a meta e detalhamento por canal.

![Índice de Solução](assets/screenshots/indice-solucao-geral.png)

### Produtividade

Análise da produtividade ao longo do período selecionado e comparação entre grupos.

![Produtividade](assets/screenshots/produtividade-geral.png)

---

## 🎯 Objetivo

O **Radar OPV** tem como objetivo centralizar indicadores operacionais em um único ambiente interativo, permitindo que o usuário:

- acompanhe a evolução dos indicadores ao longo do tempo;
- compare resultados com metas estabelecidas;
- filtre períodos e grupos;
- identifique tendências;
- compare grupos de forma visual;
- analise médias por colaborador;
- acompanhe diferentes indicadores em uma única aplicação;
- transforme dados operacionais em insights para tomada de decisão.

---

## 🚀 Funcionalidades

### 📅 Filtro por período

Permite selecionar o intervalo de datas utilizado nas análises.

### 👥 Filtro por grupo

Possibilita selecionar um ou mais grupos para comparar o desempenho.

### 📈 Produtividade

- evolução temporal;
- meta;
- tendência;
- comparação entre grupos;
- média por colaborador.

### ♻️ Retrabalho

- evolução do retrabalho;
- tendência suavizada;
- comparação com a meta;
- comparação entre grupos;
- média por colaborador.

### 🟢 SLA

- evolução temporal;
- comparação com a meta;
- acompanhamento do desempenho dentro do SLA;
- comparação entre grupos;
- resultado consolidado do período selecionado.

### ⏱️ TMR

- evolução temporal;
- comparação com a meta;
- acompanhamento do tempo médio de resolução/atendimento;
- comparação entre grupos;
- resultado consolidado do período selecionado.

### 😊 Índice de Solução

- evolução mensal;
- comparação com a meta;
- desempenho por canal;
- análise temporal.

---

## 🛠️ Tecnologias

O projeto utiliza principalmente:

- **Python**
- **Streamlit**
- **Pandas**
- **Plotly** ou biblioteca equivalente para visualizações interativas
- **Git/GitHub** para versionamento

---

## 📊 Dados

O dashboard depende de dados operacionais estruturados para calcular e apresentar os indicadores.

O fluxo recomendado é:

```text
Dados brutos
     ↓
Validação
     ↓
Limpeza
     ↓
Tratamento
     ↓
Cálculo dos indicadores
     ↓
Agregações
     ↓
Visualizações
     ↓
Dashboard
```

---

## 📐 Indicadores

### Produtividade

Indicador utilizado para avaliar a quantidade de produção realizada dentro da regra de negócio definida.

A fórmula exata deve ser documentada conforme a definição oficial utilizada pela operação.

---

### Retrabalho

Indicador utilizado para identificar a proporção de atividades que necessitaram de retrabalho.

A fórmula e os critérios de classificação devem seguir a regra de negócio oficial.

---

### SLA

Indicador relacionado ao cumprimento do prazo esperado para atendimento/resolução.

---

### TMR

Indicador de tempo médio, utilizado para acompanhar a duração média dos atendimentos ou processos avaliados.

---

### Índice de Solução

Indicador utilizado para medir a proporção de casos solucionados segundo a regra de negócio adotada.

O dashboard permite analisar o indicador:

- mensalmente;
- por canal;
- por período;
- em relação à meta.

---

## 🗺️ Roadmap

Possíveis evoluções:

- [ ] Indicação da data da última atualização dos dados
- [ ] Resumo executivo como visão inicial
- [ ] Drill-down de analista
- [ ] Possibilidade de colocar metas individuais/subgrupo por indicador
- [ ] Controle de acesso por usuário / Adicionar autenticação
- [ ] Comparação de períodos (presets como YTD, Mês vs Mês, Ano vs Ano...)
- [ ] Alertas automáticos
- [ ] Testes automatizados de regressão
- [ ] Tooltip com explicações do cálculo de indicadores e regras de negócio

---

## 👨‍💻 Autor

**André Barcellos Coirolo**

Projeto desenvolvido para aplicação prática de:

- análise de dados;
- visualização de dados;
- engenharia de dados;
- Python;
- Streamlit;
- indicadores operacionais;
- tomada de decisão orientada por dados.