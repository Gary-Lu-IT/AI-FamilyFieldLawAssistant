import zipfile
# �ɮצW��
file='chlaw.json.zip'
with zipfile.ZipFile(file, 'r') as zf:
    for name in zf.namelist():
        if(name.endswith('.json')):
            print(name)
            # �����Y�ɮ�
            zf.extract(name)
