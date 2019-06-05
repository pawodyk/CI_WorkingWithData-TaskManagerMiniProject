import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DB')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_task')
def get_task():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())
    
@app.route('/add_task')
def add_task():
    return render_template("addtask.html", categories=mongo.db.categories.find())
    
@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks= mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    print("***")
    print("sucessfully added:")
    print(request.form.to_dict())
    print("***")
    return redirect(url_for('get_task'))
    

if __name__ == "__main__":
    app.run(host = os.environ.get('IP', '127.0.0.1'), 
            port = int(os.environ.get('PORT', '5500')),
            debug=True)
            