from todo import app,mongo
from flask import render_template, request, flash, url_for, redirect

from bson import ObjectId

from .forms import Todoform
from datetime import datetime

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods = ['POST', 'GET'])
def add_todo():
    if request.method == 'POST':
        todo = Todoform(request.form)
        todo_name = todo.name.data
        todo_description = todo.description.data
        completed = todo.completed.data

        mongo.db.todo.insert_one({
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            "date_created": datetime.utcnow()
        })

        flash("Todo Successfully added", "success")
        return redirect('/view')
    else:
        form = Todoform()
    return render_template('add_todo.html', form = form, title='Add todo')

@app.route('/view')
def view_todo():
    todos = []
    for tod in mongo.db.todo.find().sort("date_created", -1):
        tod["_id"] = str(tod["_id"])
        tod["date_created"] = tod["date_created"].strftime("%b %d %Y %H:%M:%S")
        todos.append(tod)
    return render_template('view_todo.html', todos = todos, title='View todo')

@app.route('/delete_todo/<id>')
def delete_todo(id):
    mongo.db.todo.find_one_and_delete({"_id": ObjectId(id)})
    flash("Todo Successfully deleted", "success")
    return redirect('/view')

@app.route("/update_todo/<id>", methods= ['POST', 'GET'])
def update_todo(id):
    if request.method == 'POST':
        form = Todoform(request.form)
        todo_name = form.name.data
        todo_description = form.description.data
        completed = form.completed.data

        mongo.db.todo.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            "date_created": datetime.utcnow()
        }})
        flash = ("Todo successfully updated", "success")
        return redirect('/view')
    else:
        form = Todoform()

        todo = mongo.db.todo.find_one_or_404({"_id": ObjectId(id)})
        print(todo)
        form.name.data = todo.get("name", None)
        form.description.data = todo.get("description", None)
        form.completed.data = todo.get("completed",None)

    return render_template("add_todo.html", form=form)
