import sqlite3
import mysql.connector

class DB:
    def __init__(self):                              
        self.__conn = mysql.connector.connect(host="127.0.0.1",database = 'web_crawler',user="root",passwd="12345678",auth_plugin='mysql_native_password')
        self.__cursor_limitation = 10
        # self.__path = "/Users/kyriezhang/PycharmProjects/Server/web.db"
        # self.__conn = sqlite3.connect(self.__path)
        # #The max number of cursor instance may exist.
        # self.__cursor_limitation = 10

    def __wait(self):
        #Check if still have the instance.
        while (self.__cursor_limitation <= 0):
            pass

    #For the select statements. Returns the result.
    def select(self, sql , params = []):
        #Block until the resource free.
        self.__wait()
        self.__cursor_limitation -=1
        cursor = self.__conn.cursor()
        #Execute the query statement.

        sqlList = sql.split('?')
        sql = sqlList[0]
        for i in range(len(sqlList)-1):
            sql = sql + '\'' + params[i] + '\'' + sqlList[i+1]
        cursor.execute(sql)
        #Get the result by fetchall.
        result = cursor.fetchall()
        #Close the cursor.
        cursor.close()
        #Commit the transaction.
        self.__conn.commit()
        self.__cursor_limitation +=1
        return result
    
    #For the update, insert and delete statements. This
    # will return the affected rows count.
    def modify(self, sql , params = []):
        self.__wait()
        self.__cursor_limitation -=1
        cursor = self.__conn.cursor()
        #Execute the query statement.
        sqlList = sql.split('?')
        sql = sqlList[0]
        for i in range(len(sqlList)-1):
            sql = sql + '\'' + params[i] + '\'' + sqlList[i+1]

        cursor.execute(sql)
        #Get the result by fetchall.
        result = cursor.rowcount
        #Close the cursor.
        cursor.close()
        #Commit the transaction.
        self.__conn.commit()
        self.__cursor_limitation +=1
        return result
    
    #Refresh the connction.
    def refresh(self):
        self.__conn.close()
        self.__conn = mysql.connector.connect(host="127.0.0.1",user="root",passwd="12345678")
        self.__cursor_limitation = 10

def main():
    db = DB()
    # result = db.select('CREATE TABLE link(id INTEGER PRIMARY KEY AUTOINCREMENT,'
    #                    ' title varchar(50) , '
    #                    ' url varchar(500) , '
    #                    ' dat date)')
    # print(result)
    # result = db.select('SELECT * FROM link')
    # print(result)
    result = db.select('SELECT * FROM link WHERE dat >= ? AND dat <= ?' , ["2018-11-15" , "2018-11-16"])
    # result = db.select('SELECT * FROM link')
    print(result)



if __name__ == '__main__':
    main()
