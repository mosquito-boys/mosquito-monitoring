from flask import Flask, request, render_template, send_file
from db_model.Mosquito import Mosquito
from db_model.User import User
from classification.preprocessing import Preprocessing
import classification.command_classification as command_classification
from utilities.LRU import LRU
import utilities.Errors as Errors
import traceback

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
    try:

        # preparing variables to return in template to user
        predictions = []
        mosquito = None
        cropped_pic = None
        framed_pic = None
        file = None

        # request informations
        try:
            form = request.form
            latitude = form['latitude']
            longitude = form['longitude']
            file = request.files["fileToUpload"]
        except Exception:
            raise Errors.FormError()

        print(form)

        # extracting objects
        user = User(form["name"], form["email"])
        mosquito = Mosquito(user, file.filename, latitude, longitude, form["comment"])
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

        # BDD STORAGE
        # user part
        user_already_exists, id_user = is_user_in_db(user)
        if not user_already_exists:
            id_user = store_user(user)
        # mosquito part
        store_mosquito(id_user, mosquito)


        # STORE new USER or get existing user => id_user

        # STORE MOSQUITO

        return render_template("response.html", cropped_pic=cropped_pic, framed_pic=framed_pic, prediction=predictions,
                               mosquito=mosquito)

    except Exception as error:
        traceback.print_exc()
        # we return the error page
        if isinstance(error, Errors.InsectNotFound):
            return render_template("errors/mosquito_not_found_error.html")
        elif isinstance(error, Errors.FormError):
            return render_template("errors/form_error.html")
        elif isinstance(error, Errors.APIQuotaExceeded):
            return render_template("errors/api_quota_exceeded.html")
        else:
            return render_template("errors/generic_error.html")


if __name__ == "__main__":
    app.run()
