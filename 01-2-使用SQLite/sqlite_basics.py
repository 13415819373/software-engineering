"""SQLite 基础：建表、插入虚构数据并查询。"""

import sqlite3
from pathlib import Path


DB_FILE = Path(__file__).with_name("registrations.db")
student_name = "user1"

events = [
    (1, "机器人体验"),
    (2, "校园摄影"),
]
registrations = [
    (1, 1, "user1"),
    (2, 1, "user2"),
    (3, 2, "user1"),
]

with sqlite3.connect(DB_FILE) as connection:
    cursor = connection.cursor()

    # TODO 1：创建 events 表。
    # 字段：id（整数主键）、name（必填文字）。

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
    )

    # TODO 2：创建 registrations 表。
    # 字段：id（整数主键）、event_id（必填整数，关联 events.id）、
    # student_name（必填文字）。

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY,
            event_id INTEGER NOT NULL,
            student_name TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
        """
    )

    # TODO 3：为了可重复运行，先清空旧数据（先 registrations，再 events），
    #         然后把 events 和 registrations 中的数据分别插入对应的表。

    cursor.execute("DELETE FROM registrations")
    cursor.execute("DELETE FROM events")

    cursor.executemany("INSERT INTO events (id, name) VALUES (?, ?)", events)
    cursor.executemany("INSERT INTO registrations (id, event_id, student_name) VALUES (?, ?, ?)", registrations)

    # TODO 4：查询并打印全部报名记录；结果中同时显示活动名和报名者。
    cursor.execute("SELECT events.name, registrations.student_name FROM events JOIN registrations ON events.id = registrations.event_id")
    for row in cursor.fetchall():
        print(row)

    print('-----------------------')

    # TODO 5：用参数化查询筛选 student_name，打印这个人报名的活动名称。
    cursor.execute("SELECT events.name FROM events JOIN registrations ON events.id = registrations.event_id WHERE registrations.student_name = ?", (student_name,))
    for row in cursor.fetchall():
        print(row)

print(f"SQLite 数据库文件已生成：{DB_FILE.name}")
