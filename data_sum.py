# 由 main 呼叫，統計 items 重複之處(將 item 相同的 amount 相加)，並回傳統計資料
def Data_sum(data, item_name, num):
    if item_name == "name":
        data_merged = data
        pass
    else:
        data_merged = data.groupby(data[item_name]).agg({item_name: 'first', num: 'sum'})
        # 此時 index 項目會跟 item 內容一樣
    data_merged.sort_values(by = ["amount"], inplace = True, ascending = False) # inplace，由大到小
    data_merged.reset_index(drop=True) # inplace，重置index

    return data_merged