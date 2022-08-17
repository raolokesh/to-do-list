from datetime import datetime
from urllib import request
from flask import Flask,render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    todo = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.todo}"

@app.route("/" , methods =["GET","POST"])
def hello_world():
    if(request.method == "POST"):
        todo = request.form['todo']
        desc = request.form['desc']
        todo = ToDo(todo = todo, desc = desc)
        # print(todo.sno)
        db.session.add(todo)
        db.session.commit()
    alltodo= ToDo.query.all()
    # return "hello world"
    return render_template("index.html", alltodo = alltodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    alltodo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>" ,methods =['GET','POST'])
def update(sno):
    alltodoupdate = ToDo.query.filter_by(sno=sno).first()
    if(request.method == "GET"):
        return render_template("update.html",alltodoupdate=alltodoupdate)
    if(request.method == "POST"):
        alltodoupdate.sno = sno
        alltodoupdate.todo = request.form['todo']
        alltodoupdate.desc = request.form['desc']
        db.session.add(alltodoupdate)
        db.session.commit()
    return redirect("/")








if(__name__== "__main__"):
    app.run(debug=False, port=2000)