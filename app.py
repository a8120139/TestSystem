from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLiteデータベースへの接続
conn = sqlite3.connect('store_hours.db')
cur = conn.cursor()

# テーブルの作成
cur.execute('''
    CREATE TABLE IF NOT EXISTS store_hours (
        id INTEGER PRIMARY KEY,
        opening_time TIME,
        closing_time TIME,
        waiting_time INTEGER CHECK (waiting_time IN (0, 30, 60, 90, 120))
    )
''')
conn.commit()

# トリガーの作成
cur.execute('''
    CREATE TRIGGER IF NOT EXISTS update_waiting_time
    AFTER INSERT ON store_hours
    FOR EACH ROW
    BEGIN
        UPDATE store_hours
        SET waiting_time = waiting_time - 30
        WHERE id = NEW.id AND waiting_time > 0;
    END
''')
conn.commit()

# データの追加
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        opening_time = request.form['opening_time']
        closing_time = request.form['closing_time']
        waiting_time = request.form['waiting_time']

        cur.execute('INSERT INTO store_hours (opening_time, closing_time, waiting_time) VALUES (?, ?, ?)', (opening_time, closing_time, waiting_time))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

# データの閲覧
@app.route('/')
def index():
    cur.execute('SELECT * FROM store_hours')
    store_hours = cur.fetchall()
    return render_template('index.html', store_hours=store_hours)

if __name__ == '__main__':
    app.run(debug=True)
