from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def renderHTML():
    return app.send_static_file("index.html")


@app.route("/postform", methods=["POST"])
def postForm():
    print(request.files)
    return "Form received !"


if __name__ == "__main__":
    app.run()
