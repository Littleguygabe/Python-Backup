import sqlite3

class databasepractice():
    def __init__(self):
        print('database operating')
        self.con = sqlite3.connect('practice.db')
        self.cur = self.con.cursor()

        self.cur.execute('''CREATE TABLE IF NOT EXISTS points
                        (settingsid text PRIMARY KEY, x real, y real)''')
        
        self.executefunction()
    
    def executefunction(self):
        try:
            self.cur.execute('''INSERT INTO points VALUES
                            ('AUJN1893', '1982', '89')''')
            self.con.commit()

            self.printdatabase()
        except:
            print('Duplicate ID')

    def printdatabase(self):
        for row in self.cur.execute('''SELECT * FROM points'''):
            print(row)

if __name__ == '__main__':
    databasepractice()
