from flask import Flask, request, render_template, send_file
from db_model.Mosquito import Mosquito
from db_model.User import User
from classification.preprocessing import Preprocessing
import os
import classification.command_classification as command_classification
from utilities.LRU import LRU

app = Flask(__name__)

LRUCache = LRU()
LRUCache.start()

@app.route("/")
def renderHTML():
    return render_template("index.html")


@app.route("/postform", methods=["POST"])
def postForm():
    form = request.form
    files = request.files

    print(form)
    print(files)

    if form['Scientischeck'] == 'No':
        user = User(form["name"], form["email"], form['comment'])
    else:
        user = Scientist(form["name"], form["email"], form['comment'], form['speciesCheck'])

    files["fileToUpload"].save("./static/tmp/" + files["fileToUpload"].filename)

    mosquito = Mosquito(user, "./static/tmp/" + files["fileToUpload"].filename)
    coords = Preprocessing.mosquito_position(mosquito.picture)
    cropped_pic = Preprocessing.save_crop_img(coords, mosquito.picture, mosquito.picture.replace(".jpg", "_crop.jpg"))
    framed_pic = Preprocessing.save_framed_img(coords, mosquito.picture, mosquito.picture.replace(".jpg", "_framed.jpg"))

    prediction = command_classification.label_automatic(cropped_pic)
    print(prediction)
    os.remove("./static/tmp/" + files["fileToUpload"].filename)

    return render_template("response.html", cropped_pic=cropped_pic, framed_pic=framed_pic, prediction=prediction)


if __name__ == "__main__":
    app.run()
