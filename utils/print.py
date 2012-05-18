from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import sys
sys.path.append("..")
from models.database import Task,session_connect
from models.database import session_connect,Task

from reportlab.lib.pagesizes import letter
def task_teacher():
    font = "Helvetica"
    font_size=12

    x=60
    y=550

    destination_file="/tmp/first.pdf"
    my_canvas=canvas.Canvas(destination_file)
    my_canvas.setFont(font,font_size)
    my_canvas.setLineWidth(.3)
    text=""
    for row in session_connect.query(Task).all():
        x = 60
        if row.content==None:
            row.content = ""
        name=''.join(row.name)
        y = y+30
        my_canvas.drawString(x,y,name)
        teacher = ''.join(row.pub_teacher)
        x = x + 300
        my_canvas.drawString(x,y,teacher)

    y = y+50
    my_canvas.drawString(60,y,"Task Name")
    my_canvas.drawString(360,y,"Pub Teacher")
    my_canvas.save()


if __name__=="__main__":
    task_teacher()
