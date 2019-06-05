import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.getenv('MONGO_DB')
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

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
    tasks = mongo.db.tasks
    form_data = request.form.to_dict()
    tasks.insert_one(form_data)
    print("***")
    print("sucessfully added:")
    print(form_data)
    print("***")
    return redirect(url_for('get_task'))
    
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.categories.find()
    
    return render_template('edittask.html', task=the_task, categories=all_categories)
    
@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'task_name':request.form.get('task_name'),
        'category_name':request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for('get_task'))
    
    
@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_task'))

if __name__ == "__main__":
    app.run(host = os.getenv('IP', '127.0.0.1'), 
            port = int(os.getenv('PORT', '5500')),
            debug=True)
            