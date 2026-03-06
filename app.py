from flask import Flask, render_template, request

app = Flask(__name__)

<<<<<<< HEAD
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
=======
students = []

@app.route("/", methods=["GET","POST"])
def index():

    search = request.args.get("search")

    if request.method == "POST":

        name = request.form["name"]
        sap = request.form["sap"]
        department = request.form["department"]
        semester = request.form["semester"]
        subject = request.form["subject"]

        assignment = int(request.form["assignment"])
        internal = int(request.form["internal"])
        final = int(request.form["final"])
        attendance = int(request.form["attendance"])

        total = assignment + internal + final
        percentage = round(total/3,2)

        student = {
            "name": name,
            "sap": sap,
            "department": department,
            "semester": semester,
            "subject": subject,
            "assignment": assignment,
            "internal": internal,
            "final": final,
            "attendance": attendance,
            "total": total,
            "percentage": percentage
        }

        students.append(student)

    filtered_students = students

    if search:
        filtered_students = [s for s in students if search in s["sap"]]

    avg = 0
    top_student = None

    if students:
        avg = round(sum(s["percentage"] for s in students)/len(students),2)
        top_student = max(students, key=lambda x: x["percentage"])

    return render_template(
        "index.html",
        students=filtered_students,
        average=avg,
        top=top_student
    )

>>>>>>> edb4f0b (Added student performance dashboard)

if __name__ == "__main__":
    app.run(debug=True)