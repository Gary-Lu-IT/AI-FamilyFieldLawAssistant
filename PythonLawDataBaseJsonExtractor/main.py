from datetime import datetime
from pymongo import MongoClient
import json,os,sys,zipfile
# 法規內容變數
JsonLawContent=None
Today=datetime.now().strftime("%Y%m%d")
file='chlaw.json.zip'
with zipfile.ZipFile(file, 'r') as zf:
    for name in zf.namelist():
        if(name.endswith('.json')):
            print(name)
            # 解壓縮出JSON
            zf.extract(name)
            # 讀解壓縮
            with open(name, 'r', encoding='utf-8') as f:
                    JsonLawContent = f.read()
            # JSON檔資料夾路徑要存在
            if(not os.path.exists("./ChlawBackup")):
                os.makedirs("./ChlawBackup")
            # 依據日期備份
            with open(f"./ChlawBackup/{name}.{Today}.json", 'w',encoding="utf-8") as f:
                f.write(JsonLawContent)
if(not(JsonLawContent is None)):
    # 連接到MongoDB資料庫
    LawDB=MongoClient("localhost", 27017)
    collection=LawDB["sakuramoriakane_111p"]["law_collection"]
    # JSON內容去除換行符號和BOM
    JsonLawContent = JsonLawContent.replace("\n", "").replace("\ufeff", "")
    LawDict=json.loads(JsonLawContent)
    # 取出JSON內容
    Laws= LawDict["Laws"]
    # 未處理法規數量所占記憶體大小
    UnprocessedLawsSize=sys.getsizeof(Laws)
    while(len(Laws)>0):
        # 取出第一筆法規
        Law=Laws.pop(0)
        # 法規名稱
        LawName=Law["LawName"]
        # 修改日期
        LawModifiedDate=Law["LawModifiedDate"]
        ExistLaw=collection.find_one(
             {"LawName": LawName, "LawModifiedDate": LawModifiedDate}
        )
        if(not(ExistLaw is None)):
            # 如果已經存在則跳過
            print(f"法規 {LawName} 已存在，跳過處理。")
            continue
        # 儲存到MongoDB資料庫
        collection.insert_one(Law)
        #剩餘未處理資料量
        RemainingLawsSize=sys.getsizeof(Laws)
        print(f"處理進度：{(UnprocessedLawsSize - RemainingLawsSize) / UnprocessedLawsSize * 100:.2f}%")
    LawDB.close()
    print("所有法規已成功儲存到MongoDB資料庫。")