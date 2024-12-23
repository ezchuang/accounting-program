"""
OOP測試
"""
import re
import pandas as pd
import numpy as np
import sys
import os
import textcolor
import datetime
import opt_to_chart

class General:
    # 日期格式化
    def reformat_date(date_str: str) -> str:
        # 本來就是空值
        if pd.isnull(date_str):
            return None
        # 建立 正規表達式 的 pattern，並套用
        patt_for_date = re.compile(r"[\/\.\-\,]")
        date_parts = re.split(patt_for_date, date_str)
        
        # 針對這種樣式的切版 -> 20230608
        if len(date_parts) == 1:
            # 數值異常，數字太少或太多
            if len(date_parts[0]) != 8:
                return None
            # 數值正常，切版
            else:
                date_parts = [date_parts[0][:4], date_parts[0][4:6], date_parts[0][6:]]

        # 數值超出正常範圍
        if not int(date_parts[0]) >= 0 or \
            not 0 <= int(date_parts[1]) <= 12 or \
            not 0 <= int(date_parts[2]) <= 31:
            return None
        elif int(date_parts[1]) in [2,4,6,9,11] and int(date_parts[2]) > 30:
            return None

        return "-".join(date_parts) # 2023/06/08
    
    
    # 副檔名檢查
    def file_name_check(name):
        if ".csv" not in name:
            name += ".csv"
        return name

    # 檔案是否存在
    def file_exist(name):
        return os.path.isfile(name)



class FileCmd:
    def __init__(self, cmd_dict, mode):
        self.cmd_dict = cmd_dict
        self.mode = mode

    @classmethod
    def creat_obj(cls, cmd_dict, mode):
        while True:
            try:
                valid_mode_selection = cls.validate_mode(cmd_dict, mode)
                break
            except ValueError:
                print(textcolor.Color.warning("模式選擇異常"))
                mode = input(textcolor.Color.mode_select("請重新選擇模式: "))
        return cls(cmd_dict, valid_mode_selection)
    
    @staticmethod
    def validate_mode(cmd_dict, mode):
        if mode not in cmd_dict:
            raise ValueError()
        return mode


class InputFileCmd(FileCmd):
    # csv批次輸入資料
    def ipt_csv(self) -> pd.DataFrame:
        path_ipt = input(textcolor.Color.mode_select("請輸入csv檔案名稱: "))
        # 副檔名確認
        path_ipt = General.file_name_check(path_ipt)
        # 檔名搜不到檔案
        if not General.file_exist(path_ipt):
            sys.exit(textcolor.Color.warning("無此檔案，本程式自動結束"))
        # csv 資料整理
        data = pd.read_csv(path_ipt)
        return data
    
    # 個別輸入資料
    def ipt_sep(self) -> pd.DataFrame:
        data_input={
            "name" : [],
            "main_ctgr" : [],
            "sub_ctgr" : [],
            "tag" : [],
            "desc" : [],
            "amount" : [],
            "date" : [],
        }
        # 限制選擇模式
        cmd_dict_ipt_sep = {"0", "1"}
        # 初始條件
        con_ipt = "0"
        first_round = 1

        while con_ipt == "0":
            # 第一輪不執行，詢問是否繼續
            if first_round != 1:
                con_ipt = input(textcolor.Color.mode_select("是否要繼續輸入資料(是:0, 否:1): "))
            else:
                first_round = 0
            # 模式檢查
            if con_ipt not in cmd_dict_ipt_sep:
                print(textcolor.Color.warning("輸入異常"))
                continue
            elif con_ipt == "1":
                break
            # 逐項詢問輸入
            for item in data_input.keys():
                data_input[item].append(input(textcolor.Color.mode_select(f"請輸入 {item}: ")))
        # 完成後轉成 DataFrame
        data = pd.DataFrame(data_input)
        return data

        

class OutputFileCmd(FileCmd):
    # 建立新檔案
    def opt_new(self, data: pd.DataFrame) -> str:
        # 輸入檔名
        path_opt_new = input(textcolor.Color.mode_select("請輸入欲新增的檔案名稱: "))
        # 確認副檔名
        path_opt_new = General.file_name_check(path_opt_new)
        # 輸出成檔案
        data.to_csv(path_opt_new , index = False)
        # 列印完成資訊
        print(textcolor.Color.finished_msg("完成"))
        print(textcolor.Color.mode_select(f"新帳務檔案檔名為: {path_opt_new}"))
        return path_opt_new

    # 修改舊檔案
    def opt_rev(self, data: pd.DataFrame) -> str:
        # 輸入檔名
        path_be_modify = input(textcolor.Color.mode_select("請輸入欲修改的檔案: "))
        # 確認副檔名
        path_be_modify = General.file_name_check(path_be_modify)
        # 檔案不存在(因不須再詢問一次，所以不使用 .opt_new 執行)
        if not General.file_exist(path_be_modify):
            print(textcolor.Color.warning("檔案不存在，自動新建"))
            data.to_csv(path_be_modify , index = False)
            # 列印完成資訊
            print(textcolor.Color.finished_msg("完成"))
            print(textcolor.Color.mode_select(f"新帳務檔案檔名為: {path_be_modify}"))
        # 載入舊檔案
        data_old = pd.read_csv(path_be_modify)
        # 合併舊資料和新資料
        merged_data = pd.concat( [data_old, data] )
        # 排序
        merged_data.sort_values(by = ['date'], inplace = True)
        # 寫回檔案
        merged_data.to_csv(path_be_modify, index = False)
        # 列印完成資訊
        print(textcolor.Color.finished_msg("完成"))
        print(textcolor.Color.finished_res(f"合併後檔案檔名為: {path_be_modify}"))
        return path_be_modify
    
    def blank_opt(self, data: pd.DataFrame) -> None:
        return None


class Show_data(FileCmd):
    def __init__(self, cmd_dict, mode):
        self.cmd_dict = cmd_dict
        self.mode = mode
        self.start = None
        self.end = None
        self.data = None
        self.data_for_show = None # 選定的 data item key
        self.show_mode = None # 顯示模式
        self.data_select = None

    def whether_show(self, whether_show_mode):
        # 不調取資料，直接結束程式
        if whether_show_mode == "1":
            sys.exit(textcolor.Color.finished_msg("程式結束"))

    def time_input(self, msg):
        while True:
            print(textcolor.Color.depiction("請輸入要調取的日期區間(格式:XXXX-XX-XX)"))
            select_date = input(textcolor.Color.mode_select(msg))
            # 日期標準化
            select_date = General.reformat_date(select_date)
            # 輸入異常
            if select_date == np.nan:
                print(textcolor.Color.warning("輸入值異常"))
                continue
            break
        return select_date
    
    def time_check(self, start, end):
        if start > end:
            print(textcolor.Color.warning("開始日期大於結束日期"))
            return False
        return True
        
    def time_format(self, start, end):
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
        end = datetime.datetime.strptime(end, "%Y-%m-%d")
        return start, end
    
    def time_bound(self):
        # 選擇日期區間與驗證
        while True:
            self.start = self.time_input("開始日期: ")
            self.end = self.time_input("結束日期: ")
            # 檢查日期是否輸入異常
            if not self.time_check(self.start, self.end):
                continue
            # 將日期格式成 datetime 格式
            self.start, self.end = self.time_format(self.start, self.end)
            break
    
    # 統計 items 重複之處並統計(將 item 相同的 amount 相加)，回傳統計資料
    def filter_data(self):
        num, date = "amount", "date"
        # 移除 na
        # 若選定日期排序需另外處裡
        if self.data_select == date:
            data_filtered = self.data[[num, date]].dropna(inplace = False)
        else:
            data_filtered = self.data[[self.data_select, num, date]].dropna(inplace = False)
        # 日期格式轉換
        data_filtered[date] = pd.to_datetime(data_filtered[date])
        # 篩選日期 [中間為邏輯判斷]
        data_filtered = data_filtered[(data_filtered[date] >= self.start) & (data_filtered[date] <= self.end)]
        # 選出指定col
        data_filtered = data_filtered[ [self.data_select, num] ]
        # 若指定之 col 為 name 則不執行統計(加總)
        if self.data_select == "name":
            data_merged = data_filtered
        # 非 name 進行加總
        else:
            data_merged = data_filtered.groupby(data_filtered[self.data_select]) \
            .agg({self.data_select: 'first', num: 'sum'})
        # 依(總)金額排序
        data_merged.sort_values(by = [num], inplace = True, ascending = False)
        # 此時 index 項目會跟 item 內容一樣，重置index
        data_merged.reset_index(drop=True)
        self.data_for_show = data_merged

    # 呼叫副程式 opt_to_chart 將指定的 data(data_for_show) 轉成 Pie
    def data_chart(self):
        curr_header = self.data_select.capitalize()
        opt_to_chart.pie_base(self.data_for_show.to_numpy(), curr_header)
        print(textcolor.Color.finished_msg("完成"))

    # 程式內輸出
    def data_show_directly(self):
        print(self.data_for_show.reset_index(drop=True) )