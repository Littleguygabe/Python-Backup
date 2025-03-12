import sqlite3

con = sqlite3.connect('practise_db.db')
cur = con.cursor()

#create nodedata table
createnodedata = '''CREATE TABLE IF NOT EXISTS NodeData
                    (nodeID INTEGER PRIMARY KEY, x INTEGER, y INTEGER)'''

cur.execute(createnodedata)

#create paths table
createpathdata = '''CREATE TABLE IF NOT EXISTS Path
                (nodeID INTEGER, path_length FLOAT, FOREIGN KEY(nodeID) REFERENCES NodeData(nodeID))'''
cur.execute(createpathdata)

#ADD TO NODEDATA
cur.execute("INSERT INTO NodeData VALUES (1,1200,754)")
cur.execute("INSERT INTO NodeData VALUES (2,800,60)")
cur.execute("INSERT INTO NodeData VALUES (3,352,968)")

#ADD TO PATHS
cur.execute("INSERT INTO Path VALUES (1,10982)")
cur.execute("INSERT INTO Path VALUES (2,17290)")
cur.execute("INSERT INTO Path VALUES (3,6483)")

cur.execute("SELECT * FROM Path")
results = cur.fetchall()
print(results)

cur.execute("UPDATE Path SET path_length = 19203 WHERE nodeID = 3")

cur.execute("SELECT * FROM Path")
results = cur.fetchall()
print(results)