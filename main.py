"""
title: accounting program

input:
    1. name: str
    2. main_ctgr: str | enum(int)
    3. sub_ctgr: str | enum(int)
    4. tag: str
    5. desc: str
    6. amount: int
    7. date: datetime.Datetime

example:
    name: "elden ring"
    main_ctgr: "entertainment"
    sub_ctgr: "game"
    tag: "steam"
    desc: str
    amount: 1290
    date: 2022/03/29
"""

import datetime
import pandas as pd
import numpy as np
data = pd.read_csv('記帳程式用 - 範例.csv')
data = data.fillna("na") # 填充字元
data = data.applymap(lambda x: x.lower() if isinstance(x, str) else x) # 轉小寫
data["amount"] = data["amount"].apply(lambda x: 0 if x=="na" else x) # amount 空格 賦予 0
data["date"] = data["date"].apply(lambda x: datetime.date.today() if x=="na" else x) # date 空格 賦予 今日
"""
為什麼不能這樣寫?
for i in data:
    print(i)
    data = data[i].str.lower()
"""


# print(df)
print(data.to_csv("記帳程式用 - 紀錄.csv"))