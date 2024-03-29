import pandas as pd
import requests
import re

# Remove códigos HTML, códigos de escape e URLs.
def limpar_texto(texto):
    texto = texto.replace('\n\r', ' ')
    texto = texto.replace('\r\n', ' ')
    texto = texto.replace('\r \n', ' ')
    texto = texto.replace('\r', ' ')
    texto = texto.replace('\n', ' ')
    texto = texto.replace('\t', ' ')
    texto = texto.replace('&quot;', "'")
    texto = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', texto, flags=re.MULTILINE)
    texto = re.sub('<[^<]+?>', ' ', texto)
    texto = re.sub(' +', ' ', texto)
    texto = texto.lstrip(' ')
    return texto

# Formata o preço de centavos para a forma xx.xx
def formatar_preco(preco):
    if preco == 0:
        return '0.00'
    preco_str = str(preco)
    if len(preco_str) == 1:
        preco_str = '0' + preco_str
    preco_formatado = preco_str[:-2] + '.' + preco_str[-2:]
    return preco_formatado

# Função para obter os dados do jogo a partir do ID
def obter_dados_jogo(id):
    url = f'https://store.steampowered.com/api/appdetails/?appids={id}'
    resposta = requests.get(url)
    if resposta.status_code == 200:
        return resposta.json().get(str(id), {}).get('data', {})
    else:
        return None

# Lendo o arquivo CSV 
df = pd.read_csv('jogos_com_ids_corrigido.csv')

# listas vazias para armazenar os novos dados
novas_descricoes = []
novas_categorias = []
novos_generos = []
novas_plataformas = []
novas_idades_necessarias = []
novos_gratis = []
novas_idiomas_suportados = []
novos_desenvolvedores = []
novos_publicadores = []
novas_recomendacoes = []
novas_conquistas = []
novas_data_lancamento = []
novos_classificacoes_usk = []
novos_classificacoes_agcom = []
novos_classificacoes_cadpa = []
novos_classificacoes_dejus = []
novos_precos = []
novas_dlcs = []
novos_metacritic = []
novas_requisitos_pc = []

# Iterando 
for id in df['ID do Aplicativo']:
    if id != -1:
        dados_jogo = obter_dados_jogo(id)
        if dados_jogo:
            # Adicionando dados às listas
            novas_descricoes.append(limpar_texto(dados_jogo.get('detailed_description', '')))
            novas_categorias.append(', '.join([categoria['description'] for categoria in dados_jogo.get('categories', [])]))
            novos_generos.append(', '.join([genero['description'] for genero in dados_jogo.get('genres', [])]))
            novas_plataformas.append(', '.join([plataforma for plataforma, disponivel in dados_jogo.get('platforms', {}).items() if disponivel]))
            novas_idades_necessarias.append(dados_jogo.get('required_age', ''))
            novos_gratis.append(dados_jogo.get('is_free', ''))
            novas_idiomas_suportados.append(limpar_texto(dados_jogo.get('supported_languages', '')))
            novos_desenvolvedores.append(', '.join(dados_jogo.get('developers', [])))
            novos_publicadores.append(', '.join(dados_jogo.get('publishers', [])))
            novas_recomendacoes.append(dados_jogo.get('recommendations', {}).get('total', ''))
            novas_conquistas.append(dados_jogo.get('achievements', {}).get('total', ''))
            novas_data_lancamento.append(dados_jogo.get('release_date', {}).get('date', ''))
            novos_classificacoes_usk.append(dados_jogo.get('age_ratings', {}).get('br', {}).get('rating', ''))
            novos_classificacoes_agcom.append(dados_jogo.get('age_ratings', {}).get('de', {}).get('rating', ''))
            novos_classificacoes_cadpa.append(dados_jogo.get('age_ratings', {}).get('au', {}).get('rating', ''))
            novos_classificacoes_dejus.append(dados_jogo.get('age_ratings', {}).get('ru', {}).get('rating', ''))
            if dados_jogo.get('is_free', False):
                novos_precos.append(0)
            else:
                novos_precos.append(formatar_preco(dados_jogo.get('price_overview', {}).get('final', '')))
            novas_dlcs.append(len(dados_jogo.get('dlc', [])))
            novos_metacritic.append(dados_jogo.get('metacritic', {}).get('score', ''))
            requisitos_pc = dados_jogo.get('pc_requirements', [])
            if isinstance(requisitos_pc, list):
                novas_requisitos_pc.append('')
            else:
                novas_requisitos_pc.append(limpar_texto(requisitos_pc.get('minimum', '')))

        else:
            
            novas_descricoes.append('')
            novas_categorias.append('')
            novos_generos.append('')
            novas_plataformas.append('')
            novas_idades_necessarias.append('')
            novos_gratis.append('')
            novas_idiomas_suportados.append('')
            novos_desenvolvedores.append('')
            novos_publicadores.append('')
            novas_recomendacoes.append('')
            novas_conquistas.append('')
            novas_data_lancamento.append('')
            novos_classificacoes_usk.append('')
            novos_classificacoes_agcom.append('')
            novos_classificacoes_cadpa.append('')
            novos_classificacoes_dejus.append('')
            novos_precos.append('')
            novas_dlcs.append('')
            novos_metacritic.append('')
            novas_requisitos_pc.append('')
    else:
        novas_descricoes.append('')
        novas_categorias.append('')
        novos_generos.append('')
        novas_plataformas.append('')
        novas_idades_necessarias.append('')
        novos_gratis.append('')
        novas_idiomas_suportados.append('')
        novos_desenvolvedores.append('')
        novos_publicadores.append('')
        novas_recomendacoes.append('')
        novas_conquistas.append('')
        novas_data_lancamento.append('')
        novos_classificacoes_usk.append('')
        novos_classificacoes_agcom.append('')
        novos_classificacoes_cadpa.append('')
        novos_classificacoes_dejus.append('')
        novos_precos.append('')
        novas_dlcs.append('')
        novos_metacritic.append('')
        novas_requisitos_pc.append('')

# novas colunas 
df['Descrição'] = novas_descricoes
df['Categorias'] = novas_categorias
df['Gêneros'] = novos_generos
df['Plataformas'] = novas_plataformas
df['Idade Necessária'] = novas_idades_necessarias
df['Grátis'] = novos_gratis
df['Idiomas Suportados'] = novas_idiomas_suportados
df['Desenvolvedores'] = novos_desenvolvedores
df['Publicadores'] = novos_publicadores
df['Recomendações'] = novas_recomendacoes
df['Conquistas'] = novas_conquistas
df['Data de Lançamento'] = novas_data_lancamento
df['Classificação USK'] = novos_classificacoes_usk
df['Classificação AGCOM'] = novos_classificacoes_agcom
df['Classificação CADPA'] = novos_classificacoes_cadpa
df['Classificação DEJUS'] = novos_classificacoes_dejus
df['Preço'] = novos_precos
df['Numero de DLCs'] = novas_dlcs
df['Metacritic'] = novos_metacritic
df['Requisitos PC'] = novas_requisitos_pc

# Salvando
df.to_csv('jogos_dados_completos_nao_tratados.csv', index=False)
