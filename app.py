from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up SQL database
db = SQLAlchemy(app)

# Create todo item model with attributes
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    starred = db.Column(db.Boolean)

# Homepage route
@app.route('/')
def index():
    # Show all todos
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list = todo_list)

# When adding a new task, call POST method from base.html
@app.route('/add', methods=["POST"])
def add():
    # Add new item
    title = request.form.get("title")

    # Initialize todo
    new_todo = Todo(title=title, complete=False, starred=False)

    # Add todo to database
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    # Update item as completed or not
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    # Delete item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/star/<int:todo_id>')
def star(todo_id):
    # Mark item as important
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.starred = not todo.starred
    db.session.commit()
    return redirect(url_for("index"))

# Set up database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)