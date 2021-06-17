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
    except Exception:
        print("exception")


if __name__ == "__main__":
    app.run(debug=True, port=3000)
