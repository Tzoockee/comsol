==========================================================================================
De instalat:
==========================================================================================

1. Python 2.7.9 32bit 
	https://www.python.org/downloads/

2. wxPython 3.0 pentru Python 2.7 32bit 
	http://www.wxpython.org/download.php

3. pyODBC 3.0.7 pentru Python 2.7 32bit 
	https://code.google.com/p/pyodbc/

--------------------
Pentru Client:
--------------------
1. MS SQL Server ODBC driver 
	http://www.microsoft.com/en-us/download/details.aspx?id=36434

--------------------
Pentru Server:
--------------------
1. MS SQL Server Express 2014 64bit: SQLEXPR_x64_ENU.exe
	http://www.microsoft.com/en-us/download/details.aspx?id=42299
	- La instalare se retine numele serverului
	- Se seteaza "Mixed Authentication" si se retine parola pentru userul "sa"

2. Optional: MS SQL Server Management Studio 64bit: SQLManagementStudio_x64_ENU.exe
	http://www.microsoft.com/en-us/download/details.aspx?id=42299


==========================================================================================
De configurat:
==========================================================================================
--------------------
Pentru Client:
--------------------
1. In client_cfg.py:
	- docRepositoryPath -> unde se salveaza documentele
	- DB_Connection     -> string-ul de conectare la baza de date. Se modifica: SERVER, DATABASE, UID, PWD	

--------------------
Pentru Server:
--------------------
2. In admin_cfg.py:
	- DB_Connection     -> string-ul de conectare la baza de date. Se modifica: SERVER, DATABASE, UID, PWD