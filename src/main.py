from flask import Flask, render_template, request
from MovieRecomendation import MovieRecomendation
from Model import get_links

app = Flask(__name__)

movieRecomendation = MovieRecomendation()


@app.route("/")
def main():
    return render_template('movie-recommender.html')


@app.route("/recomendation", methods=["POST", "GET"])
def get_recomendation():
    try:
        movie_name = request.form.get('movie_title')
        recomendations = movieRecomendation.get_recomendation(movie_name, 10)
        print(recomendations)
        title_rating_list = []
        links = get_links()
        anyMoviesFound = str(recomendations) != "No movies found. Please check your input"
        if str(recomendations) != "No movies found. Please check your input":
            seggestions_list = recomendations['Title'].values.tolist()
            rating_recomendations = recomendations['Probability'].values.tolist()
            imdbIds = recomendations['Id'].values.tolist()


            for index in range(len(seggestions_list)):
                title_rating_list.append({
                    "title": seggestions_list[index] + " - " + str(rating_recomendations[index]),
                    "link": links[links['movieId'] == imdbIds[index]]['imdbId'].values[0],
                })

        return render_template('sugestions.html', suggestions=title_rating_list, not_found=not anyMoviesFound)
    except Exception as e:
        # print exceptio
        return 'Exeption: ' + str(e)
        print("exception " + str(e))


if __name__ == "__main__":
    app.run(debug=True)
