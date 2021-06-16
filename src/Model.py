import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pickle


def get_datasets():
    ratings = pd.read_csv("../dataset/ml-latest-small/ratings.csv")
    final_dataset = ratings.pivot(index='movieId', columns='userId', values='rating')
    final_dataset.fillna(0, inplace=True)

    # filter dataset minimin votes/user in movies = 10, minimum votes in one film by user = 50
    no_user_voted = ratings.groupby('movieId')['rating'].agg('count')
    final_dataset = final_dataset.loc[no_user_voted[no_user_voted > 10].index, :]

    no_movies_voted = ratings.groupby('userId')['rating'].agg('count')
    final_dataset = final_dataset.loc[:, no_movies_voted[no_movies_voted > 50].index]

    dataset_otimizado = csr_matrix(final_dataset.values)
    final_dataset.reset_index(inplace=True)

    return final_dataset, dataset_otimizado


def get_movies():
    return pd.read_csv("../dataset/ml-latest-small/movies.csv")


def save_model(modelai):
    filename = 'smallest_dataset.sav'
    pickle.dump(modelai, open(filename, 'wb'))


final_dataset, dataset_otimizado = get_datasets()
model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
model.fit(dataset_otimizado)
save_model(model)
