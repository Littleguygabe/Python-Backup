import linecache;
print('1) add a record')
print('2) view a record')
print('3) delete a record')
choice = int(input('choose 1 or 2 or 3'))
recodNo = []
firstnameArray = []
surnameArray = []

if choice == 1:
    recordnum = input('enter a record number')
    while len(recordnum)<3:
        recordnum = recordnum + ' '
        
    firstname = input('enter a firstname ')
    while len(firstname)<10:
        firstname = firstname + ' '
        
    surname = input('enter a surname ')
    while len(surname)<10:
        surname = surname + ' '
        
    mark = input('enter a mark')
    while len(mark)<3:
        mark = mark + ' '
        
    file = open('7.5 scores.txt','a')
    file.write(recordnum)
    file.write('\n')
    file.write(firstname)
    file.write('\n')
    file.write(surname)
    file.write('\n')
    file.write(mark)
    file.write('\n')
    
    print('done')

elif choice ==2:
    viewnum = int(input('what record would you like to see? '))
    
    file = open('7.5 scores.txt','r')
    file.seek(((viewnum-1)*32),0)
    
    playNo = file.read(4)
    firstname = file.read(11)
    surname = file.read(11)
    mark = file.read(4)
    
    print('Player No: ', playNo)
    print('Player firstname: ', firstname)
    print('Player surname: ', surname)
    print('player mark: ',mark)
    
elif choice == 3:
    deletenum = input('enter a record to delete')
    
    lines = open('7.5 scores.txt').readlines()
    indexvallower = int(deletenum)*2
    indexvalupper = int(deletenum)*4
    open('newfile.txt','w').writelines(lines[0:indexvallower-1])
    open('newfile.txt','a').writelines(lines[indexvalupper:-1])
    
    undeleted = open('newfile.txt').readlines()
    
    open('7.5 scores.txt','w').writelines(undeleted[0:-1])


