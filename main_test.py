"""
title: accounting program

input:
    name: str
    main_ctgr: str | enum(int)
    sub_ctgr: str | enum(int)
    tag: str
    desc: str
    amount: int
    date: datetime.Datetime

example:
    name: "elden ring"
    main_ctgr: "entertainment"
    sub_ctgr: "game"
    tag: "steam"
    desc: str
    amount: 1290
    date: 2022/03/29
"""


bill='''
账单:6月
1.伙食费,-2000
2.零花钱,-500
3.房租,-3000
4.衣服,-1000
5.工资,+10000
6.理财,+800
7.朋友聚餐,-500
8.买衣服,-500
9.水电费,-100
10.油费,-300
11.全勤奖,+1000
12.货币基金,+600
13.手机费,-100
14.水果,-300
15.地铁+公交,-400
'''


import re
import math
account = bill.split()
# print(account)

# 將此 input 分成 月份 與 項目+金額
header, body = account[0], account[1:]
# print(header)
print(body)

# re()的其他函式要用的判斷模式(pattern)
patt = re.compile(r"[\.\,]")
# print(patt)

# 分出正負 data，因應 patt 的設計->["1."(被[1:]消除), "伙食费", "-2000"]
expend = [re.split(patt, e)[1:] for e in body if "-" in e]
income = [re.split(patt, e)[1:] for e in body if "+" in e]
# print(expend)
# print(income)

# 利用 math.fabs() 將str數值轉換成 int 再轉成 float
expend_data = [ [ e[0], math.fabs( int(e[1]) ) ] for e in expend ]
income_data = [ [ e[0], math.fabs( int(e[1]) ) ] for e in income ]
# print(expend_data)
# print(income_data)

# 總計
income_money = [e[1] for e in income_data]
# print("收入", income_money, sum(income_money))

outcome_money = [e[1] for e in expend_data]
# print("支出", outcome_money, sum(outcome_money))

remain = [re.split(patt, e)[1:][1] for e in body]
remain = [int(e) for e in remain]
# print("結餘", sum(remain))

from pyecharts import options as opts
from pyecharts.charts import Pie

# 支出
def pie_base():
    c = (
        Pie()
        .add(
            "", 
            expend_data, 
            radius=["70%", "80%"],
            center=["50%", "50%"],
            rosetype = "radius",
        )
        .set_global_opts(
            title_opts = opts.TitleOpts(title = header + "支出"),
            legend_opts = opts.LegendOpts(
                type_ = "scroll",
                pos_left = "85%",
                orient = "vertical",
            ),
        )
        .set_series_opts(
            label_opts = opts.LabelOpts(formatter = "{b}: {c}")
        )
    )
    return c

pie_base().render("支出.html")

# 收入
def pie_base():
    c = (
        Pie()
        .add(
            "", 
            expend_data, radius=["30%", "65%"],
            center=["50%", "50%"],
            rosetype = "radius",
        )
        .set_global_opts(
            title_opts = opts.TitleOpts(title = header + "收入"),
            legend_opts = opts.LegendOpts(pos_left = "15%"),
        )
        .set_series_opts(
            label_opts = opts.LabelOpts(formatter = "{b}: {c}")
        )
    )
    return c

pie_base().render("收入.html")