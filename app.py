from flask import Flask, request, render_template

app = Flask(__name__)

messages = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        messages.append({"name": name, "message": message})
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run()
