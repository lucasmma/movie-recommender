import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pickle5 as pickle
import numpy as np

dataset = "ml-small"


def slice_data_frame(data_frame, chunk_size):
    num_chunks = len(data_frame) // chunk_size + 1
    for i in range(num_chunks):
        yield data_frame[i*chunk_size:(i+1)*chunk_size]

def filter_dataset(dataset):
    final_dataset = dataset.pivot(index='movieId', columns='userId', values='rating')
    final_dataset.fillna(0, inplace=True)

    # filter dataset minimin votes/user in movies = 10, minimum votes in one film by user = 50
    no_user_voted = dataset.groupby('movieId')['rating'].agg('count')
    final_dataset = final_dataset.loc[no_user_voted[no_user_voted > 10].index, :]

    no_movies_voted = dataset.groupby('userId')['rating'].agg('count')
    final_dataset = final_dataset.loc[:, no_movies_voted[no_movies_voted > 50].index]
    return final_dataset

def get_datasets():
    ratings = pd.read_csv("dataset/" + dataset + "/ratings.csv")

    dataframe_size = ratings.shape[0]
    dataframe = []
    for index, datachunk in enumerate(slice_data_frame(ratings, 100000)):
        dataframe.append(pd.DataFrame(datachunk))
        percentage = ((index + 1) * 100000) / dataframe_size * 100
        if (percentage > 100.0):
            percentage = 100.0
        print("Index: {} e Progresso: {} %".format(index, percentage))
        # if(index == 3):
        #     break
    
    concatenated_dataset = pd.concat(dataframe)
    final_dataset = filter_dataset(concatenated_dataset)

    dataset_otimizado = csr_matrix(final_dataset.values)
    final_dataset.reset_index(inplace=True)

    return final_dataset, dataset_otimizado


def get_movies():
    return pd.read_csv("dataset/" + dataset + "/movies.csv")

def get_links():
    dtype = {"movieId": int, "imdbId": str, "tmdbId": str}
    return pd.read_csv("dataset/" + dataset + "/links.csv", dtype=dtype)

def save_model(modelai):
    filename = dataset + '.sav'
    pickle.dump(modelai, open(filename, 'wb'))

if(__name__ == "__main__"):
    print("Pegando datasets")
    final_dataset = get_datasets()
    print("Treinando modelo")
    model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
    model.fit(final_dataset)
    print("Salvando modelo")
    save_model(model)
    print("Modelo treinado e salvo com sucesso")
    print("Fim do processo")
