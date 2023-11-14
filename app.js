const express = require('express');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const port = 3000;

// SQLiteデータベースの作成・接続
const db = new sqlite3.Database('your_database_name.db', (err) => {
    if (err) {
        console.error(err.message);
    } else {
        console.log('Connected to the SQLite database.');
    }
});

// テーブルを作成するクエリ
const createTableQuery = `
    CREATE TABLE IF NOT EXISTS store_hours (
        id INTEGER PRIMARY KEY,
        opening_time TIME,
        closing_time TIME,
        waiting_time INTEGER CHECK (waiting_time IN (0, 30, 60, 90, 120))
    );
`;

// テーブル作成
db.run(createTableQuery);

// トリガーを作成するクエリ
const createTriggerQuery = `
    CREATE TRIGGER IF NOT EXISTS update_waiting_time
    AFTER INSERT ON store_hours
    FOR EACH ROW
    BEGIN
        UPDATE store_hours
        SET waiting_time = waiting_time - 30
        WHERE id = NEW.id AND waiting_time > 0;
    END;
`;

// トリガー作成
db.run(createTriggerQuery);

// サーバーの起動
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});

// Store Hoursを追加するエンドポイント
app.post('/add_store_hour', (req, res) => {
    const { opening_time, closing_time, waiting_time } = req.body;

    const insertQuery = `
        INSERT INTO store_hours (opening_time, closing_time, waiting_time)
        VALUES (?, ?, ?)
    `;

    db.run(insertQuery, [opening_time, closing_time, waiting_time], function (err) {
        if (err) {
            return res.status(500).json({ error: err.message });
        }

        const lastId = this.lastID;

        db.get(`SELECT * FROM store_hours WHERE id = ?`, [lastId], (err, row) => {
            if (err) {
                return res.status(500).json({ error: err.message });
            }

            res.status(201).json(row);
        });
    });
});