"""从本地 SQLite 数据库读取虚构活动并通过 FastAPI 返回。"""

import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException


DB_FILE = Path(__file__).with_name("activities.db")
app = FastAPI(title="活动 API")


def initialize_database():
    """首次运行时建立活动表并放入两条虚构样例。"""
    with sqlite3.connect(DB_FILE) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        count = connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        if count == 0:
            connection.executemany(
                "INSERT INTO events (id, name) VALUES (?, ?)",
                [(1, "机器人体验"), (2, "校园摄影")],
            )


initialize_database()


@app.get("/events")
def list_events():
    with sqlite3.connect(DB_FILE) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            "SELECT id, name FROM events ORDER BY id"
        ).fetchall()
    return [dict(row) for row in rows]


@app.get("/events/{event_id}")
def get_event(event_id: int):
    # TODO：按 event_id 查询一项活动。

    with sqlite3.connect(DB_FILE) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT id, name FROM events WHERE id = ?", (event_id,)
        ).fetchone()

        # 找不到记录时，用 HTTP 404 告诉客户端资源不存在。
        if row is None:
            # 在这里抛出 404
            raise HTTPException(status_code=404, detail="活动不存在")
    return dict(row)
