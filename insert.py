from sql import SQL
import sys

class Insert(SQL):
    def __init__(self, host='cs1.ucc.ie', usr='mp18', pswrd='choeb', db='cs2208_mp18'):
        super().__init__(host=host, usr=usr, pswrd=pswrd, db=db)

        if self.tablesExist() == False:
            print("Cannot Insert as Tables don't exist")
            sys.exit()
        

    def insertStock(self, stockList):
        
        if self.tablesExist() == True:
            cursor = self._cursor()
            n= 0
            for i,j,k in stockList:
                self._SQLinsert= f"INSERT INTO StockList (booktitle, author, quantityinstock) VALUES('{i}','{j}',{k});"
                cursor.execute(self._SQLinsert)
                n+=1
                print(f'insert stock op {n}: {i,j,k}')
            self._conn.commit()

        return self

    def insertOrder(self,orderList):
        
        if self.tablesExist() == True:
            cursor = self._cursor()
            n=0
            for i,j,k,l in orderList:
                
                self._SQLinsert= f"INSERT INTO OrderList (bookid, orderername, ordereraddress, quantity) VALUES('{i}','{j}','{k}', {l});"
                #print(self._SQLinsert)
                cursor.execute(self._SQLinsert)
                n+=1
                print(f'insert order op {n}: {i,j,k,l}')
            self._conn.commit()
        return self



    def readfile(self, file):
        with open(file) as inFile:
            fileLines = [line.strip('\n').lstrip(' ').split(',') for line in inFile]
            
        
        return fileLines

def testBlock():
    
    
    a = Insert()
    #a.dropTables()
    a.insertStock(a.readfile('bookData.txt'))
    a.insertOrder(a.readfile('orderData.txt'))
   

    
    
    print(a)

if __name__ == "__main__":
    testBlock()