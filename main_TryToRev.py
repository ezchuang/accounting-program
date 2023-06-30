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
import os

# 自訂義模組
import opt_to_chart
import function_TryToRev
import textcolor
import cmd_db


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
print(
    textcolor.Color.depiction(
        "請填妥您需要使用的資料，填入資料若有空值，會在輸出時將其排除(僅僅排除該筆)\n" +
        "例如: name有填，tag沒填，amount有填\n      呼叫 name 時該筆資料會納入統計\n      但呼叫 tag 時該筆資料不會納入統計\n") +
    textcolor.Color.high_light(
        "盡量確保 name、main_ctgr、amount、date 有填妥\n" +
        "date 填入數值錯誤會被更改成空值")
    )


class Main_routine:
    def __init__(self):
        self.cmd_dict = None
        self.select_ipt_mode = None
        self.ipt_data_obj = None
        self.select_opt_mode = None
        self.opt_data_obj = None
        self.path_opt = None
        self.data = None
        self.show_data_obj = None

    def run(self):
        self.select_input_mode()
        self.load_data()
        self.format_date()
        self.select_output_mode()
        self.save_data()
        self.data_pretreatment()
        self.whether_show_data()
        self.show_data()
    
    # 選擇輸入模式
    def select_input_mode(self):
        # 調取該模式"顯示"用的 cmd_dict
        self.cmd_dict = cmd_db.ipt_msg()
        # 輸入 選項選擇
        for msg in self.cmd_dict:
            print(textcolor.Color.depiction(f"{self.cmd_dict[msg]}"))
        self.select_ipt_mode = input(textcolor.Color.mode_select("請選擇 輸入 模式: "))

    # 輸入資料
    def load_data(self):
        # 建立obj
        self.ipt_data_obj = function_TryToRev.InputFileCmd.creat_obj(self.cmd_dict, self.select_ipt_mode)
        # 調取該模式"執行"用的 cmd_dict
        self.ipt_data_obj.cmd_dict = cmd_db.ipt_run(self.ipt_data_obj)
        # load in 資料
        self.data = self.ipt_data_obj.cmd_dict[self.select_ipt_mode]()
        # 這邊的 ipt_data_obj.cmd_dict 結束任務
    
    # 日期格式化 與 排序
    def format_date(self):
        # 整理 date 格式
        self.data["date"] = self.data["date"].apply(function_TryToRev.General.reformat_date)
        # 依日期排序
        self.data.sort_values(by=['date'], inplace = True)


    # 選擇輸出模式
    def select_output_mode(self):
        # 調取該模式"顯示"用的 cmd_dict
        self.cmd_dict = cmd_db.opt_msg(self.select_ipt_mode)
        # 輸入 選項選擇
        for msg in self.cmd_dict:
            print(textcolor.Color.depiction(f"{self.cmd_dict[msg]}"))
        self.select_opt_mode = input(textcolor.Color.mode_select("請選擇 輸出 模式: "))
    
    # 資料整併與存檔
    def save_data(self):
        # 建立obj
        self.opt_data_obj = function_TryToRev.InputFileCmd.creat_obj(self.cmd_dict, self.select_ipt_mode)
        # 調取該模式"執行"用的 cmd_dict
        self.opt_data_obj.cmd_dict = cmd_db.ipt_run(self.ipt_data_obj, self.select_ipt_mode)
        # save 資料
        self.path_opt = self.ipt_data_obj.cmd_dict[self.select_opt_mode]()


        # 測試用
        print(self.data)
        print(self.ipt_data_obj.cmd_dict)

    # 可調取的資料僅限此次輸入資料
    def data_pretreatment(self):
        # 個別輸入的空值仍會撈到，重 Load 一次資料
        if self.select_ipt_mode == "0":
            pass
        else:
            self.data = pd.read_csv(self.path_opt)

    # 是否調取資料選擇
    def whether_show_data(self):
        if self.select_opt_mode == "2":
            whether_show_mode = "0"
        else:
            # 詢問是否調取資料
            self.cmd_dict = cmd_db.show_data_mode_msg()
            # 選項選擇
            for msg in self.cmd_dict:
                print(textcolor.Color.depiction(f"{self.cmd_dict[msg]}"))
            whether_show_mode = input(textcolor.Color.mode_select("請選擇 是否需要調取資料: "))
        self.show_data_obj = function_TryToRev.Show_data.creat_obj(self.cmd_dict, whether_show_mode)
        # 是否結束程式
        self.show_data_obj.whether_show(whether_show_mode)

    def show_data(self):
        self.show_data_obj.cmd_dict = cmd_db.show_data_select_msg()
        print(textcolor.Color.depiction("請輸入您想顯示的分類方式: "))
        for msg in self.show_data_obj.cmd_dict:
            print(textcolor.Color.depiction(f"{self.show_data_obj.cmd_dict[msg]}"))
        # 輸入 選項選擇
        data_select = input(textcolor.Color.mode_select("請輸入選擇呈現的資訊: "))
        self.show_data_obj.show_data_main(data_select)


if __name__ == "__main__":
    main_function = Main_routine()
    main_function.run()