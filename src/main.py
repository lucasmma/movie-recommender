from flask import Flask, render_template, request
from MovieRecomendation import MovieRecomendation

app = Flask(__name__)


@app.route("/")
def main():

    page = "<html><head>"
    page += '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>'
    page += "<style>button{ margin-top: 16px }</style>"
    page += "</head><body>"
    page += "<input id='title'></input>"
    page += "<div id='sugestions'></div>"
    page += "<br>"
    page += """<button onclick=\'$.ajax({
      url: "/recomendation",
      type: "POST",
      data: {movie_title: $("#title").val()},
      success: function(response) {
        $("#sugestions").html(response);
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });\'>Get Recomendation</button>"""
    page += "</body></html>"

    return page


@app.route("/recomendation", methods=["POST", "GET"])
def get_recomendation():
    try:
        movie_name = request.form.get('movie_title')
        recomendations = MovieRecomendation().get_recomendation(movie_name, 10)
        seggestions_list = recomendations['Title'].values.tolist()

        print(recomendations['Title'].values.tolist())
        render_template('sugestions.html')
        return render_template('sugestions.html', suggestions=seggestions_list)
    except Exception:
        print("exception")


if __name__ == "__main__":
    app.run(debug=True)
    while True:
        movie_name = input("Digite o nome de um filme: ")
        if movie_name == "-1":
            break
        print()
