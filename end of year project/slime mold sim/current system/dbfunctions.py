import sqlite3, random, string

def login(username,password):   
    con = sqlite3.connect('simData.db')
    cur = con.cursor()
    createTableCommand = '''CREATE TABLE IF NOT EXISTS loginInfo
                            (username STRING,password STRING, admin BOOLEAN)''' 
                            
    cur.execute(createTableCommand)  
    command = 'SELECT password FROM loginInfo WHERE username = ?'
    cur.execute(command, (username,))
    results = cur.fetchall()
    con.commit()
    if len(results)>0:       
        if results[0][0] == password:
            #check if Admin or not
            if admin(username,password) == 1:
                return 'admin'
            else:
                return True
        else:
            return False
            
    else:
        return False

def admin(username,password):
    con=sqlite3.connect('simData.db')
    cur=con.cursor()
    checkAdminCommand = 'SELECT admin FROM loginInfo WHERE username = ? AND password = ?'
    cur.execute(checkAdminCommand, (username, password,))
    results = cur.fetchall()
    con.commit()
    return results[0][0]

def createNewUser(username,password,adminOption):
    if adminOption == 1:
        adminEnabled = True
        
    else:
        adminEnabled = False   
    con=sqlite3.connect('simData.db')
    cur=con.cursor()
    insertNewUserCommand = 'INSERT INTO loginInfo VALUES(?, ?, ?)'
    cur.execute(insertNewUserCommand,(username, password, adminEnabled,))
    con.commit() 
    
def checkPassword(username,password):
    con=sqlite3.connect('simData.db')
    cur = con.cursor()
    checkPassCommand = 'SELECT password FROM loginInfo WHERE username = ?'
    cur.execute(checkPassCommand,(username,))
    results=cur.fetchall()
    con.commit()
    if len(results)>0:
        if results[0][0] == password:
            return True
        
        return False

    return False
    
def checkUsernameAlreadyExists(username):
    con=sqlite3.connect('simData.db')
    cur = con.cursor()
    checkUserExistsCommand = 'SELECT * FROM loginInfo WHERE username = ?'
    cur.execute(checkUserExistsCommand,(username,))
    results = cur.fetchall()
    
    if len(results)>0:
        return True

    return False
    
def checkUserExists(username):
    con = sqlite3.connect('simData.db')
    cur = con.cursor()
    checkExistsCommand = 'SELECT * FROM loginInfo WHERE username = ?'
    cur.execute(checkExistsCommand,(username,))
    results = cur.fetchall()
    con.commit()
    if len(results)>0:
        return True
    else:
        return False
    
def deleteUser(username):
    con=sqlite3.connect('simData.db')
    cur = con.cursor()
    deleteUserCommand = '''DELETE FROM loginInfo WHERE username = ?'''
    cur.execute(deleteUserCommand,(username,))
    
    deleteUserSettingsCommand = '''DELETE FROM settings WHERE settings.settingsKey = (SELECT settingsKey FROM userNameSettingsLink WHERE userNameSettingsLink.username = ?)'''
    cur.execute(deleteUserSettingsCommand,(username,))
    
    deleteUserLinkCommand = '''DELETE FROM userNameSettingsLink WHERE username = ?'''
    cur.execute(deleteUserLinkCommand,(username,))
    con.commit()
    
    con.commit()
    return True

def getAllTables():
    con=sqlite3.connect('simData.db')
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_schema WHERE type='table'")
    results = cur.fetchall()
    con.commit()
    temparr=[]
    for i in range(0,len(results)):
        temparr.append(results[i][0])
        
    return temparr

def retrieveTable(tableName):
    con=sqlite3.connect('simData.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM '+tableName)
    results = cur.fetchall()
    con.commit()
    return results
    
def retrieveColumnNames(tableName):
    con = sqlite3.connect('simData.db')
    cur = con.cursor()
    results=cur.execute('SELECT * FROM '+tableName)
    con.commit()
    temparr=[]
    for column in results.description:
        temparr.append(column[0])
    return temparr

def generateGameId(username):
    con = sqlite3.connect('simData.db')
    cur = con.cursor()
    createTableCommand = '''CREATE TABLE IF NOT EXISTS userNameSettingsLink
                    (username STRING,gameID INTEGER,settingsKey STRING)'''
    cur.execute(createTableCommand)
    
    findGIDCommand = '''SELECT MAX(gameID) FROM userNameSettingsLink WHERE username = ?'''
    cur.execute(findGIDCommand,(username,))
    results = cur.fetchall()
    con.commit()
    if results[0][0] == None:
       return 1
    else:
        return results[0][0]+1
    
def createSettingsId():
    letters = string.ascii_lowercase
    settingsKey = ( ''.join(random.choice(letters) for i in range(5)))

    con = sqlite3.connect('simData.db')
    cur = con.cursor()
    
    checkKeyCommand = '''SELECT * FROM userNameSettingsLink WHERE settingsKey = ?'''
    cur.execute(checkKeyCommand,(settingsKey,))
    results = cur.fetchall()
    while len(results)!=0:
        settingsKey = ( ''.join(random.choice(letters) for i in range(10)))
        cur.execute(checkKeyCommand,(settingsKey,))
        results = cur.fetchall()
        
    con.commit()
    return settingsKey

def createLinkRegister(username,gameID,settingsKey):
    con=sqlite3.connect('simData.db')
    cur = con.cursor()
    insertLinkDataCommand = '''INSERT INTO userNameSettingsLink VALUES(?,?,?)'''
    cur.execute(insertLinkDataCommand,(username,gameID,settingsKey))
    con.commit()

def enterParameters(settingsKey,curiosity,tLen,moveInt,viewDist,sr,disp):
    con = sqlite3.connect('simData.db')
    cur = con.cursor()
    createTableCommand = '''CREATE TABLE IF NOT EXISTS settings (
	"settingsKey"	STRING,
	"curiosityVal"	INTEGER,
	"tailLen"	INTEGER,
	"moveInterval"	INTEGER,
	"viewDistance"	INTEGER,
	"spawnRadius"	INTEGER,
	"Dispertion"	STRING,
	PRIMARY KEY("settingsKey"))'''

    cur.execute(createTableCommand)
    
    inputSettingCommand = '''INSERT INTO settings VALUES (?, ?, ?, ?, ?, ?, ?)'''
    cur.execute(inputSettingCommand,(settingsKey,curiosity,tLen,moveInt,viewDist,sr,disp,))
    con.commit()

def getSettings(username,gameID):
    con = sqlite3.connect('simData.db')
    cur = con.cursor()
    retrieveSettingsCommand = '''SELECT * FROM settings WHERE settingsKey = (SELECT settingsKey FROM userNameSettingsLink WHERE username = ? AND gameID = ?)'''
    cur.execute(retrieveSettingsCommand,(username,gameID,))
    results = cur.fetchall()
    con.commit()
    return results

def updateSettings(settingsKey,curiosity,tLen,moveInt,viewDist,sr,disp):
    con = sqlite3.connect('simData.db')
    cur = con.cursor()
    updateSettingsCommand = '''UPDATE settings SET
                                curiosityVal = ?,
                                tailLen = ?,
                                moveInterval = ?,
                                viewDistance = ?,
                                spawnRadius = ?,
                                Dispertion = ?
                                WHERE settingsKey = ?'''
                                
    cur.execute(updateSettingsCommand,(curiosity,
                               tLen,
                               moveInt,
                               viewDist,
                               sr,
                               disp,
                               settingsKey,))

    con.commit()
    
def checksaves(username):
    con = sqlite3.connect('simData.db')
    cur = con.cursor()
    checkSavesCommand = '''SELECT * FROM userNameSettingsLink WHERE username = ?'''
    cur.execute(checkSavesCommand,(username,))
    results = cur.fetchall()
    con.commit()
    if len(results) == 0:
        return False
    else:
        return True
    
def getKeydata(key):
    con=sqlite3.connect('simData.db')
    cur=con.cursor()
    getKeyDataCommand = '''SELECT username, gameID FROM userNameSettingsLink WHERE settingsKey = ?'''
    cur.execute(getKeyDataCommand,(key,))
    con.commit()
    results=cur.fetchall()
    return results
    
def deleteSettings(key):
    con=sqlite3.connect('simData.db')
    cur = con.cursor()
    deleteSettingsCommand = '''DELETE FROM settings WHERE settingsKey = ?'''
    cur.execute(deleteSettingsCommand,(key,))

    deleteUsernameLinkCommand = '''DELETE FROM userNameSettingsLink WHERE settingsKey = ?'''
    cur.execute(deleteUsernameLinkCommand,(key,))

    con.commit()

def saveSimSettings(settingsKey,nodePositions):
    con = sqlite3.connect('simData.db')
    cur = con.cursor()
    #ensure table exists
    createTableCommand = '''CREATE TABLE IF NOT EXISTS posData (
        "settingsKey" STRING,
        "nodeX" INTEGER,
        "nodeY" INTEGER)'''
        
    cur.execute(createTableCommand)
    
    #delete Old data
    deleteDataCommand = '''DELETE FROM posData WHERE settingsKey = ?'''
    cur.execute(deleteDataCommand,(settingsKey,))
    
    #add in new node data
    inputDataCommand = '''INSERT INTO posData VALUES (?, ?, ?)'''
        
    for i in range(0,len(nodePositions),2):
        cur.execute(inputDataCommand,(settingsKey,nodePositions[i],nodePositions[i+1]))
    con.commit()
    
def retrieveSimSettings(settingsKey):
    con=sqlite3.connect('simData.db')
    cur = con.cursor()
    
    retrieveDataCommand = '''SELECT nodeX,nodeY FROM posData WHERE settingsKey = ?'''
    cur.execute(retrieveDataCommand,(settingsKey,))
    results=cur.fetchall()
    con.commit()
    
    #convert from 2d to 1d list
    temparr = []
    for x,y in results:
        temparr.append(x)
        temparr.append(y)
    
    return temparr

def retrieveUserSaves(username):

    con = sqlite3.connect('simData.db')
    cur = con.cursor()

    retrieveSavesCommand = '''SELECT DISTINCT
                                usernameSettingsLink.gameID,
                                settings.settingsKey,
                                settings.curiosityVal,
                                settings.moveInterval,
                                settings.viewDistance,
                                settings.spawnRadius,
                                settings.Dispertion
                                FROM userNameSettingsLink 
                                INNER JOIN settings 
                                WHERE userNameSettingsLink.settingsKey = settings.settingsKey
                                AND userNameSettingsLink.username = ?'''

    cur.execute(retrieveSavesCommand,(username,))
    results = cur.fetchall()
    con.commit()
    return results