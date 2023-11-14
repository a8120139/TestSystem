-- SQLite
-- テーブルを作成する
CREATE TABLE store_hours (
    id INTEGER PRIMARY KEY,
    opening_time TIME,
    closing_time TIME,
    waiting_time INTEGER CHECK (waiting_time IN (0, 30, 60, 90, 120))
);

-- トリガーを作成して待ち時間を更新する
CREATE TRIGGER update_waiting_time
AFTER INSERT ON store_hours
FOR EACH ROW
BEGIN
    UPDATE store_hours
    SET waiting_time = waiting_time - 30
    WHERE id = NEW.id AND waiting_time > 0;
END;
