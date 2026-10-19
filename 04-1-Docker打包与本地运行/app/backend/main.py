"""活动报名 API：SQLite 数据库路径可由 DATABASE_PATH 环境变量设置。"""

import os
import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


DATABASE_PATH = Path(os.getenv("DATABASE_PATH", "registrations.db"))
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
app = FastAPI(title="活动报名 API")
CORS_ORIGINS = [
    origin.strip().rstrip("/")
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]
if CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type"],
    )


class RegistrationInput(BaseModel):
    username: str = Field(min_length=1, max_length=30)


def connect():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    with connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
                username TEXT NOT NULL,
                UNIQUE(event_id, username)
            );
            """
        )
        if connection.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 0:
            connection.executemany(
                "INSERT INTO events (id, name) VALUES (?, ?)",
                [(1, "机器人体验"), (2, "校园摄影"), (3, "编程入门")],
            )


initialize_database()


@app.get("/events")
def list_events():
    with connect() as connection:
        rows = connection.execute("SELECT id, name FROM events ORDER BY id").fetchall()
    return [dict(row) for row in rows]


@app.get("/events/{event_id}/registrations")
def list_registrations(event_id: int):
    with connect() as connection:
        exists = connection.execute("SELECT 1 FROM events WHERE id = ?", (event_id,)).fetchone()
        if not exists:
            raise HTTPException(status_code=404, detail="活动不存在")
        rows = connection.execute(
            "SELECT id, username FROM registrations WHERE event_id = ? ORDER BY id",
            (event_id,),
        ).fetchall()
    return [dict(row) for row in rows]


@app.post("/events/{event_id}/registrations", status_code=201)
def create_registration(event_id: int, data: RegistrationInput):
    username = data.username.strip()
    if not username:
        raise HTTPException(status_code=400, detail="用户名不能为空")
    try:
        with connect() as connection:
            connection.execute(
                "INSERT INTO registrations (event_id, username) VALUES (?, ?)",
                (event_id, username),
            )
            row = connection.execute(
                "SELECT id, username FROM registrations WHERE event_id = ? AND username = ?",
                (event_id, username),
            ).fetchone()
    except sqlite3.IntegrityError as error:
        raise HTTPException(status_code=409, detail="活动不存在或该用户已经报名") from error
    return dict(row)


@app.patch("/events/{event_id}/registrations/{registration_id}")
def update_registration(event_id: int, registration_id: int, data: RegistrationInput):
    username = data.username.strip()
    if not username:
        raise HTTPException(status_code=400, detail="用户名不能为空")
    with connect() as connection:
        cursor = connection.execute(
            "UPDATE registrations SET username = ? WHERE id = ? AND event_id = ?",
            (username, registration_id, event_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="报名记录不存在")
        row = connection.execute(
            "SELECT id, username FROM registrations WHERE id = ?", (registration_id,)
        ).fetchone()
    return dict(row)


@app.delete("/events/{event_id}/registrations/{registration_id}", status_code=204)
def delete_registration(event_id: int, registration_id: int):
    with connect() as connection:
        cursor = connection.execute(
            "DELETE FROM registrations WHERE id = ? AND event_id = ?",
            (registration_id, event_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="报名记录不存在")
