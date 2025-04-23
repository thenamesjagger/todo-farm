from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.id}>"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"

    else:
        tasks = Task.query.order_by(Task.date_created).all()
        completed_count = Task.query.filter_by(completed=True).count()
        return render_template_string(TEMPLATE, tasks=tasks, completed=completed_count)

@app.route('/complete/<int:id>')
def complete(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed

    try:
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue updating your task"

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tree Todo Farm</title>
    <style>
        body { font-family: Arial, sans-serif; background: #e6ffe6; margin: 0; padding: 20px; }
        h1 { color: #2e7d32; }
        .task-form input[type="text"] { padding: 10px; width: 70%; }
        .task-form input[type="submit"] { padding: 10px; background: #66bb6a; border: none; color: white; cursor: pointer; }
        ul { list-style: none; padding: 0; }
        li { background: #dcedc8; margin: 5px 0; padding: 10px; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; }
        .completed { text-decoration: line-through; color: gray; }
        .forest { margin-top: 30px; }
        .tree { display: inline-block; margin: 5px; font-size: 2rem; }
    </style>
</head>
<body>
    <h1>🌱 Tree Todo Farm</h1>
    <form class="task-form" method="POST">
        <input type="text" name="content" placeholder="Add a new task..." required>
        <input type="submit" value="Add Task">
    </form>
    <ul>
        {% for task in tasks %}
            <li>
                <span class="{% if task.completed %}completed{% endif %}">{{ task.content }}</span>
                <span>
                    <a href="{{ url_for('complete', id=task.id) }}">✅</a>
                    <a href="{{ url_for('delete', id=task.id) }}">🗑️</a>
                </span>
            </li>
        {% endfor %}
    </ul>
    <div class="forest">
        <h2>Your Tree Farm 🌳</h2>
        {% for _ in range(completed) %}
            <span class="tree">🌳</span>
        {% endfor %}
        {% if completed == 0 %}
            <p>Complete tasks to plant trees!</p>
        {% endif %}
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

