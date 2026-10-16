# 校园活动报名小程序(任务 00-3 起始文件)
#
# 小提示:以 # 开头的是"注释",写给人看的,Python 会自动忽略。
# 阅读顺序:第一部分(数据)→ 第二部分(函数)→ 第三部分(演示)
#
# 英文单词对照:
#   event = 活动          capacity = 容量(最多多少人)
#   attendees = 报名者    student = 学生
#   remaining_seats = 剩余名额
#   sign_up = 报名        cancel_signup = 取消报名


# ===== 第一部分:数据 =====
# events 是"活动清单"(列表,用 [ ] 表示),现在只放了 1 个活动
events = [
    {  # 一个活动 = 一张"信息卡"(字典,用 { } 表示),每项是 "标签": 内容
        "name": "机器人社团开放日",  # 活动名称(文字)
        "capacity": 2,  # 最多报名人数(整数)
        "attendees": ["user1"],  # 已报名的人(列表),现在只有 user1
    }
]


# ===== 第二部分:函数 =====
# 函数 = 打包好的一套操作。括号里是"参数"(交给函数的材料),return 是函数交回的"答案"。


def remaining_seats(event):
    # 剩余名额 = 总名额 - 已报名人数(len 是"数一数有几个")
    return event["capacity"] - len(event["attendees"])


def sign_up(event, student):
    # 情况 1:这个人已经报过名 → 报名失败
    if student in event["attendees"]:
        return False
    # 情况 2:没有剩余名额了 → 报名失败
    if remaining_seats(event) <= 0:
        return False
    # 以上两种都不是 → 把名字加进名单(append = 加到末尾),报名成功
    event["attendees"].append(student)
    return True


def cancel_signup(event, student):
    # TODO:在这里实现取消报名(任务 00-3 第四步)
    # 白话步骤:
    #   如果 student 在报名名单里 → 把名字从名单中删掉,返回 True
    #   否则 → 什么都不改,返回 False
    # 提示:可以参考 sign_up 的写法;删除用 名单.remove(名字)
    return False


# ===== 第三部分:演示 =====
# main() 里按顺序写了"先做什么、再做什么",程序从这里开始执行。


def main():
    event = events[0]  # 取出清单里的第 1 个活动
    print(f"活动:{event['name']}")  # 显示活动名称
    print(f"当前报名:{event['attendees']}")  # 显示现在的报名名单
    print(f"剩余名额:{remaining_seats(event)}")  # 显示剩余名额
    signed_up = sign_up(event, "user2")  # 让 user2 报名,把返回值存进 signed_up
    print(f"user2 报名成功:{signed_up}")  # 显示是否成功(True / False)
    print(f"更新后的报名:{event['attendees']}")  # 报名后的名单
    print(f"更新后的名额:{remaining_seats(event)}")  # 报名后的剩余名额

    # 热身 5:在下面写 for 循环,逐个打印报名者的名字。
    # 补全空白后,把前面的 # 去掉:
    # for name in event["attendees"]:
    #     print(______)

    # 第四步:在这里增加"一次成功取消"和"一次取消未报名者"的演示


# 这一行的意思是:直接运行这个文件时,从 main() 开始。现在不用深究。
if __name__ == "__main__":
    main()


# ===== 热身练习答案区(用注释写答案,不要删除上面的代码)=====
# 第 1～4 题按程序开始时的 event 作答(此时 user2 还没有报名)。
# 1. 类型判断(填:文字 / 整数 / 列表)
#    event["name"] 是:
#    event["capacity"] 是:
#    event["attendees"] 是:
#    预测 len(event["attendees"]) 的结果:
#
# 2. 表达式:event["capacity"] - len(event["attendees"]) 的结果是(    ),它表示:
#
# 3. 条件:if student in event["attendees"]: 的意思是"如果(    ),就(    )"
#    名单为空时,这个条件的结果是(填 True / False):
#
# 4. 函数:remaining_seats(event) 的参数是(    ),返回值是(    )
#    写出一条调用它的语句:
#
# 5. 循环:见 main() 里的"热身 5"
