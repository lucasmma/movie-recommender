import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt


def get_dataset():
    ratings = pd.read_csv("../dataset/ml-latest-small/ratings.csv")
    final_dataset = ratings.pivot(index='movieId', columns='userId', values='rating')
    final_dataset.fillna(0, inplace=True)

    # filter dataset minimin votes/user in movies = 10, minimum votes in one film by user = 50
    no_user_voted = ratings.groupby('movieId')['rating'].agg('count')
    final_dataset = final_dataset.loc[no_user_voted[no_user_voted > 10].index, :]

    no_movies_voted = ratings.groupby('userId')['rating'].agg('count')
    final_dataset=final_dataset.loc[:,no_movies_voted[no_movies_voted > 50].index]

    dataset_otimizado = csr_matrix(final_dataset.values)
    final_dataset.reset_index(inplace=True)

    return dataset_otimizado, final_dataset


def main():
    dataset = get_dataset()
    # print(dataset.head())


if __name__ == "__main__":
    main()
