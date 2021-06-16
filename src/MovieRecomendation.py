import pandas as pd
from sklearn.neighbors import NearestNeighbors
from Utils import get_dataset, get_movies

class MovieRecomendation:
    def __init__(self):
        self.movies = get_movies()
        self.final_dataset, self.dataset_otimizado = get_dataset()

    def get_recomendation(self, movie_name):
        n_movies_to_reccomend = 10
        movie_list = self.movies[self.movies['title'].str.contains(movie_name)]
        if len(movie_list):
            movie_idx = movie_list.iloc[0]['movieId']
            movie_idx = self.final_dataset[self.final_dataset['movieId'] == movie_idx].index[0]
            distances, indices = self.model().kneighbors(self.dataset_otimizado[movie_idx], n_neighbors=n_movies_to_reccomend + 1)
            rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())),
                                       key=lambda x: x[1])[:0:-1]
            recommend_frame = []
            for val in rec_movie_indices:
                movie_idx = self.final_dataset.iloc[val[0]]['movieId']
                idx = self.movies[self.movies['movieId'] == movie_idx].index
                recommend_frame.append({'Title': self.movies.iloc[idx]['title'].values[0], 'Distance': val[1]})
            df = pd.DataFrame(recommend_frame, index=range(1, n_movies_to_reccomend + 1))
            return df
        else:
            return "No movies found. Please check your input"

    def model(self):
        return NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)