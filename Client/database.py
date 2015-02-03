__author__ = 'Costin'

import pyodbc
import wx
import client_cfg
import os

def _Connection():
    conn = pyodbc.connect(client_cfg.DB_Connection, autocommit=True)
    curs = conn.cursor()
    curs.execute('SET DATEFORMAT dmy')
    return conn

def _SelectRows(query, *args):
    try:
        conn = _Connection()
        curs = conn.cursor()
        curs.execute(query, args)
        rows = curs.fetchall()
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
        return None
    return rows

def _ExecuteQuery(query, *args):
    try:
        conn = _Connection()
        curs = conn.cursor()
        curs.execute(query, args)
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)

def TestLogin(username, password):
    rows = _SelectRows('SELECT COUNT(*) AS Status FROM USERS WHERE username = ? and password = ?', username, password)
    if rows is None or len(rows) == 0:
        return False

    return False if rows[0].Status < 1 else True

def ChangePassword(username, password):
    userId = GetUserId(username)
    _ExecuteQuery('UPDATE Users SET password = ? WHERE ID = ?', password, userId)

def GetUserFullName(username):
    rows = _SelectRows('SELECT firstname, lastname FROM USERS WHERE username = ?', username)
    if rows is None or len(rows) == 0:
        return ''
    return rows[0].firstname + ' ' + rows[0].lastname

def GetDocumentTypes():
    return _SelectRows('SELECT docType FROM DocType ORDER BY docType ASC')

def GetUserId(username):
    rows = _SelectRows('SELECT id FROM Users WHERE username = ?', username)
    if rows is None or len(rows) == 0:
        return ''
    return rows[0].id

def GetDocTypeId(docType):
    rows = _SelectRows('SELECT id FROM DocType WHERE docType = ?', docType)
    if rows is None or len(rows) == 0:
        return ''
    return rows[0].id

def AddDocument(authUser, docType, userDate, lastName, firstName, filePath, description):
    userId = GetUserId(authUser)
    docTypeId = GetDocTypeId(docType)
    try:
        conn = _Connection()
        conn.autocommit = False
        curs = conn.cursor()
        curs.execute('INSERT INTO Documents(user_id, doctype_id, user_date, file_path, first_name, last_name, description) VALUES (?, ?, ?, ?, ?, ?, ?)', userId, docTypeId, userDate, filePath, firstName, lastName, description)
        curs.execute('SELECT @@IDENTITY As newNumber')
        row = curs.fetchone()
        curs.commit()
        conn.close()
    except pyodbc.Error, err:
        wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_ERROR)
        return ''
    return str(row.newNumber) + ' - ' + userDate

def GetDocument(number):
    rows = _SelectRows('SELECT file_path FROM Documents WHERE ID = ?', number)
    if rows is None or len(rows) == 0:
        return ''
    return rows[0].file_path

def GetReport(authUser, docType, dateFrom, dateTo):
    userId = GetUserId(authUser)
    docTypeId = GetDocTypeId(docType)

    return _SelectRows("""SELECT 
                            D.id As Numar,
                            D.user_date As Data,
                            DT.docType As Tip,                            
                            D.last_name + ' ' + D.first_name As Solicitant
                        FROM 
                            Documents D INNER JOIN DocType DT ON D.doctype_id = DT.ID
                        WHERE
                            d.docType_id = ? AND D.user_id = ? AND D.user_date >= ? AND d.user_date <= ?
                        ORDER BY
                            D.id ASC""", docTypeId, userId, dateFrom, dateTo)

