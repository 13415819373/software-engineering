# 课程名称、已报名同学和总名额
course = "Python 入门体验课"
students = ["小林", "小周", "小陈"]
max_seats = 12


def show_summary(title, names, seats):
    # 计算已报名人数和剩余名额
    student_count = len(students)
    seats_left = seats - student_count

    # 显示课程报名情况
    print(f"课程：{title}")
    print(f"已报名人数：{student_count} 人")
    print(f"剩余名额：{seats_left} 人")
    print("报名名单：")
    for name in names:
        print(f"- {name}")


show_summary(course, students, max_seats)
