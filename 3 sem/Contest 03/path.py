import os

def checkdir(way):
    files = 0
    dirs = 1
    Ins = os.listdir(path = way)
    for i in Ins:
        if os.path.isfile(way + "/" + i) == True: files += 1
        elif os.path.isdir(way + "/" + i) == True:
            dfiles, ddirs = checkdir(way + "/" + i)
            files, dirs = files + dfiles, dirs + ddirs
    return files, dirs

way = input()
files = 0
dirs = 0
#print(os.getcwd())
if os.path.exists(way):
    if os.path.isfile(way): files += 1
    else:
        files, dirs = checkdir(way)
print("Files:", files)
print("Dirs:", dirs)
