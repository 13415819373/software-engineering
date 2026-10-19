"""从本地 SQLite 数据库读取虚构活动并通过 FastAPI 返回。"""

import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_FILE = Path(__file__).with_name("activities.db")
app = FastAPI(title="活动 API")

# 跨域
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RegistrationIn(BaseModel):
    username: str


def initialize_database():
    """首次运行时建立活动表并放入两条虚构样例。"""
    with sqlite3.connect(DB_FILE) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """
        )
        count = connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        if count == 0:
            connection.executemany(
                "INSERT INTO events (id, name) VALUES (?, ?)",
                [(1, "机器人体验"), (2, "校园摄影")],
            )

        ## 第一步：增加报名数据表
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                event_id INTEGER NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events(id)
            )
        """
        )


initialize_database()


@app.get("/events")
def list_events():
    with sqlite3.connect(DB_FILE) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute("SELECT id, name FROM events ORDER BY id").fetchall()
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


## 第二步：新增报名（Create）
@app.post("/events/{event_id}/registrations", status_code=201)
def create_registration(event_id: int, body: RegistrationIn):
    with sqlite3.connect(DB_FILE) as connection:
        # 1. 查活动是否存在（和 get_event 里一样的写法）
        event = connection.execute(
            "SELECT id FROM events WHERE id = ?", (event_id,)
        ).fetchone()
        if event is None:
            # 在这里抛出 404
            raise HTTPException(status_code=404, detail="活动不存在")

        # 2. 插入报名，用 body.username 取用户名
        cursor = connection.execute(
            "INSERT INTO registrations (event_id, username) VALUES (?, ?)",
            (event_id, body.username),
        )
        new_id = cursor.lastrowid

    return {"id": new_id, "event_id": event_id, "username": body.username}


## 第三步：查看报名（Read）
@app.get("/events/{event_id}/registrations")
def list_registrations(event_id: int):
    with sqlite3.connect(DB_FILE) as connection:
        connection.row_factory = sqlite3.Row
        # 1. 查活动是否存在（和 get_event 里一样的写法）
        event = connection.execute(
            "SELECT id FROM events WHERE id = ?", (event_id,)
        ).fetchone()
        if event is None:
            # 在这里抛出 404
            raise HTTPException(status_code=404, detail="活动不存在")

        # 2. 查该活动的报名，用 fetchall
        rows = connection.execute(
            "SELECT id, event_id, username FROM registrations WHERE event_id = ?", (event_id,)
        ).fetchall()
    return [dict(row) for row in rows]

## 第四步：修改报名（Update）
@app.patch("/events/{event_id}/registrations/{registration_id}")
def update_registration(event_id: int, registration_id: int, body: RegistrationIn):
    with sqlite3.connect(DB_FILE) as connection:
        connection.row_factory = sqlite3.Row

        # 同时匹配报名编号和活动编号：不存在、或不属于该活动，都查不到
        row = connection.execute(
            "SELECT id FROM registrations WHERE id = ? AND event_id = ?",
            (registration_id, event_id),
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="报名记录不存在")

        connection.execute(
            "UPDATE registrations SET username = ? WHERE id = ?",
            (body.username, registration_id),
        )

    return {"id": registration_id, "event_id": event_id, "username": body.username}


## 第五步：删除报名（Delete）
@app.delete("/events/{event_id}/registrations/{registration_id}", status_code=204)
def delete_registration(event_id: int, registration_id: int):
    with sqlite3.connect(DB_FILE) as connection:
        row = connection.execute(
            "SELECT id FROM registrations WHERE id = ? AND event_id = ?",
            (registration_id, event_id),
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="报名记录不存在")

        connection.execute(
            "DELETE FROM registrations WHERE id = ?", (registration_id,)
        )