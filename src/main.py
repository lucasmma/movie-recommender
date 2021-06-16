from flask import Flask
from MovieRecomendation import MovieRecomendation

app = Flask(__name__)


@app.route("/")
def main():
    return "<h1>Hello World</h1>"


if __name__ == "__main__":
    # app.run(debug=True)
    while True:
        movie_name = input("Digite o nome de um filme")
        if movie_name == "-1":
            break
        MovieRecomendation().get_recomendation(movie_name)
