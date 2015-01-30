__author__ = 'Costin'

import pyodbc
import wx
import admin_cfg

def Connection():
    conn = pyodbc.connect(admin_cfg.DB_Connection, autocommit=True)
    return conn

def AddNewUser(username, firstname, lastname):
    try:
        conn = Connection()
        curs = conn.cursor()
        curs.execute('INSERT INTO USERS(username, firstname, lastname, password) VALUES(?, ?, ?, ?)', username, firstname, lastname, username)
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
		
def AddNewDocType(docType, description):
    try:
        conn = Connection()
        curs = conn.cursor()
        curs.execute('INSERT INTO DocType(docType, description) VALUES(?, ?)', docType, description)
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)

def DeleteUser(username):
    try:
        conn = Connection()
        curs = conn.cursor()
        curs.execute('DELETE FROM USERS WHERE username = ''?''', username)
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
		
def DeleteDocType(docType):
    try:
        conn = Connection()
        curs = conn.cursor()
        curs.execute('DELETE FROM DocTypes WHERE docType = ''?''', docType)
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)

def FillUserList(userlist):
    try:
        conn = Connection()
        curs = conn.cursor()
        curs.execute('SELECT username, firstname, lastname FROM USERS')
        index = 0
        for row in curs:
            userlist.InsertStringItem(index, str(row.username))
            userlist.SetStringItem(index, 1, str(row.firstname))
            userlist.SetStringItem(index, 2, str(row.lastname))
            index = index + 1
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)

def FillDocTypeList(docTypeList):
    try:
        conn = Connection()
        curs = conn.cursor()
        curs.execute('SELECT doctype, description FROM DocType')
        index = 0
        for row in curs:
            docTypeList.InsertStringItem(index, str(row.doctype))
            docTypeList.SetStringItem(index, 1, str(row.description))
            index = index + 1
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)