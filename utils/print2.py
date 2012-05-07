import random  
from reportlab.lib.pagesizes import A4  
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate  
from reportlab.lib.units import mm  
from reportlab.platypus.flowables import PageBreak, Spacer  
from reportlab.platypus.paragraph import Paragraph  
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  
from reportlab.lib import colors  
      
from spreadsheettable import SpreadsheetTable  
styleSheet = getSampleStyleSheet()  
MARGIN_SIZE = 25 * mm  
PAGE_SIZE = A4  
      
def create_pdfdoc(pdfdoc, story):  
        """ 
        Creates PDF doc from story. 
        """  
        pdf_doc = BaseDocTemplate(pdfdoc, pagesize = PAGE_SIZE,  
            leftMargin = MARGIN_SIZE, rightMargin = MARGIN_SIZE,  
            topMargin = MARGIN_SIZE, bottomMargin = MARGIN_SIZE)  
        main_frame = Frame(MARGIN_SIZE, MARGIN_SIZE,  
            PAGE_SIZE[0] - 2 * MARGIN_SIZE, PAGE_SIZE[1] - 2 * MARGIN_SIZE,  
            leftPadding = 0, rightPadding = 0, bottomPadding = 0,  
            topPadding = 0, id = 'main_frame')  
        main_template = PageTemplate(id = 'main_template', frames = [main_frame])  
        pdf_doc.addPageTemplates([main_template])  
      
        pdf_doc.build(story)  
      
def demo():  
        """ 
        Runs demo demonstrating usage of Spreadsheet Tables. 
        """  
        print 'Generating spreadsheet_demo.pdf in current working directiory...'  
        table_style = [  
            ('GRID', (0,0), (-1,-1), 1, colors.black),  
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),  
            ('LEFTPADDING', (0,0), (-1,-1), 3),  
            ('RIGHTPADDING', (0,0), (-1,-1), 3),  
            ('FONTSIZE', (0,0), (-1,-1), 10),  
            ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),  
        ]  
      
        data = [  
            ['Row No', 'Favourite movies'],  
            [RowNumber(), 'Star Wars'],  
            [RowNumber(), 'Back to the  Future'],  
            [RowNumber(), 'Forrest Gump'],  
            [RowNumber(), 'Fight Club'],  
            [RowNumber(), 'The Matrix'],  
            [RowNumber(), 'Terminator'],  
            [RowNumber(), 'Alien'],  
            [RowNumber(), 'Die Hard'],  
            [RowNumber(), 'Blade Runner'],  
            [RowNumber(), 'Star Trek'],  
            [RowNumber(), 'V for Vendetta'],  
            [RowNumber(), 'Twelve Monkeys'],  
            [RowNumber(), 'The Truman Show'],  
        ]  
        story = []  
        story.append(Paragraph("Spreadsheet Table usage demonstration",  
            styleSheet['Title']))  
        story.append(Paragraph("Row enumeration (the simplest possible formula example)", styleSheet['Heading2']))  
        story.append(Paragraph("This saimpossible .", styleSheet['BodyText']))  
        story.append(Spacer(0, 10 * mm))  
        spreadsheet_table = SpreadsheetTable(data, repeatRows = 1)  
        spreadsheet_table.setStyle(table_style)  
        story.append(spreadsheet_table)  
        story.append(PageBreak())  
        story.append(Paragraph("This shows how enumeration behave with split.",  
            styleSheet['BodyText']))  
        story.append(Spacer(0, 10 * mm))  
        spreadsheet_table = SpreadsheetTable(data, repeatRows = 1)  
        spreadsheet_table.setStyle(table_style)  
        s = spreadsheet_table.split(PAGE_SIZE[0], 90)  
        for part in s:  
            story.append(part)  
            story.append(Spacer(0, 10 * mm))  
        story.append(PageBreak())  
      
        story.append(Paragraph("Repeating bottom rows", styleSheet['Heading2']))  
        story.append(Paragraph("This shows how to insert repeatingbottom of table. With normal Table you can only repeat top rows.",  
            styleSheet['BodyText']))  
        story.append(Spacer(0, 10 * mm))  
        data.append(['Row No', 'Favourite movies'])  
        table_style.append(['FONTNAME', (0,-1), (-1,-1), 'Times-Bold'])  
        spreadsheet_table = SpreadsheetTable(data, repeatRows = 1, repeatRowsB = 1)  
        spreadsheet_table.setStyle(table_style)  
        story.append(spreadsheet_table)  
        story.append(PageBreak())  
        story.append(Paragraph("This shows how repeating bottom rows behave with split.", styleSheet['BodyText']))  
        story.append(Spacer(0, 10 * mm))  
        spreadsheet_table = SpreadsheetTable(data, repeatRows = 1, repeatRowsB = 1)  
        spreadsheet_table.setStyle(table_style)  
        s = spreadsheet_table.split(PAGE_SIZE[0], 90)  
        for part in s:  
            story.append(part)  
            story.append(Spacer(0, 10 * mm))  
        story.append(PageBreak())  
      
        story.append(Paragraph("Summary rows", styleSheet['Heading2']))  
        story.append(Paragraph("You can insert formulas", styleSheet['BodyText']))  
        story.append(Spacer(0, 10 * mm))  
        data = [  
            ['Employee', 'Monthly salary'],  
            ['Amy N. Jones', random.randint(2000, 6000)],  
            ['Gloria T. Rodriguez', random.randint(2000, 6000)],  
            ['Kyle S. Tyson', random.randint(2000, 6000)],  
            ['Jeffrey C. Jackson', random.randint(2000, 6000)],  
            ['Roger T. Hicks', random.randint(2000, 6000)],  
            ['Maxine D. Luther', random.randint(2000, 6000)],  
            ['Rita J. Colon', random.randint(2000, 6000)],  
            ['Eva J. Bollinger', random.randint(2000, 6000)],  
            ['William A. Fitch', random.randint(2000, 6000)],  
            ['Martin E. Burke', random.randint(2000, 6000)],  
            ['Richard A. Jones', random.randint(2000, 6000)],  
            ['Richard A. Jone', random.randint(2000, 6000)],  
            ['Stephen G. Pullen', random.randint(2000, 6000)],  
        ]  
        table_style[-1] = ['FONTNAME', (0,-3), (-1,-1), 'Times-Bold']  
        spreadsheet_table = SpreadsheetTable(data, repeatRows = 1, repeatRowsB = 3)  
        spreadsheet_table.setStyle(table_style)  
        story.append(spreadsheet_table)  
        story.append(PageBreak())  
        story.append(Paragraph("This shows how summary rows behave with split.",styleSheet['BodyText']))  
        story.append(Spacer(0, 10 * mm))  
        spreadsheet_table = SpreadsheetTable(data, repeatRows = 1, repeatRowsB = 3)  
        spreadsheet_table.setStyle(table_style)  
        s = spreadsheet_table.split(PAGE_SIZE[0], 160)  
        for part in s:  
            story.append(part)  
            story.append(Spacer(0, 10 * mm))  
      
        story.append(Paragraph("More...", styleSheet['Heading2']))  
        story.append(Paragraph("If you need other formulas to get your work done",styleSheet['BodyText']))  
      
        create_pdfdoc('spreadsheet_demo.pdf', story)  

if __name__ == '__main__':  
        demo()  



