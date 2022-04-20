import pymysql
#import pprint

class SQL(object):   
    
    def __init__(self, host = 'cs1.ucc.ie', usr = 'mp18',pswrd = 'choeb',db = 'cs2208_mp18'):
        self._host = host
        self._usr = usr
        self._pswrd = pswrd
        print('db')
        self._db = db
        self._tableList = ['OrderList','StockList', 'BackOrderList']


    def __str__(self):
        cursor = self._cursor(cclass = pymysql.cursors.Cursor)
        self._rows = []
        if self.tablesExist() == False:
            #return ('Tables have not been created yet')
            return('No tables to print')
        else:
            for i in self._tableList:
                
                cursor.execute(f"SELECT * FROM {i}")
                self._rows = cursor.fetchall()
                
                if self._rows:
                    print(f"{i}:")
                    [print (i) for i in self._rows]
            return ('Done')
            
    

    def _cursor(self, cclass = pymysql.cursors.DictCursor):
        self._conn = pymysql.Connect(
                            host = self._host,
                            user = self._usr,
                            password = self._pswrd,
                            database = self._db,
                            cursorclass= cclass
                            )
        if self._conn:
            print ('Connected')
        else:
            print('Could not connect')
        return self._conn.cursor()

    def tablesExist(self):
        cursor = self._cursor(cclass = pymysql.cursors.Cursor)
        cursor.execute("SHOW TABLES")
        self._rows = cursor.fetchall()
        fullTable = [i[0] for i in self._rows]
        if all(elem in fullTable for elem in self._tableList) == True:
            #print('TRUE')
            return True
        
        else:
            #print('FALSE')
            print('There are no tables')
            return False

    def dropTables(self):
        cursor = self._cursor()
        print(self._tableList)
        for i in self._tableList:
            try:
                (cursor.execute(f"DROP TABLE {i}"), print(f"{i} Dropped") )
            except:
                print(f'{i} does not exist')

        
        '''  
        if self.tablesExist() == True:
            print(self._tableList)
            [(cursor.execute(f"DROP TABLE {i}"), print(f"{i} Dropped") )for i in self._tableList]
            return self
        else:
            return self
       
        '''


def testBlock():
   
    a = SQL()
    a.tablesExist()
    a.dropTables()
    
    print(a)

if __name__ == "__main__":
    testBlock()    
