from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store_hours.db'
db = SQLAlchemy(app)

from sqlalchemy import CheckConstraint

class StoreHours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opening_time = db.Column(db.Time)
    closing_time = db.Column(db.Time)
    waiting_time = db.Column(db.Integer, default=0, nullable=False)
    
    __table_args__ = (
        CheckConstraint('waiting_time IN (0, 30, 60, 90, 120)', name='check_waiting_time'),
    )

# トリガーを模倣する関数
def update_waiting_time_after_insert(mapper, connection, target):
    store_hour = target
    if store_hour.waiting_time > 0:
        store_hour.waiting_time -= 30

# トリガーの登録
db.event.listen(StoreHours, 'after_insert', update_waiting_time_after_insert)

@app.route('/')
def index():
    store_hours = StoreHours.query.all()
    return render_template('index.html', store_hours=store_hours)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        opening_time = datetime.strptime(request.form['opening_time'], '%H:%M').time()
        closing_time = datetime.strptime(request.form['closing_time'], '%H:%M').time()
        waiting_time = int(request.form['waiting_time'])
        
        new_store_hour = StoreHours(opening_time=opening_time, closing_time=closing_time, waiting_time=waiting_time)
        db.session.add(new_store_hour)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import jsonify

# ...

@app.route('/get_store_hours', methods=['GET'])
def get_store_hours():
    store_hours = StoreHours.query.all()
    store_hours_list = [{
        'opening_time': str(hour.opening_time),
        'closing_time': str(hour.closing_time),
        'waiting_time': hour.waiting_time
    } for hour in store_hours]
    return jsonify(store_hours_list)

# ...

