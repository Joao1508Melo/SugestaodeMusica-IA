import pandas as pd
import numpy as np
import json
from youtubesearchpython import SearchVideos

pd.set_option('display.max_columns', None)  # mostra todas as colunas do dataframe
dfMusicas = pd.read_csv('dataset/spotify_dataset.csv')
dfMusicas.drop(columns=['Unnamed: 0'], inplace=True) #apaga a coluna inutil
dfMusicas.drop_duplicates(subset=['track_id'], keep='first', inplace=True) #apaga as linhas com id repetido
dfMusicas.drop_duplicates(subset=['track_name', 'artists'], keep='first', inplace=True) #apaga as musicas com mesmo nome e cantor

#algoritmo knn

def knnQuery(queryPoint, arrCharactPoints, k):
    tmp = arrCharactPoints.copy(deep=True)
    tmp['dist'] = tmp.apply(lambda x: np.linalg.norm(x - queryPoint), axis=1)
    tmp = tmp.sort_values('dist')
    return tmp.head(k).index


def querySimilars(df, columns, idx, func, param):
    arr = df[columns].copy(deep=True)
    queryPoint = arr.loc[idx]
    arr = arr.drop([idx])
    response = func(queryPoint, arr, param)
    return response


def youtubeSearchVideo(music, results=1):
    searchJson = SearchVideos(music, offset=1, mode="json", max_results=results).result()
    searchParsed = json.loads(searchJson)
    searchParsed = searchParsed['search_result'][0]
    return {'title': searchParsed['title'],
            'duration': searchParsed['duration'],
            'views': searchParsed['views'],
            'url': searchParsed['link']}


def procurarMusica(musica):
    #selectedDfMusicas = dfMusicas[dfMusicas['track_name'] == musica]
    selectedDfMusicas = dfMusicas[dfMusicas['track_name'].str.contains(musica, na=False, case=False)]
    return selectedDfMusicas.sort_values(['popularity'], ascending=False)

def procurarMusicaIndice(index):
    indiceDfMusica = dfMusicas.loc[index]
    return indiceDfMusica

def recomedarMusicas(index, pop):
    generoMsc = dfMusicas.loc[index]['track_genre']

    popMscEsc = procurarMusicaIndice(index)
    if popMscEsc['popularity'] < pop:
        pop = popMscEsc['popularity']

    filteredDfMusicas = dfMusicas[(dfMusicas['track_genre'] == generoMsc) & (dfMusicas['popularity'] >= pop)]

    columns = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']
    func, param = knnQuery, 10

    recomendadas = querySimilars(filteredDfMusicas, columns, index, func, param)
    return recomendadas