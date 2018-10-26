from flask import Flask, request, render_template, send_file
from db_model.Mosquito import Mosquito
from db_model.User import User
from classification.preprocessing import Preprocessing
import os
import classification.command_classification as command_classification
import zipfile

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

    files["fileToUpload"].save("./static/pictures/" + files["fileToUpload"].filename)

    mosquito = Mosquito(user, "./static/pictures/" + files["fileToUpload"].filename)
    coords = Preprocessing.mosquito_position(mosquito.picture)


    cropped_pic = Preprocessing.save_crop_img(coords, mosquito.picture, mosquito.picture + "_crop")
    framed_pic = Preprocessing.save_framed_img(coords, mosquito.picture, mosquito.picture + "_framed")

    prediction = command_classification.label_automatic(cropped_pic)
    print(prediction)
    os.remove("./static/pictures/" + files["fileToUpload"].filename)

    return render_template("response.html", cropped_pic=cropped_pic, framed_pic=framed_pic, prediction = prediction)

if __name__ == "__main__":
    app.run()
