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

def GetUsers():
    try:
        conn = Connection()
        curs = conn.cursor()
        curs.execute('SELECT username As Utilizator, lastname as Nume, firstname as Prenume FROM USERS')
        rows = curs.fetchall()
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
    return rows

def GetDocTypes():
    try:
        conn = Connection()
        curs = conn.cursor()
        curs.execute('SELECT docType As Tip, description as Descriere FROM DocType')
        rows = curs.fetchall()
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
    return rows

