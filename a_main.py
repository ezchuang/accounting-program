
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
# 一般程式人員常用模組
import re
import datetime
import pandas as pd
import numpy as np
import sys

# 文字顏色模組
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

# 自訂義模組
import c_opt_to_chart
import b_data_clean_up


# 後面呼叫資料時使用，可搜尋 "呼叫資料" 就可以找到該區段的code
items_dict = {
    "0" : "name",
    "1" : "main_ctgr",
    "2" : "sub_ctgr",
    "3" : "tag",
    "4" : "date",
}
# 後面呼叫資料時使用
header_dict = {
    "0" : "Name",
    "1" : "Main Category",
    "2" : "Sub Category",
    "3" : "Tag",
    "4" : "Date",
}



# 輸入資料警示
print(Fore.YELLOW +
      "請填妥您需要使用的資料，填入資料若有空值，會在輸出時將其排除(僅僅排除該筆)\n" +
      "例如: name有填，tag沒填，amount有填\n      呼叫 name 時該筆資料會納入統計\n      但呼叫 tag 時該筆資料不會納入統計\n" +
      Style.BRIGHT +
      "盡量確保 name、main_ctgr、amount、date 有填妥\n" +
      "date 填入數值錯誤會被更改成空值" +
      Style.RESET_ALL)

while True:
    # 輸入 選項選擇
    select_ipt_mode = input(
        Fore.YELLOW + "csv批次輸入 請輸入 0\n單筆資料輸入 請輸入 1\n" + 
        Fore.CYAN + Style.BRIGHT +
        "請選擇 輸入 模式: " + 
        Style.RESET_ALL
        )
    if select_ipt_mode not in ["0", "1"]:
        print(Fore.RED + Style.BRIGHT + "模式選擇異常" + Style.RESET_ALL)
        continue
    break
# 測試用
# select_ipt_mode="1"


# 輸入 檔案確認
if select_ipt_mode == "0": # input csv
    print(Fore.YELLOW + Style.BRIGHT + "請將目標csv檔案與本程式放置於相同資料夾中" + Style.RESET_ALL)
    path_ipt = input(Fore.CYAN + Style.BRIGHT + "請輸入csv檔案名稱: " + Style.RESET_ALL)
    # 測試用
    # path = "記帳程式用 - 範例"
    # 副檔名確認
    if ".csv" not in path_ipt:
        path_ipt += ".csv"
    # csv 資料整理
    data = b_data_clean_up.data_clean_up(path_ipt)
else: # 個別資料 input
    data = b_data_clean_up.data_input_func()

while True:
    # 輸出 選項選擇
    select_opt_mode = input(
        Fore.YELLOW + 
        "建立新的帳務檔案 請輸入 0\n新增資料到既有檔案 請輸入 1 (請確保既有檔案有放入此資料夾中)\n" + 
        Fore.CYAN + Style.BRIGHT +
        "請選擇 輸出 模式: " + 
        Style.RESET_ALL
        )
    if select_opt_mode not in ["0", "1"]:
        print(Fore.RED + Style.BRIGHT + "模式選擇異常" + Style.RESET_ALL)
        continue
    break
# 測試用
# select_opt_mode="0"



# 輸出 檔案確認
# 建立新檔案
if select_opt_mode == "0": 
    path_opt_new = input(Fore.CYAN + Style.BRIGHT + "請輸入欲新增的檔案名稱: " + Style.RESET_ALL)
    # 副檔名確認
    if ".csv" not in path_opt_new:
        path_opt_new += ".csv"
    data.to_csv(path_opt_new , index = False)
    print(Fore.GREEN + "完成" + Style.RESET_ALL)
    print(Fore.BLUE + Style.BRIGHT + "新帳務檔案檔名為: " + path_opt_new + Style.RESET_ALL)
# 修改舊檔案
else:
    path_be_modify = input(Fore.CYAN + Style.BRIGHT + "請輸入欲修改的檔案: " + Style.RESET_ALL)
    # 測試用
    # path_be_modify = "記帳程式用-紀錄"
    # 副檔名確認
    if ".csv" not in path_be_modify:
        path_be_modify += ".csv"
    
    # 寫回方案 1，問答太多了，這個直接指定成預設
    # 與舊資料一起排序，再寫回(覆蓋)檔案
    # 載入舊檔案
    data_old = pd.read_csv(path_be_modify)
    # 合併舊資料和新資料
    merged_data = pd.concat([data_old, data])
    # 排序
    sorted_data = merged_data.sort_values(by=['date'])
    # 寫回檔案
    sorted_data.to_csv(path_be_modify, index=False)
    
    # 寫回方案 2
    # 加在資料最後面
    # newline = ""，避免輸入資料時會額外生成一列空白列
    # with open(path_be_modify, "a", newline = "") as path_tmp:
    #     # 檔名搜不到檔案
    #     if path_tmp.tell() == 0:
    #         print(Fore.RED + Style.BRIGHT + "檔案不存在，自動新建" + Style.RESET_ALL)
    #     # 輸出成 csv，由 path_tmp.tell() == 0 判斷是否需要加 header
    #     data.to_csv(path_tmp, header = (path_tmp.tell() == 0), index = False)
    #     """
    #     1. mode = "a"，可用於 .to_csv() 中，此 arg 會同 open() 的設定方式，"a" 表示加在檔案內資料的後面
    #     2. .tell()，會 return 指向之記憶體位置，"==0" 表 path_tmp 為空或不存在，則需加入 header
    #     """
    print(Fore.GREEN + "完成" + Style.RESET_ALL)
    print(Fore.BLUE + Style.BRIGHT + path_be_modify + Style.RESET_ALL)



# 呼叫資料
select_show_data = input(Fore.CYAN + Style.BRIGHT + "是否需要調取資料(是請按 0，否請按 1): " + Style.RESET_ALL)
# 測試用
# select_show_data = 0


# 不調取資料，直接結束程式
if select_show_data == "1":
    sys.exit(Fore.GREEN + "程式結束" + Style.RESET_ALL)



# 日期區間選擇
# 開始日期
while True:
    select_date_start = input(Fore.YELLOW + 
                            "請輸入要調取的日期區間(格式:XXXX-XX-XX)" + 
                            Fore.CYAN + Style.BRIGHT +
                            "開始日期: " + 
                            Style.RESET_ALL)
    # 測試用
    # select_date_start = "2022-03-09"

    # 日期標準化
    select_date_start = b_data_clean_up.reformat_date(select_date_start)
    # 輸入異常
    if select_date_start == np.nan:
        print(Fore.RED + Style.BRIGHT + "輸入異常" + Style.RESET_ALL)
        continue
    # 將日期格式成 datetime 格式
    break

# 結束日期
while True:
    select_date_end = input(Fore.YELLOW + 
                            "請輸入要調取的日期區間(格式:XXXX-XX-XX)" + 
                            Fore.CYAN + Style.BRIGHT +
                            "結束日期: " + 
                            Style.RESET_ALL)
    # 測試用
    # select_date_end = "2023-04-05"

    # 日期標準化
    select_date_end = b_data_clean_up.reformat_date(select_date_end)
    # 輸入異常(包含日期順序錯誤)
    if select_date_end == np.nan or select_date_start > select_date_end:
        print(Fore.RED + Style.BRIGHT + "輸入異常" + Style.RESET_ALL)
        continue
    # 將日期格式成 datetime 格式，不做在上面的 while 是因為讓 false 先判斷排除
    select_date_start = datetime.datetime.strptime(select_date_start, "%Y-%m-%d")
    select_date_end = datetime.datetime.strptime(select_date_end, "%Y-%m-%d")
    break



# 選擇要調取資料的種類與方式
while True:
    select_which_data = input(Fore.YELLOW + 
                            "請輸入您想顯示的分類方式: \n" +
                            "name (不分類，且個別輸出)請輸入 0\n" +
                            "main category 請輸入 1\n" +
                            "sub category 請輸入 2\n" +
                            "tag 請輸入 3\n" +
                            "date 請輸入 4\n" +
                            "結束程序 請輸入 5\n" +
                            Fore.CYAN + Style.BRIGHT +"請輸入您的選擇: " +
                            Style.RESET_ALL)
    # 測試用
    # select_which_data = "1"
    # 選擇想要比較的資料
    # 異常輸入
    if select_which_data not in items_dict and select_which_data != "5":
        print(Fore.RED + Style.BRIGHT + "輸入異常" + Style.RESET_ALL)
        continue
    # 結束程式
    elif select_which_data == "5":
        sys.exit(Fore.GREEN + "程式結束" + Style.RESET_ALL)
    # 選擇需要的項目(選擇下一步驟)
    else:
        select_show_data_mode = input(Fore.YELLOW + "圖表顯示請輸入 0\n顯示於本程式內請輸入 1\n" + Fore.CYAN + Style.BRIGHT + "請輸入您的選擇(會依總金額排序): " + Style.RESET_ALL)
        # 測試用
        # select_show_data_mode = "0"
    # 變數名稱太長，多用一個變數
    curr_choice = items_dict[select_which_data]
    curr_header = header_dict[select_which_data]

    # 統計資料生成
    data_for_opt = b_data_clean_up.data_sum(data, curr_choice, select_date_start, select_date_end)

    # 針對想要的模式輸出
    # 異常輸入
    if select_show_data_mode != "0" and select_show_data_mode != "1":
        print(Fore.RED + Style.BRIGHT + "輸入異常" + Style.RESET_ALL)
    # 程式內輸出
    elif select_show_data_mode == "1":
        # 處理 index 並輸出
        print( data_for_opt.reset_index(drop=True) )
    # 呼叫副程式 opt_to_chart 將指定的 data(data_for_opt) 轉成 Pie
    else:
        c_opt_to_chart.pie_base( data_for_opt.to_numpy(), curr_header )
        print(Fore.GREEN + "完成" + Style.RESET_ALL)