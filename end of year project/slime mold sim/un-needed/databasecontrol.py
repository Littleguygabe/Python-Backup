import sqlite3

def createtable():
    con = sqlite3.connect('paramaters.db')
    cur = con.cursor()

    createnodedatacommand = '''CREATE TABLE IF NOT EXISTS NodeData
                    (gameID INTEGER,nodeID INTEGER, pathLength INTEGER, shortestArray TEXT, x INTEGER, y INTEGER)'''

    cur.execute(createnodedatacommand)
    con.commit()
    
def creategameID():
    gameid = 0
    try:
        con = sqlite3.connect('paramaters.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM paramaterValues")
        results=cur.fetchall()
        gameid = len(results)+1
        return gameid

        #change to max function rather than building it off of length

    except:
        return 1

def updatenoderegisters(nodeid,shortestlength,shortestArray,gameid,x,y):
    con = sqlite3.connect('paramaters.db')
    cur = con.cursor()

    insertnewnodecommand = "INSERT INTO NodeData VALUES(?, ?, ?, ?, ?, ?)"
    cur.execute(insertnewnodecommand,(gameid, nodeid, shortestlength, shortestArray, x, y,))

    cur.execute("SELECT * FROM NodeData")
    results=cur.fetchall()
    con.commit()

def GetPastGame(gameid):
    coords = []
    #check save exists
    con = sqlite3.connect('paramaters.db')
    cur = con.cursor()
    findposcommand = "SELECT * FROM NodeData WHERE gameID = ?"
    cur.execute(findposcommand, (gameid,))
    results = cur.fetchall()
    for i in range(0,len(results)):
        temparray = []
        temparray.append(results[i][4])
        temparray.append(results[i][5])
        coords.append(temparray)



    con.commit()
    print(f'Loaded Game Save {gameid}')
    return(coords)

def rgb_to_hex(r,g,b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def getparamaters(gameid):
    con = sqlite3.connect('paramaters.db')
    cur = con.cursor()
    getparamatersCommand = "SELECT * FROM paramaterValues WHERE gameID = ?"
    cur.execute(getparamatersCommand,(gameid,))
    paramaterResults = cur.fetchall()
    con.commit()
    
    #put all parameter and agent positions in one function to tick databse box
    nagents=paramaterResults[0][1]
    taillen=paramaterResults[0][2]
    unlimitfpsoption = paramaterResults[0][3]
    fpslimit = paramaterResults[0][4]
    displayfpsoption = paramaterResults[0][5]
    

    return(nagents,taillen,unlimitfpsoption,fpslimit,displayfpsoption)

def getDBcolour(elementID):
    con = sqlite3.connect('colourdb.db')
    cur = con.cursor()
    getColourCommand = "SELECT R, G, B FROM ColourScheme WHERE element_ID = ?"
    try:
        cur.execute(getColourCommand,(elementID,))
        results=cur.fetchall()
        hexcode = rgb_to_hex(results[0][0],results[0][1],results[0][2])
    except:
        if elementID == 1:
            hexcode = rgb_to_hex(0,255,0)
        elif elementID == 2:
            hexcode = rgb_to_hex(0,0,0)

        elif elementID == 3:
            hexcode = rgb_to_hex(255,255,255)
    con.commit()
    return hexcode

def getShortestValues(gameid,nodeid):
    con=sqlite3.connect('paramaters.db')
    cur=con.cursor()

    getpathdataCommand = "SELECT pathLength FROM NodeData WHERE gameID = ? AND nodeID = ?"
    cur.execute(getpathdataCommand,(gameid,nodeid,))
    results=cur.fetchall()
    currentshortest = results[0][0]
    con.commit()
    return currentshortest

def updateshortestpath(newpathlength,gameid,nodeid):
    con=sqlite3.connect('paramaters.db')
    cur=con.cursor()
    updatepathCommand = "UPDATE NodeData SET pathLength = ? WHERE gameID = ? AND nodeID = ?"
    cur.execute(updatepathCommand,(newpathlength,gameid,nodeid,))
    con.commit()

def insertNodePositions(classArray,gameid):
    con = sqlite3.connect('paramaters.db')
    cur=con.cursor()
    createagentPosCommand = '''CREATE TABLE IF NOT EXISTS AgentPositions
                    (gameID INTEGER,AgentX INTEGER, AgentY INTEGER, AgentAngle INTEGER)'''
    
    cur.execute(createagentPosCommand)

    checkEmptyCommand = "SELECT * FROM AgentPositions WHERE gameID = ?"
    cur.execute(checkEmptyCommand,(gameid,))
    results = cur.fetchall()

    if len(results)>0:
        #DELETE DATA FIRST
        deleteAgentDataCommand = "DELETE FROM AgentPositions WHERE gameID = ?"
        cur.execute(deleteAgentDataCommand,(gameid,))

        insertAgentDataCommand = "INSERT INTO AgentPositions VALUES(?, ?, ?, ?)"
        for i in range(0,len(classArray)):
            xpos = classArray[i].xpos
            ypos = classArray[i].ypos
            agentAngle = classArray[i].angle

            cur.execute(insertAgentDataCommand,(gameid,xpos,ypos,agentAngle,))
            con.commit()

    else:
        print('Insert Data')
        insertAgentDataCommand = "INSERT INTO AgentPositions VALUES(?, ?, ?, ?)"
        for i in range(0,len(classArray)):
            xpos = classArray[i].xpos
            ypos = classArray[i].ypos
            agentAngle = classArray[i].angle

            cur.execute(insertAgentDataCommand,(gameid,xpos,ypos,agentAngle,))
            con.commit()

def getagentpositions(gameid):
    con=sqlite3.connect('paramaters.db')
    cur = con.cursor()
    getagentpositionscommand = "SELECT AgentX, AgentY FROM AgentPositions WHERE gameID = ?"
    cur.execute(getagentpositionscommand,(gameid,))
    results = cur.fetchall()
    print(results)
    con.commit()

    return results

def DoesDBExist():
    try:
        con=sqlite3.connect('file:paramaters.db?mode=rw', uri=True)
        return(True)
    except:
        return(False)
    
def saveParameters():
    print('Saving Parameters')