__author__ = 'Costin'

import pyodbc

connString = 'DRIVER={SQL Server};SERVER=LAPTOP\SQLSERVEREXPRESS;DATABASE=NumereDB;UID=sa;PWD=alibaba'

def AddNewUser(username, firstname, lastname):
    conn = pyodbc.connect(connString, autocommit=True)
    curs = conn.cursor()
    curs.execute('INSERT INTO USERS(username, firstname, lastname, password) VALUES(?, ?, ?, ?)', username, firstname, lastname, username)
    conn.close()