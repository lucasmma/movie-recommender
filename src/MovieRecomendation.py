import pandas as pd
from Model import get_datasets, get_movies
import pickle as pickle


class MovieRecomendation:
    def __init__(self):
        self.movies = get_movies()
        self.final_dataset, self.dataset_otimizado = get_datasets()

    def get_recomendation(self, movie_name, size):
        try:
            movie_list = self.movies[self.movies['title'].str.lower().str.contains(movie_name.lower())]
            if len(movie_list):
                movie_idx = movie_list.iloc[0]['movieId']
                if(len(self.final_dataset[self.final_dataset['movieId'] == movie_idx].index) == 0):
                    return "No movies found. Please check your input"
                movie_idx = self.final_dataset[self.final_dataset['movieId'] == movie_idx].index[0]
                distances, indices = self.model().kneighbors(self.dataset_otimizado[movie_idx],
                                                            n_neighbors=size + 1)
                rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())),
                                        key=lambda x: x[1])[:0:-1]
                # Convert distances to similarity probabilities
                # Inverse distance method: 1/distance
                inverse_distances = [1 / val[1] for val in rec_movie_indices]
                # Normalize the probabilities
                total_inverse_distance = sum(inverse_distances)
                # calculate the probabilities
                probabilities = [inv_dist / total_inverse_distance for inv_dist in inverse_distances]
                
                recommend_frame = []
                for idx, val in enumerate(rec_movie_indices):
                    movie_idx = self.final_dataset.iloc[val[0]]['movieId']
                    movie_title_idx = self.movies[self.movies['movieId'] == movie_idx].index
                    recommend_frame.append({
                        'Title': self.movies.iloc[movie_title_idx]['title'].values[0],
                        'Probability': probabilities[idx],
                        'Id': movie_idx
                    })
                df = pd.DataFrame(recommend_frame[::-1], index=range(1, size + 1))
                return df
            else:
                return "No movies found. Please check your input"
        except Exception as e:
            return "GetRecomendation Exception: " + str(e)
    @staticmethod
    def model():
        return pickle.load(open("ml-small.sav", 'rb'))
