from flask import Flask, request, render_template, send_file
from db_model.Mosquito import Mosquito
from db_model.User import User
from classification.preprocessing import Preprocessing
import classification.command_classification as command_classification
from utilities.LRU import LRU
import utilities.Errors as Errors

app = Flask(__name__)

LRUCache = LRU()
LRUCache.start()


@app.route("/")
def renderHTML():
    return render_template("formular.html")


@app.route("/info")
def renderInfo():
    return render_template("info.html")


@app.route("/postform", methods=["POST"])
def postForm():
    # preparing variables to return in template to user
    predictions = []
    mosquito = None
    cropped_pic = None
    framed_pic = None
    file = None

    # request informations
    form = request.form
    latitude = form['latitude']
    longitude = form['longitude']
    file = request.files["fileToUpload"]

    print(form)

    try:
        # extracting objects
        user = User(form["name"], form["email"], form['comment'])
        mosquito = Mosquito(user, file.filename, latitude, longitude)
        user_pic_path = "./dataset_to_be_validated/" + mosquito.filename
        generated_pic_path = "./static/tmp/" + mosquito.filename
        # saving file
        file.save(user_pic_path)
        # making preproc
        coords = Preprocessing.mosquito_position(user_pic_path)
        cropped_pic = Preprocessing.save_crop_img(coords, user_pic_path,
                                                  generated_pic_path.replace(".jpg", "_crop.jpg"))
        framed_pic = Preprocessing.save_framed_img(coords, user_pic_path,
                                                   generated_pic_path.replace(".jpg", "_framed.jpg"))
        # making predictions
        predictions = command_classification.label_automatic(cropped_pic)
        print("predictions", predictions)
        best_prediction = 0
        for species in predictions:
            if float(species[1]) > best_prediction:
                best_prediction = float(species[1])
                predicted_label = species[0]

        mosquito.label = predicted_label


    except (TypeError, Errors.InsectNotFound, KeyError):
        print("Couldn't run prediction algorithms")

    # BDD STORAGE !!!
    # STORE MOSQUITO
    # STORE USER
    # STORE SPECIES

    return render_template("response.html", cropped_pic=cropped_pic, framed_pic=framed_pic, prediction=predictions,
                           mosquito=mosquito)


if __name__ == "__main__":
    app.run()
