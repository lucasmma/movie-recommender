import pandas as pd
from Model import get_datasets, get_movies
import pickle


class MovieRecomendation:
    def __init__(self):
        self.movies = get_movies()
        self.final_dataset, self.dataset_otimizado = get_datasets()

    def get_recomendation(self, movie_name, size):
        movie_list = self.movies[self.movies['title'].str.contains(movie_name)]
        if len(movie_list):
            movie_idx = movie_list.iloc[0]['movieId']
            movie_idx = self.final_dataset[self.final_dataset['movieId'] == movie_idx].index[0]
            distances, indices = self.model().kneighbors(self.dataset_otimizado[movie_idx],
                                                         n_neighbors=size + 1)
            rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())),
                                       key=lambda x: x[1])[:0:-1]
            recommend_frame = []
            for val in rec_movie_indices:
                movie_idx = self.final_dataset.iloc[val[0]]['movieId']
                idx = self.movies[self.movies['movieId'] == movie_idx].index
                recommend_frame.append({'Title': self.movies.iloc[idx]['title'].values[0], 'Distance': val[1]})
            df = pd.DataFrame(recommend_frame, index=range(1, size + 1))
            return df
        else:
            return "No movies found. Please check your input"

    @staticmethod
    def model():
        return pickle.load(open("ml-small.sav", 'rb'))
