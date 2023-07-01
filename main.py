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
import function
import textcolor
import cmd_db


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
        self.cmd_dict = None # 變動，for 文字說明書出 & obj建立
        self.select_ipt_mode = None # 輸入模式選擇
        self.ipt_data_obj = None # 輸入 data 的 obj
        self.data = None # 輸入的 data
        self.select_opt_mode = None # 存檔模式選擇
        self.opt_data_obj = None # data 存檔的 obj
        self.path_opt = None # 存檔檔案路徑/名稱
        self.show_data_mode = None # 資料顯示模式
        self.show_data_obj = None # 顯示 data 的 obj
        self.show_data_selected = None # 選定要呈現的 data item
        self.show_data_selected_obj = None # 顯示 data 的 item 的 obj
        self.show_data_mode_obj = None # 顯示 data 的模式的 obj
        self.data_for_show = None # 整理完待輸出的 data

    def run(self):
        self.select_input_mode()
        self.load_data()
        self.format_date()
        self.select_output_mode()
        self.save_data()
        self.data_pretreatment()
        self.whether_show_data()
        self.select_time_bound()
        while self.show_data_selected != "5":
            self.select_show_data()
            self.select_data_mode()
            self.filter_show_data()
            self.show_data()
            continue
        
    
    # 選擇輸入模式 & 建立obj
    def select_input_mode(self):
        # 調取該模式"顯示"用的 cmd_dict
        self.cmd_dict = cmd_db.ipt_msg()
        # 輸入 選項選擇
        for msg in self.cmd_dict:
            print(textcolor.Color.depiction(f"{self.cmd_dict[msg]}"))
        self.select_ipt_mode = input(textcolor.Color.mode_select("請選擇 輸入 模式: "))
        # 建立obj
        self.ipt_data_obj = function.InputFileCmd.creat_obj(self.cmd_dict, self.select_ipt_mode)


    # 輸入資料
    def load_data(self):
        # 調取該模式"執行"用的 cmd_dict
        self.ipt_data_obj.cmd_dict = cmd_db.ipt_run(self.ipt_data_obj)
        # load in 資料
        self.data = self.ipt_data_obj.cmd_dict[self.select_ipt_mode]()
        # 這邊的 ipt_data_obj.cmd_dict 結束任務
    

    # 日期格式化 與 排序
    def format_date(self):
        # 整理 date 格式
        self.data["date"] = self.data["date"].apply(function.General.reformat_date)
        # 依日期排序
        self.data.sort_values(by=['date'], inplace = True)


    # 選擇存檔模式 & 建立obj
    def select_output_mode(self):
        # 調取該模式"顯示"用的 cmd_dict
        self.cmd_dict = cmd_db.opt_msg(self.select_ipt_mode)
        # 輸入 選項選擇
        for msg in self.cmd_dict:
            print(textcolor.Color.depiction(f"{self.cmd_dict[msg]}"))
        self.select_opt_mode = input(textcolor.Color.mode_select("請選擇 輸出 模式: "))
        # 建立obj
        self.opt_data_obj = function.OutputFileCmd.creat_obj(self.cmd_dict, self.select_ipt_mode)
    

    # 資料整併與存檔
    def save_data(self):
        # 調取該模式"執行"用的 cmd_dict
        self.opt_data_obj.cmd_dict = cmd_db.opt_run(self.opt_data_obj, self.select_ipt_mode)
        # save 資料
        self.path_opt = self.opt_data_obj.cmd_dict[self.select_opt_mode](self.data)


        # 測試用
        # print(self.data)
        # print(self.ipt_data_obj.cmd_dict)


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
            self.cmd_dict = cmd_db.weather_show_data_msg()
            # 選項選擇
            print(textcolor.Color.depiction("是否需要調取資料: "))
            for msg in self.cmd_dict:
                print(textcolor.Color.depiction(f"{self.cmd_dict[msg]}"))
            whether_show_mode = input(textcolor.Color.mode_select("請選擇: "))
        self.show_data_obj = function.Show_data.creat_obj(self.cmd_dict, whether_show_mode)
        # 是否結束程式
        self.show_data_obj.whether_show(whether_show_mode)
        self.show_data_obj.data = self.data


    # 選擇日期區間與驗證
    def select_time_bound(self):
        self.show_data_obj.time_bound()


    # 選擇顯示的資料
    def select_show_data(self):
        self.cmd_dict = cmd_db.show_data_select_msg()
        print(textcolor.Color.depiction("依據顯示的分類方式選擇以下選項: "))
        # 選擇輸出種類
        for msg in self.cmd_dict:
            print(textcolor.Color.depiction(f"{self.cmd_dict[msg]}"))
        self.show_data_selected = input(textcolor.Color.mode_select("請輸入選擇想呈現的資訊: "))
        if self.show_data_selected == "5":
            sys.exit(textcolor.Color.finished_msg("程式結束"))
        self.show_data_selected_obj = function.FileCmd.creat_obj(self.cmd_dict, self.show_data_selected)


    # 選擇選定資料的顯示方式
    def select_data_mode(self):
        self.cmd_dict = cmd_db.show_data_mode_msg()
        # 選擇輸出種類
        for msg in cmd_db.show_data_mode_msg():
            print(textcolor.Color.depiction(f"{self.cmd_dict[msg]}"))
        self.show_data_mode = input(textcolor.Color.mode_select("請輸入您的選擇(會依總金額排序): "))
        self.show_data_mode_obj = function.FileCmd.creat_obj(self.cmd_dict, self.show_data_mode)


    # 整理顯示資料
    def filter_show_data(self):
        self.show_data_selected_obj.cmd_dict = cmd_db.show_data_select()
        self.show_data_mode_obj.cmd_dict = cmd_db.show_data_run(self.show_data_obj)

        self.show_data_obj.data_select = self.show_data_selected_obj.cmd_dict[self.show_data_selected_obj.mode]
        # 統計資料生成
        self.data_for_show = self.show_data_obj.filter_data()
        

    # 顯示資料
    def show_data(self):
        self.show_data_mode_obj.cmd_dict[self.show_data_mode]()




if __name__ == "__main__":
    main_function = Main_routine()
    main_function.run()