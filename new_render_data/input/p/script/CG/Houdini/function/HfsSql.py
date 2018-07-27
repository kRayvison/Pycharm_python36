import os,sys
import sqlite3

def connectsl(file=''):
    new_sl = False
    db_file = "D:/python folder/sql/test.db"
    if not os.path.exists(db_file):
        new_sl = True
        # os.remove("D:/python folder/sql/test.db")
    sl = sqlite3.connect(db_file)
    cu = sl.cursor()

    # if new_sl:
    cu.execute('''CREATE TABLE IF NOT EXISTS ReFerType ( TYPES   TEXT primary key  NOT NULL,INFO TEXT );''')
    sl.commit()
    # sl.close()
    return sl,cu

def createtable(connect,cur,table_name,parms,vales_in):
    cu.execute('''CREATE TABLE IF NOT EXISTS ReFerType ( TYPES   TEXT primary key  NOT NULL,INFO TEXT );''')
    sl.commit()


def getTableInfo(cur,table_name,parms):
    ## parms = ["TYPES"]
    script = "SELECT "
    inde = 0
    for elm in parms:
        if not inde:
            script += elm
            inde =1
        else:
            script += ", " + elm

    script += " from %s"%table_name
    # print(script)
    cursor = cur.execute(script)
    return cursor

def insertToTable(connect,cur,table_name,parms,vales_in):
    ## parms = ["TYPES"]
    ## vales_in = []
    script = "INSERT INTO %s ("%table_name
    vales = " VALUES ("
    inde = 0
    for elm in parms:
        if not inde:
            script += elm
            vales += "?"
            inde =1
        else:
            script += ", " + elm
            vales += ",?"

    script += " )" + vales + ")"
    # print(script)
    cur.execute(script,vales_in)
    connect.commit()


def main():
    type_list = ["file","tex","map"]
    sl,cu = connectsl()
    table_name = "ReFerType"
    cursor = getTableInfo(cu,table_name,["TYPES"])
    ## get typelist
    typelist = []
    for elm in cursor:
        print("elm",elm)
        typelist.append(elm[0])

    print(typelist)
    for elm in type_list:
        if not elm in typelist:
            insertToTable(sl,cu,table_name,["TYPES"],[elm])


if __name__ == '__main__':
    main()
