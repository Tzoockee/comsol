__author__ = 'Costin'

import pyodbc
import wx
import sys
sys.path.append("..\\Shared\\")
from settings import settings

def CreateDatabase(conn, curs):
    curs.execute('CREATE DATABASE NumereDB')
    curs.execute('USE NumereDB')
    curs.execute("""CREATE TABLE [dbo].[docType](
                    [id] [int] IDENTITY(1,1) NOT NULL,
                    [doctype] [varchar](50) NOT NULL,
                    [description] [varchar](500) NOT NULL,
                 CONSTRAINT [PK_docType] PRIMARY KEY CLUSTERED
                (
                    [id] ASC
                )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
                ) ON [PRIMARY]""")
    curs.execute("""CREATE UNIQUE NONCLUSTERED INDEX [IX_docType] ON [dbo].[docType]
                    (
                        [doctype] ASC
                    )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
                    """)
    curs.execute("""CREATE TABLE [dbo].[Users](
                    [id] [int] IDENTITY(1,1) NOT NULL,
                    [username] [varchar](50) NOT NULL,
                    [firstname] [varchar](50) NOT NULL,
                    [lastname] [varchar](50) NOT NULL,
                    [password] [varchar](50) NOT NULL,
                 CONSTRAINT [PK_Users] PRIMARY KEY CLUSTERED
                (
                    [id] ASC
                )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
                ) ON [PRIMARY]""")
    curs.execute("""CREATE UNIQUE NONCLUSTERED INDEX [IX_Users] ON [dbo].[Users]
                    (
                        [username] ASC
                    )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
                    """)
    curs.execute("""CREATE TABLE [dbo].[Documents](
                    [id] [int] IDENTITY(""" + str(settings['Start_Seed']) + """,1) NOT NULL,
                    [user_id] [int] NOT NULL,
                    [doctype_id] [int] NOT NULL,
                    [user_date] [date] NOT NULL,
                    [system_date] [datetime] NOT NULL CONSTRAINT [DF_Documents_system_date]  DEFAULT (getdate()),
                    [file_path] [varchar](512) NOT NULL,
                    [first_name] [varchar](128) NOT NULL,
                    [last_name] [varchar](128) NOT NULL,
                    [description] [varchar](1024) NOT NULL,
                 CONSTRAINT [PK_Documents] PRIMARY KEY CLUSTERED
                (
                    [id] ASC
                )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
                ) ON [PRIMARY]""")
    curs.execute("""ALTER TABLE [dbo].[Documents]  WITH CHECK ADD  CONSTRAINT [FK_Documents_docType] FOREIGN KEY([doctype_id])
                    REFERENCES [dbo].[docType] ([id])""")
    curs.execute('ALTER TABLE [dbo].[Documents] CHECK CONSTRAINT [FK_Documents_docType]')
    curs.execute("""ALTER TABLE [dbo].[Documents]  WITH CHECK ADD  CONSTRAINT [FK_Documents_Users] FOREIGN KEY([user_id])
                    REFERENCES [dbo].[Users] ([id])""")
    curs.execute('ALTER TABLE [dbo].[Documents] CHECK CONSTRAINT [FK_Documents_Users]')

def Connection():
    conn = pyodbc.connect(settings['DB_Connection'], autocommit=True)
    curs = conn.cursor()
    try:
        curs.execute('USE NumereDB')
    except pyodbc.Error, err:
        CreateDatabase(conn, curs)
        curs.execute('USE NumereDB')
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
        curs.execute('DELETE FROM docType WHERE docType = ''?''', docType)
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

