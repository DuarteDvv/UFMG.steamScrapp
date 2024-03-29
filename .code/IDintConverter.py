import pandas as pd

df = pd.read_csv('jogos_com_ids.csv')

df['ID do Aplicativo'].fillna(-1, inplace=True)


df['ID do Aplicativo'] = df['ID do Aplicativo'].astype(int)


df.to_csv('jogos_com_ids_corrigido.csv', index=False)

