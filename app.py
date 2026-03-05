from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():

    name = None
    sap = None
    age = None
    marks = None

    if request.method == "POST":
        name = request.form["name"]
        sap = request.form["sap"]
        age = request.form["age"]
        marks = request.form["marks"]

    return render_template("index.html",
                           name=name,
                           sap=sap,
                           age=age,
                           marks=marks)

if __name__ == "__main__":
    app.run(debug=True)