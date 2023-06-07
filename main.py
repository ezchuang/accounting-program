
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
import re
import datetime
import pandas as pd
# import numpy as np
import sys

import colorama
from colorama import Fore 
from colorama import Style
"""
功能上 Fore.GREEN == "\033[32m"，實質上是有落差的，差在哪不知道
"\033[32m" <- ANSI code of green
    \033 -> Escape character -> ESC[
    ESC[ -> Control Sequence Introducer
    32 -> green
    m -> SGR（Select Graphic Rendition）結束    !!SGR是什麼我沒去查

功能上 Style.BRIGHT == \033[1m
功能上 Style.RESET_ALL == \033[0m
在 Print() 加上 bold and green: \033[1;32m
RGB mode: ESC[38;2;{r};{g};{b}m
256 colors mode: ESC[38;5;{ID}m
"""
colorama.init()

# 將 date 格式統一
def reformat_date(date_str):
    patt_for_date = re.compile(r"[\/\.\-\,]")
    date_parts = re.split(patt_for_date, date_str)
    return "/".join(date_parts)

# csv 資料整理
def data_clean_up(path):
    data = pd.read_csv(path)
    data = data.fillna("na") # 填充字元
    data = data.applymap(lambda x: x.lower() if isinstance(x, str) else x) # 轉小寫
    data["amount"] = data["amount"].apply(lambda x: 0 if x=="na" else x) # amount 空格 賦予 0
    data["date"] = data["date"].apply(lambda x: str( datetime.date.today() ) if x=="na" else reformat_date(x)) # date 空格 賦予 今日
    data.sort_values(by = ["date", "main_ctgr", "sub_ctgr"], inplace = True) # 針對日期排序
    
    return data
    """
    修改大小寫，為什麼不能這樣寫?
    for i in data:
        print(i)
        data = data[i].str.lower()
    """


select_ipt_mode, select_opt_mode = "", ""
while True:
    # select_ipt_mode = input(
    #     Fore.YELLOW + Style.BRIGHT + "csv批次輸入 請輸入 0\n單筆資料輸入 請輸入 1\n輸入請選擇模式: " + Style.RESET_ALL
    #     )
    # select_opt_mode = input(
    #     Fore.YELLOW + Style.BRIGHT + "建立新的帳務檔案 請輸入 0\n新增資料到既有檔案 請輸入 1 (請確保既有檔案有放入此資料夾中，並將其命名為 \"記帳程式用-紀錄\")\n輸出請選擇模式: " + Style.RESET_ALL
    #     )
    # 測試用
    select_ipt_mode="0"
    select_opt_mode="0"

    if (select_ipt_mode == "0" or select_ipt_mode == "1") or\
        (select_opt_mode == "0" or select_opt_mode == "1"):
        break
    print("模式選擇異常")

# 輸入模式切換
if select_ipt_mode == "0": # input csv
    print(Fore.RED + Style.BRIGHT + "請將目標csv檔案與本程式放置於相同資料夾中" + Style.RESET_ALL)
    # path = input(Fore.YELLOW + Style.BRIGHT + "請輸入csv檔案名稱: " + Style.RESET_ALL)
    # 測試用
    path = "記帳程式用 - 範例"

    if ".csv" not in path:
        path += ".csv"
    data = data_clean_up(path)
else: # 個別資料 input
    print("尚未完成，完成期限遙遙無期")

# 輸出模式切換
if select_opt_mode == "0": # 建立新檔案
    data.to_csv("記帳程式用-紀錄.csv", index = False)
    print(Fore.GREEN + "完成" + Style.RESET_ALL)
    print(Fore.BLUE + Style.BRIGHT + "新帳務檔案檔名為: 記帳程式用-紀錄.csv" + Style.RESET_ALL)
else: # 修改舊檔案
    """
    1. mode = "a"，可用於 .to_csv() 中，此 arg 會同 open() 的設定方式，"a" 表示加在檔案內資料的後面
    2. .tell()，會 return 指向之記憶體位置，"==0" 表 path_tmp 為空或不存在，則需加入 header
    """
    path_be_modify = input("請輸入欲修改的檔案: ")
    with open(path_be_modify, "a") as path_tmp:
        if path_tmp.tell() == 0:
            print(Fore.RED + Style.BRIGHT + "檔案不存在，自動新建" + Style.RESET_ALL)
        data.to_csv(path_tmp, header = (path_tmp.tell() == 0), index = False)
        print(Fore.GREEN + "完成" + Style.RESET_ALL)
        print(Fore.BLUE + Style.BRIGHT + path_be_modify + Style.RESET_ALL)


# 呼叫資料
select_show_data = input(Fore.YELLOW + Style.BRIGHT + "是否需要調取資料(是請按 0，否請按 1): " + Style.RESET_ALL)
if select_show_data == "1":
    sys.exit(Fore.GREEN + "程式結束" + Style.RESET_ALL)

while True:
    select_which_data = input(Fore.YELLOW + Style.BRIGHT +
                            "請輸入您想顯示的分類方式: \n" +
                            "name (不分類)請輸入 0\n" +
                            "main category 請輸入 1\n" +
                            "sub category 請輸入 2\n" +
                            "tag 請輸入 3\n" +
                            "date 請輸入 4\n" +
                            "結束程序請輸入 5\n" +
                            "請輸入您的選擇: " +
                            Style.RESET_ALL)
    items_dict = {
        "0" : "name",
        "1" : "main_ctgr",
        "2" : "sub_ctgr",
        "3" : "tag",
        "4" : "date",
    }
    header_dict = {
        "0" : "Name",
        "1" : "Main Category",
        "2" : "Sub Category",
        "3" : "Tag",
        "4" : "Date",
    }
    if select_which_data in items_dict:
        select_show_data_mode = input(Fore.YELLOW + Style.BRIGHT + "圖表顯示請輸入 0\n顯示於本程式內請輸入 1\n請輸入您的選擇(會依總金額排序): " + Style.RESET_ALL)
    elif select_which_data == "5":
        sys.exit(Fore.GREEN + "程式結束" + Style.RESET_ALL)
    else:
        print(Fore.RED + Style.BRIGHT + "輸入異常" + Style.RESET_ALL)

    if select_show_data_mode == "0": # 呼叫副程式 opt_to_chart 將指定的 data 轉成 Pie
        import opt_to_chart
        opt_to_chart.pie_base(data[ items_dict[select_which_data], header_dict[3] ], items_dict[select_which_data])
    else:
        print(data[ items_dict[select_which_data], items_dict[3] ]) # 尚未實驗過是否可行





# 寫不出來，想要於完成後呼叫其他程式打開該檔案
# import subprocess

# def open_file_with_vscode(file_path):
#     try:
#         subprocess.Popen(['code', file_path])
#     except FileNotFoundError:
#         print("无法找到VSCode安装路径，请确保已正确安装VSCode。")
# # 用法示例
# file_path = 'G:\Files\code\GitHub\accounting\記帳程式用 - 紀錄.csv'
# open_file_with_vscode(file_path)