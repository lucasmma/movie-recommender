from flask import Flask, render_template, request
from MovieRecomendation import MovieRecomendation

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
        if str(recomendations) != "No movies found. Please check your input":
            seggestions_list = recomendations['Title'].values.tolist()
            rating_recomendations = recomendations['Distance'].values.tolist()

            for index in range(len(seggestions_list)):
                title_rating_list.append(seggestions_list[index] + " - " + str(rating_recomendations[index] * 2))
        else:
            title_rating_list.append("Movie not found")
        return render_template('sugestions.html', suggestions=title_rating_list)
    except Exception as e:
        # print exceptio
        return 'Exeption: ' + str(e)
        print("exception " + str(e))


if __name__ == "__main__":
    app.run(debug=True, port=3000, host='0.0.0.0')
