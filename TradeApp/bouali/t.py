import os 

path1 = os.getcwd()
path2 = os.path.join(path1, 'data')
isExist = os.path.exists(path2)
if isExist == True:
    print(path2)
