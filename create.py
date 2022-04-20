#import pymysql
from sql import SQL

class Create(SQL):
    def __init__(self, host='cs1.ucc.ie', usr='mp18', pswrd='choeb', db='cs2208_mp18'):
        super().__init__(host=host, usr=usr, pswrd=pswrd, db=db)


        self._tables()
        self._trigger()
        
    def createAll(self):
        print('create')
        if self.tablesExist() == False:
            cursor = self._cursor()
            cursor.execute(self._SQLorder)
            print('Created OrderList')
            cursor.execute(self._SQLstock)
            print('Created StockList')
            cursor.execute(self._SQLback)
            print('Created BackOrderList')
            cursor.execute(self._SQLtrigger)
            print('Created Trigger: Before_Insert ')
            

            self._conn.commit()
        else:
            print('Tables already exist')

        return self
    

    
    def _tables(self):
        print('tab')
                
        self._SQLorder = f"""CREATE TABLE `{self._db}`.`OrderList` (
                            orderid INT NOT NULL auto_increment, 
                            bookid INT,
                            orderername VARCHAR(50),
                            ordereraddress VARCHAR(50),
                            quantity INT,
                            fulfilled INT,
                            PRIMARY KEY (orderid)
                            );
                        """
        
        self._SQLstock = f"""CREATE TABLE `{self._db}`.`StockList`(
                            bookid INT NOT NULL auto_increment,
                            booktitle VARCHAR(50),
                            author VARCHAR(50), 
                            quantityinstock INT,
                            PRIMARY KEY (bookid)
                            );
                        """  

        self._SQLback = f"""CREATE TABLE `{self._db}`.`BackOrderList`(
                            backorderid INT NOT NULL auto_increment,
                            orderid INT,
                            quantity INT,
                            PRIMARY KEY (backorderid)
                            );
                        """
        #print(list(locals()))
        return self

                #self._conn.commit()
                #print('commit')
    
    def _trigger(self):

        self._SQLtrigger =(
            f"""CREATE DEFINER=`{self._usr}`@`%` TRIGGER `{self._db}`.`OrderList_BEFORE_INSERT` BEFORE INSERT ON `OrderList` FOR EACH ROW
                        BEGIN
                            DECLARE nStock int;
                            DECLARE oldStock int;
                            DECLARE ordid int;
                            
                            SELECT StockList.quantityinstock
                                INTO oldStock
                                FROM StockList 
                                WHERE StockList.bookid = NEW.bookid;
                            SET nStock = oldStock - NEW.quantity;
                            
                            IF nStock >= 0 
                            THEN
                                SET NEW.fulfilled = 1;
                                
                                UPDATE StockList 
                                    SET StockList.quantityinstock = nStock
                                    WHERE bookid = NEW.bookid;
                                
                            ELSE 
                                SET NEW.fulfilled = 0;
                                
                                UPDATE StockList 
                                    SET StockList.quantityinstock = nStock
                                    WHERE bookid = NEW.bookid;
                                
                                SELECT Max(orderid)
									INTO ordid 
                                    FROM OrderList;
                                
                                
                                INSERT INTO BackOrderList (orderid, quantity)
                                    VALUES(ordid +1, ABS(nStock));
                            END IF;
                                
                                
                        END
                        """
                        )
        return self




    

def testBlock():
    
    
    a = Create()
    a.dropTables()
    a.createAll()
    a.createAll()
    
    
    print(a)

if __name__ == "__main__":
    testBlock()

