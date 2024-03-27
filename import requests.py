import requests
import csv
import pandas as pd

def get_app_id(game_name):
    # URL da API da Steam para obter a lista de aplicativos
    url = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json'
    
    # Fazendo a solicitação GET para a API
    response = requests.get(url)
    
    # Verificando se a solicitação foi bem sucedida
    if response.status_code == 200:
        # Convertendo a resposta para JSON
        data = response.json()
        
        # Procurando o nome do jogo na lista de aplicativos
        for app in data['applist']['apps']:
            if app['name'].lower() == game_name.lower():
                return app['appid']
    
    return None

def scrape_steam_data(input_csv, output_csv):
    # Lista para armazenar os dados com IDs
    data_with_ids = []
    
    # Abrindo o arquivo CSV de entrada
    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        # Lendo os dados do arquivo CSV
        reader = csv.DictReader(csvfile)
        
        # Loop através das linhas do CSV
        for row in reader:
            game_name = row['Nome']
            
            # Obtendo o ID do aplicativo da Steam para o jogo
            app_id = get_app_id(game_name)
            
            if app_id:
                # Adicionando o ID à linha
                row['ID do Aplicativo'] = int(app_id) 
            else:
                # Se não encontrar o ID, define como None
                row['ID do Aplicativo'] = None
            
            # Adicionando a linha à lista de dados com IDs
            data_with_ids.append(row)
    
    # Convertendo a lista de dicionários para um DataFrame do pandas
    df = pd.DataFrame(data_with_ids)
    
    # Escrevendo o DataFrame para um novo arquivo CSV
    df.to_csv(output_csv, index=False)

# Chamando a função para raspar os dados da Steam e criar um novo arquivo CSV
scrape_steam_data('jogosSortAllTimePeak.csv', 'jogos_com_ids.csv')
