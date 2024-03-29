import requests
import csv
import pandas as pd

def get_app_id(game_name):
    # URL da API
    url = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json'
    
    
    response = requests.get(url)
    
    
    if response.status_code == 200:
        
        data = response.json()
        
        
        for app in data['applist']['apps']:
            if app['name'].lower() == game_name.lower():
                return app['appid']
    
    return None

def scrape_steam_data(input_csv, output_csv):
    
    data_with_ids = []
    
    
    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            game_name = row['Nome']
            
            # Obtendo o ID 
            app_id = get_app_id(game_name)
            
            if app_id:
                
                row['ID do Aplicativo'] = int(app_id) 
            else:
                
                row['ID do Aplicativo'] = None
            
            data_with_ids.append(row)
    
    
    df = pd.DataFrame(data_with_ids)
    
    
    df.to_csv(output_csv, index=False)


scrape_steam_data('jogosSortAllTimePeak.csv', 'jogos_com_ids.csv')
