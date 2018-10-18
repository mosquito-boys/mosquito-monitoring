from flask import Flask, request, render_template
from classes.Mosquito import Mosquito
from classes.User import User
from classification.preprocessing import Preprocessing
import os

app = Flask(__name__)

@app.route("/")
def renderHTML():
    return render_template("index.html")


@app.route("/postform", methods=["POST"])
def postForm():
    form = request.form
    files = request.files

    print(form)
    print(files)

    user = User(form["name"], form["email"])

    files["fileToUpload"].save("./tmp/" + files["fileToUpload"].filename)

    mosquito = Mosquito(user, "./tmp/" + files["fileToUpload"].filename)

    coords = Preprocessing.mosquito_position(mosquito.picture)

    cropped_picture = Preprocessing.mosquito_croping(Preprocessing.mosquito_position(mosquito.picture), mosquito.picture)

    os.remove("./tmp/" + files["fileToUpload"].filename)

    return str(coords)

if __name__ == "__main__":
    app.run()
