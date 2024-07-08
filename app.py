from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)   #setup Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'   #configure app for database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)    #create database

class Todo(db.Model):                               #objects to be stored in database based on this model
    id = db.Column(db.Integer, primary_key = True)  #column of model: id, holds integer, contains boolean indicating completed or not
    title = db.Column(db.String(100))               #title of To-do Task, is a String of max length 100
    complete = db.Column(db.Boolean)                #is the task complete or not


@app.route("/")     #landing page
def index():
    #show all todos
    todo_list = Todo.query.all()
    print(todo_list)

    return render_template("base.html", todo_list=todo_list)     #get HTML file and pass in todo_list to display using jinja

@app.route("/about")
def about():
    return "About Us"

@app.route("/add", methods = ["POST"])  #post method
def add():
    #add new item
    title = request.form.get("title")                   #get title from HTML input form
    new_todo = Todo(title = title, complete = False)    #new to-do item with title from user
    db.session.add(new_todo)                            #add new to do to database
    db.session.commit()                                 #update database
    return redirect(url_for("index"))                   #redirect to url after adding

@app.route("/update/<int:todo_id>")  #update method
def update(todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()   #get first instance of matching id
    todo.complete = not todo.complete                   #switch complete status
    db.session.commit()                                 #update database
    return redirect(url_for("index"))                   #redirect to url after updating

@app.route("/delete/<int:todo_id>")  #delete method
def delete(todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()   #get first instance of matching id
    db.session.delete(todo)                             #delete first instance of matching id
    db.session.commit()                                 #update database
    return redirect(url_for("index"))                   #redirect to url after deleting

if __name__ == "__main__":      #convention
    with app.app_context():
        db.create_all()         #initializes database

    app.run(debug = True)       #allows Flask app to run by running python file, otherwise use Flask run; debug = True runs app in development mode