import zipfile
# 檔案名稱
file='chlaw.json.zip'
with zipfile.ZipFile(file, 'r') as zf:
    for name in zf.namelist():
        if(name.endswith('.json')):
            print(name)
            # 解壓縮檔案
            zf.extract(name)
