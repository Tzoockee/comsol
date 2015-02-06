def FillListCtrl(listCtrl, rows):
    listCtrl.ClearAll()

    if len(rows) == 0:
        return
        
    for index, column in enumerate(rows[0].cursor_description):
        listCtrl.InsertColumn(index+1, column[0])
            
    for indexRow, row in enumerate(rows):
        listCtrl.InsertStringItem(indexRow, str(row[0]))
        for indexCol in range(1, len(row.cursor_description)):
            listCtrl.SetStringItem(indexRow, indexCol, str(row[indexCol]))

def GetDateString(dateCtrl):
    selectedYear = str(dateCtrl.GetValue().Year)
    selectedMonth = str(dateCtrl.GetValue().Month+1)
    selectedDay = str(dateCtrl.GetValue().Day)
    return selectedDay + '/' + selectedMonth + '/' + selectedYear