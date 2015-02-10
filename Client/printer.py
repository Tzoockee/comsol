from wx.html import HtmlEasyPrinting
import HTML

class Printer(HtmlEasyPrinting):
    def __init__(self, parent):
        global frame
        HtmlEasyPrinting.__init__(self,name="Printing", parentWindow=parent)
     
    def PreviewText(self, rows, doc_name):
        self.SetHeader(doc_name)
        HtmlEasyPrinting.PreviewText(self, self.GetReportTableForPrint(rows))    
    
    def Print(self, rows, doc_name):
        self.SetHeader(doc_name)
        self.PrintText(self.GetReportTableForPrint(rows), doc_name)    
        
    def GetReportTableForPrint(self, rows):
        if len(rows) == 0:
            return
    
        col_names = [cn[0] for cn in rows[0].cursor_description]
        t = HTML.Table(header_row=col_names, style = 'border-collapse:collapse;', cellpadding = '5', cellspacing = '0', border = '2')
        for row in rows:
            t.rows.append([cell for cell in row])
        return str(t)
 
        
