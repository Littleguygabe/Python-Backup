print('1) Enter username and password ')
print('2) Change username and password')
choice = int(input('choose an option (1 or 2) '))
username_Array = []
encrypted_password = []
encrypted_old_password = []

def password_change(new_password, name, password):
    with open("usernames.txt", mode = "r", encoding="utf-8") as file:
        names = file.read().splitlines()
    for name2append in names:
        username_Array.append(name2append)
    file.close()
    
    #encrypt inputted old password
    for i in range(0,len(password)):
        password_unicode_character = ord(password[i])
        encrypted_old_password.append(chr(password_unicode_character+1))
    
    password = ''.join(str(x) for x in encrypted_old_password)
    
    for i in range(0,len(username_Array)-1):
        if username_Array[i] == name:
            if username_Array[i+1] == password:
                file = open('usernames.txt','w')
                file.write('')
                file.close()
            
    for i in range (0,len(new_password)):
        unicode_character = ord(new_password[i])
        encrypted_password.append(chr(unicode_character+1))
    
    str_encrypted_password = ''.join(str(x) for x in encrypted_password)
    for k in range(0,len(username_Array)):
        if username_Array[k] == password:
            username_Array[k] = str_encrypted_password
        
    for i in range(0,len(username_Array)):
        file = open('usernames.txt','a')
        file.write(username_Array[i] + '\n')
        file.close()
        
    print('succesfully changed')

while choice == 1:
    name = input('what is your username ')
    password = input('what is your password ')
    for i in range(0,len(password)):
        password_unicode_character = ord(password[i])
        encrypted_old_password.append(chr(password_unicode_character+1))
    
    password = ''.join(str(x) for x in encrypted_old_password)
    
    file = open('usernames.txt','a')
    file.write(name)
    file.write('\n')
    file.write(password)
    break

while choice == 2:
    name = str(input('what is you username? '))
    password = str(input('what is your old password? '))
    new_password = input('what do you want your new password to be? ')
    password_change(new_password,name,password)
    break
