"""演示内存数据与 JSON 文件数据的区别。"""

import json
from pathlib import Path


DATA_FILE = Path(__file__).with_name("registrations.json")

# 这份名单只在本次程序运行时保存在内存里。
attendees_in_memory = ["user1", "user2"]
attendees_in_memory.append("user4")
print("本次运行中，内存里的名单：", attendees_in_memory)

# 首次运行时创建文件；之后运行时从文件读取已有名单。
if DATA_FILE.exists():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        saved_attendees = json.load(file)
else:
    saved_attendees = ["user1", "user2"]

# TODO：把 user3 改成另一个虚构用户名，再运行程序观察 JSON 的变化。
new_attendee = "user33"
if new_attendee not in saved_attendees:
    saved_attendees.append(new_attendee)

# 将更新后的名单写入文件，确保下次运行仍能读到。
with DATA_FILE.open("w", encoding="utf-8") as file:
    json.dump(saved_attendees, file, ensure_ascii=False, indent=2)

print("保存并读回的名单：", saved_attendees)

print(f"数据文件位置：{DATA_FILE}")
