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
    return render_template("formular.html")


@app.route("/postform", methods=["POST"])
def postForm():
    form = request.form
    file = request.files["fileToUpload"]

    print("NEW REQUEST")
    print(form)
    print(file)

    # if form['Scientischeck'] == 'No':
    #     user = User(form["name"], form["email"], form['comment'])
    # else:
    #     user = Scientist(form["name"], form["email"], form['comment'], form['speciesCheck'])


    # extracting objects
    user = User(form["name"], form["email"], form['comment'])
    mosquito = Mosquito(user, file.filename)

    user_pic_path = "./dataset_to_be_validated/" + mosquito.filename
    generated_pic_path = "./static/tmp/" + mosquito.filename

    # saving file
    file.save(user_pic_path)

    # making preproc
    coords = Preprocessing.mosquito_position(user_pic_path)
    cropped_pic = Preprocessing.save_crop_img(coords, user_pic_path, generated_pic_path.replace(".jpg", "_crop.jpg"))
    framed_pic = Preprocessing.save_framed_img(coords, user_pic_path, generated_pic_path.replace(".jpg", "_framed.jpg"))

    # making predictions
    predictions = command_classification.label_automatic(cropped_pic)
    print("predictions", predictions)
    best_prediction = 0
    for species in predictions:
        if float(species[1]) > best_prediction:
            label = species[0]

    mosquito.label = label



    # BDD STORAGE !!!
    # STORE MOSQUITO
    # STORE USER
    # STORE SPECIES




    # os.remove("./static/tmp/" + file.filename)

    return render_template("response.html", cropped_pic=cropped_pic, framed_pic=framed_pic, prediction=predictions)


if __name__ == "__main__":
    app.run()
