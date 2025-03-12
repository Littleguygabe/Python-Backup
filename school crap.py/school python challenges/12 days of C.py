with open("lyrics.txt", mode = "r", encoding="utf-8") as file: lyrics = file.readlines() 
for i in range(0,len(lyrics)): print(lyrics[i])