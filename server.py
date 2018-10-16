from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def renderHTML():
    return render_template("index.html")


@app.route("/postform", methods=["POST"])
def postForm():
    print(request.files)
    # request.form
    return "Form received !"


if __name__ == "__main__":
    app.run()
