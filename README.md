# accounting
 
title: 

    accounting program

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

instructions:

    1. 本程式以問答式選取所需功能，所有 固定選項問答 皆有將選項附上(包含說明與警示)
        1.1 所有問答皆有做異常排除的邏輯 (若有發現新的未排除異常，我會再做修正)
    2. 資料輸入的部分:
        2.1 date 請使用西元紀年
            2.1.1 輸入不拘形式 20230609、2023/06/09、2023-06-09...，但不能輸入2023609
            2.1.2 異常輸入 會被修正成空值(會無法輸出到圖表資訊)
        2.2 amount拜託不要輸入數字以外的東西(這是記帳的核心，要是輸入數字以外的東西會跳 error)
        2.3 除了上述兩者，其他資訊都是用 str 比對，維持 " 記帳應該是件自由的事 " 這個特性
        2.4 本程式只要選用的分類裡面有空值，該資料皆無法輸出到圖表資訊，因為本程式始有的輸出模組無法處理 NaN
    3. 功能:
        3.1
