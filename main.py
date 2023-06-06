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

import pandas as pd
df = pd.read_csv('每月_160547_101_投信投顧公會境內基金配息資料.csv')
# df = pd.read_csv('Accounting information.csv')
# print("df.info()")
# df.info()
print("df.describe()")
df.describe()