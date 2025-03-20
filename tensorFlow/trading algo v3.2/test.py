maxfileSize = 50
fileSizeMB = 130

fileCount = 1
while fileSizeMB>maxfileSize:
    fileSizeMB/=2
    fileCount*=2


print(fileCount)