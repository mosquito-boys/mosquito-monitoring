import os
from flask import Flask, request, render_template
from flask_sslify import SSLify
from db_model.SQLiteEngine import SQLiteEngine
from db_model.Mosquito import Mosquito
from db_model.User import User
from classification.preprocessing import Preprocessing
import classification.command_classification as command_classification
from utilities.LRU import LRU
import utilities.Errors as Errors
import traceback
import datetime

app = Flask(__name__)

LRUCache = LRU()
LRUCache.start()
SQLiteEngine.create_database()

KEY_PATH = "privkey.pem"
CRT_PATH = "fullchain.pem"


def check_fix_date(date):
    """
    Checking if date is coherent and not in future. Else returning current time
    :param date: (str aaaa-mm-dd)
    :return: fixed date (str aaaa-mm-dd)
    """
    # default, using today's date
    now = datetime.datetime.now()
    ret = '-'.join([str(now.year), str(now.month), str(now.day)])

    # Flag if we can use this user's date
    date_ok = False
    date_split = date.split("-")

    # Check if date is not in future
    if len(date_split) == 3:
        [year, month, day] = date_split
        if year.isdigit() and month.isdigit() and day.isdigit():
            date_datetime = datetime.datetime(int(year), int(month), int(day))
            if date_datetime <= now:
                date_ok = True

    # React depending if date was ok
    if date_ok:
        print("Date is OK")
        ret = date
    else:
        print("Date (" + date + ") wasn't OK. Using" + ret)
    return ret


@app.route("/")
def renderHTML():
    """
    Render home page with an embedded formular to upload a mosquito pictures
    :return: formular.html
    """
    return render_template("pages/formular.html")


@app.route("/info")
def renderInfo():
    """
    Render the page with info on project and team
    :return: info.html
    """
    return render_template("pages/info.html")


@app.route("/map")
def renderMap():
    """
    Management mosquitoes rendering from database using using Google Maps API
    :return: map.html
    """
    mosquitos = SQLiteEngine.get_all_mosquitos()
    print("mosquitos in DB", mosquitos)
    return render_template("pages/map.html", mosquitos=mosquitos)


@app.route("/postform", methods=["POST"])
def postForm():
    """
    Pass information from formular to back-end and send results to response for front answer
    :return: response.html or error page
    """
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
            file = request.files["fileToUpload"]
        except Exception:
            raise Errors.FormError()

        print(form)

        # extracting objects
        user = User(form["name"], form["email"])
        latitude = form['latitude']
        longitude = form['longitude']
        date = check_fix_date(form['date'])
        mosquito = Mosquito(user, file.filename, latitude, longitude, form["comment"], date)
        user_pic_path = "./dataset_to_be_validated/" + mosquito.filename
        safe_name = ''.join(c for c in mosquito.filename if c not in '(){}<>')
        generated_pic_path = "./static/tmp/" + safe_name

        # saving file
        if not os.path.exists("./dataset_to_be_validated"):
            os.makedirs("./dataset_to_be_validated")
        file.save(user_pic_path)
        print(date)
        print(user_pic_path)
        print(generated_pic_path)

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
        predicted_label = None
        for species in predictions:
            if float(species[1]) > best_prediction:
                best_prediction = float(species[1])
                predicted_label = species[0]

        mosquito.label = predicted_label

        # user part
        user_already_exists, id_user = SQLiteEngine.is_user_in_db(user.email)
        if not user_already_exists:
            SQLiteEngine.store_user(user)

        id_user = SQLiteEngine.get_user_id(user.email)
        print("store_mosquito")
        SQLiteEngine.store_mosquito(id_user, mosquito)

        return render_template("pages/response.html", cropped_pic=cropped_pic, framed_pic=framed_pic,
                               prediction=predictions, mosquito=mosquito)

    except Exception as error:
        traceback.print_exc()
        # we return the error page
        if isinstance(error, Errors.InsectNotFound):
            return render_template("pages/errors/mosquito_not_found_error.html")
        elif isinstance(error, Errors.FormError):
            return render_template("pages/errors/form_error.html")
        elif isinstance(error, Errors.APIQuotaExceeded):
            return render_template("pages/errors/api_quota_exceeded.html")
        else:
            return render_template("pages/errors/generic_error.html")


if __name__ == "__main__":
    """
    Launch flask application, with SSL certificate if available
    """
    if os.path.exists(CRT_PATH) and os.path.exists(KEY_PATH):
        print("Loading with certificate")
        # Forcing https:// connections
        sslify = SSLify(app)
        # Running the app with certificates
        app.run(host='0.0.0.0', ssl_context=(CRT_PATH, KEY_PATH))
    else:
        print("Loading HTTP")
        app.run(host='0.0.0.0')
