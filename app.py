from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
today = datetime.now().strftime('%Y-%m-%d')

class TaskManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    status = db.Column(db.String(1), default='0')
    date = db.Column(db.Date)

db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    task_list = db.session.query(TaskManager).all()
    today = datetime.now().date()
    return render_template("index.html", task_list=task_list, today=today)

@app.route('/modal', methods=['GET', 'POST'])
def modal():
    return render_template("modal.html", today=today)


@app.route('/add', methods=['GET', 'POST'])
def add():
    title = request.form.get('title')
    priority = request.form.get('priority')
    description = request.form.get('description')
    status = request.form.get('status')
    date = (datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else datetime.strptime(today, '%Y-%m-%d').date())
    new_task = TaskManager(title=title, priority=priority, description=description, status=status, date=date)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    task_to_delete = db.session.query(TaskManager).filter_by(id=task_id).first()
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update status/<int:task_id>', methods=['GET', 'POST'])
def update_status(task_id):
    task_to_update = db.session.query(TaskManager).filter_by(id=task_id).first()
    if task_to_update.status == "0":
        task_to_update.status = "1"
    else:
        task_to_update.status = "0"
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update date/<int:task_id>', methods=['GET', 'POST'])
def update_date(task_id):
    task_to_update = db.session.query(TaskManager).filter_by(id=task_id).first()
    task_to_update.date = (datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else datetime.strptime(today, '%Y-%m-%d'))
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)