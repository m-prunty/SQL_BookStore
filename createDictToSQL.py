from sql import SQL

class CreateDicttoSQL(SQL):
    def __init__(self, dict_, host='cs1.ucc.ie', usr='mp18', pswrd='choeb', db='cs2208_mp18'):
        super().__init__(host=host, usr=usr, pswrd=pswrd, db=db)
        self.dict = dict_
        
        self._tableList = [i for i in self.dict.keys()]
        
    def create_from_list(self):
        print('create')
        if self.tablesExist() == False:
            cursor = self._cursor()
            for i, j in zip(self._tableList, self.cmdlist):
                print(j)
                cursor.execute(j)
                print(f'Created {i}')
            self._conn.commit()
        else:
            print('Tables already exist')

        return self

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


    def dict_to_tables(self):
        #self.dict = dict_
        self.cmdlist= []
        for key in self._tableList:

            cmd = f"""CREATE TABLE `{self._db}`.`{key}` ("""
           
            for i in self.dict[key]:
                split = i.split(' ')

                if split[1]== 'i':
                    split[1] = 'INT'
                
                elif split[1]== 'v':
                    split[1] = 'VARCHAR(45)'

                elif split[1]== 'd':
                    split[1] = 'DATE'

                cmd += f'{split[0]} {split[1]}'
                cmd += f',' if i != self.dict[key][-1] else f""", PRIMARY KEY ({(self.dict[key][0]).split(' ')[0]}) );"""
            self.cmdlist.append(cmd)
        
        return self



def testBlock():
    sqltables= {'Book': ('ISBN i', 'title v', 'pub d'),
                'BookCopy': ('cpNo i', 'status v', 'ISBN i'),
                'Loan': ('loanID i', 'dateout d', 'datereturned d', 'borID i', 'cpNo i'),
                'Borrower': ('borID i', 'name v', 'address v')
                }

    sqltables= {'Staff' :('staffid i', 'name v', 'branchid v', 'salary i'),
                #'BranchMeasure':('branchid v', 'averagesalary i')
                }
    
    a = CreateDicttoSQL(sqltables)
    a.dict_to_tables()
    a.create_from_list()
    #a.dropTables()
    print ([type(i) for i in a.cmdlist])
    

if __name__ == "__main__":
    testBlock()

