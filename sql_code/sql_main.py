'''Programme to connect and query a SQLite DB
'''


import python_sql as pysql
import os.path as path

if __name__ == "__main__":
    print("Working with SQLite DB")

    nfilename = "/Users/Ben/Documents/Flask_project/Databases/dblog.db" #This needs checking on different computers, should us OS join
    if path.exists(nfilename):
        #Below will connect to DB
        _, con_new, cursor_new = pysql.connect_db(nfilename, 0)
        tab_list = pysql.query_existing(cursor_new)
        sql_txt = "SELECT timestamp FROM temlog WHERE DHT_temp = 26"
        result = pysql.select_existing(cursor_new,sql_txt)
        print(result)