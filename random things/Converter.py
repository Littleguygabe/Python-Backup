import time
time.sleep(1)
print ("Welcome to the converter")
print ("What would you like to convert to:")

print ("1) Binary to denary")
print ("2) Denary to binary")
print ("3) Binary to Hex")
print ("4) Hex to Binary")
print ("5) Hex to Denary")
print ("6) Denary to Hex")
choice = int(input ("Please input a corresponding number: "))

if choice == 1:
    x = 1
    while x == 1:
        Denary_Binary = 0
        Binary = str(input ("Please input a 8 digit Binary code: "))
        if len(Binary) == 8:
            print ("Code corrrect length")
            x = 2
        else:
            print ("Code not correct length")
            x = 1
        if Binary[0] == "1":
            Denary_Binary = Denary_Binary + 128
        if Binary[1] == "1":
            Denary_Binary = Denary_Binary + 64
        if Binary[2] == "1":
            Denary_Binary = Denary_Binary + 32
        if Binary[3] == "1":
            Denary_Binary = Denary_Binary + 16
        if Binary[4] == "1":
            Denary_Binary = Denary_Binary + 8
        if Binary[5] == "1":
            Denary_Binary = Denary_Binary + 4
        if Binary[6] == "1":
            Denary_Binary = Denary_Binary + 2
        if Binary[7] == "1":
            Denary_Binary = Denary_Binary + 1
        print ("Your denary total is: ", Denary_Binary)

if choice == 2:
    Denary_Binary = ""
    Denary_Binary = str(Denary_Binary)
    x = 1
    while x == 1:
        Denary = int(input ("Please input a number bellow 255: "))
        if Denary <= 255:
            print ("Correct length")
            x = 2
        else:
            print ("Please re_input")
            x = 1

        if Denary >= 128:
            Denary_Binary = Denary_Binary + "1"
            Denary = Denary - 128
        else:
            Denary_Binary = Denary_Binary + "0"

            
        
        if Denary >= 64:
            Denary_Binary = Denary_Binary + "1"
            Denary = Denary - 64
        else:
            Denary_Binary = Denary_Binary + "0"

            
            
        if Denary >= 32:
            Denary_Binary = Denary_Binary + "1"
            Denary = Denary - 32
        else:
            Denary_Binary = Denary_Binary + "0"

            
        
        if Denary >= 16:
            Denary_Binary = Denary_Binary + "1"
            Denary = Denary - 16
        else:
            Denary_Binary = Denary_Binary + "0"

            

        if Denary >= 8:
            Denary_Binary = Denary_Binary + "1"
            Denary = Denary - 8
        else:
            Denary_Binary = Denary_Binary + "0"


        if Denary >= 4:
            Denary_Binary = Denary_Binary + "1"
            Denary = Denary - 4
        else:
            Denary_Binary = Denary_Binary + "0"
        
        if Denary >= 2:
            Denary_Binary = Denary_Binary + "1"
            Denary = Denary - 2
        else:
            Denary_Binary = Denary_Binary + "0"

            
        
        if Denary >= 1:
            Denary_Binary = Denary_Binary + "1"
            Denary = Denary - 1
        else:
            Denary_Binary = Denary_Binary + "0"

        print ("Your Binary code is: ", Denary_Binary)
    
    

if choice == 3:
    x = 1
    while x == 1:
        Denary_hex1 = 0
        Denary_hex2 = 0
        Denary_hex = ""
        Binary = str(input ("Please input a 8 digit Binary code: "))
        if len(Binary) == 8:
            print ("Code corrrect length")
            x = 2
        else:
            print ("Code not correct length")
            x = 1
        if Binary[0] == "1":
            Denary_hex1 = Denary_hex1 + 8
        if Binary[1] == "1":
            Denary_hex1 = Denary_hex1 + 4
        if Binary[2] == "1":
            Denary_hex1 = Denary_hex1 + 2
        if Binary[3] == "1":
            Denary_hex1 = Denary_hex1 + 1            
        if Binary[4] == "1":
            Denary_hex2 = Denary_hex2 + 8
        if Binary[5] == "1":
            Denary_hex2 = Denary_hex2 + 4
        if Binary[6] == "1":
            Denary_hex2 = Denary_hex2 + 2
        if Binary[7] == "1":
            Denary_hex2 = Denary_hex2 + 1

        if Denary_hex1 == 15:
            Denary_hex = Denary_hex + "F"
        if Denary_hex1 == 14:
            Denary_hex = Denary_hex + "E"
        if Denary_hex1 == 13:
            Denary_hex = Denary_hex + "D"
        if Denary_hex1 == 12:
            Denary_hex = Denary_hex + "C"
        if Denary_hex1 == 11:
            Denary_hex = Denary_hex + "B"
        if Denary_hex1 == 10:
            Denary_hex = Denary_hex + "A"
        if Denary_hex1 == 9:
            Denary_hex = Denary_hex + "9"
        if Denary_hex1 == 8:
            Denary_hex = Denary_hex + "8"
        if Denary_hex1 == 7:
            Denary_hex = Denary_hex + "7"
        if Denary_hex1 == 6:
            Denary_hex = Denary_hex + "6"
        if Denary_hex1 == 5:
            Denary_hex = Denary_hex + "5"
        if Denary_hex1 == 13:
            Denary_hex = Denary_hex + "4"
            
        print ("Your hex code is: ", Denary_hex)
