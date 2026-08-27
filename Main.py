import pandas as pd
import warnings
import datetime
from src import Data_Processing as dp
from src import Dashboard as ds

warnings.filterwarnings('ignore')
pd.set_option('display.width', 2000)

# Variáveis de caminho para as bases de dados
B1 = r"data/demo"
B2 = r"data/demo/Compilado_URA"
B3 = r"data/demo/Compilado_Email"

def main():
    # Início do processamento
    inicio_base = datetime.datetime.now()
    print("Carregando bases...")
    # Carregar as bases de dados
    df_Qireal, df_Metas, df_ProdRet, df_SLA, df_TMR, df_IS_Final = dp.Load_Bases(B1, B1, B1, B1, B1, B2, B3, B1)
    # Fim Carregamento bases
    print(f"Tempo total de carregamento: {datetime.datetime.now() - inicio_base}")
    # Processar as bases de dados
    inicio_processo = datetime.datetime.now()
    print("Processando bases...")
    ds.main(df_Qireal, df_Metas, df_ProdRet, df_SLA, df_TMR, df_IS_Final)
    print("Processamento concluído!")
    print(f"Tempo total de processamento: {datetime.datetime.now() - inicio_processo}")


if __name__ == "__main__":
    main()