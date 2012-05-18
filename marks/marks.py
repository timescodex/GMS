from flask import Flask,render_template,request,Blueprint,session,redirect,url_for
marks = Blueprint('marks',__name__,template_folder='templates',static_folder='static')
import sys
sys.path.append("..")
from models.database import session_connect,Task,Marks,Thesis
from flaskext.sqlalchemy import Pagination
from math import ceil
import xmlrpclib
from sqlalchemy import *

class SimplePagination(object):
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1
    @property
    def has_next(self):
        return self.page < self.pages
    def iter_pages(self, left_edge=2, left_current=2,right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
                num > self.pages - right_edge:
                if last + 1 != num:
                    yield last
                yield num
                last = num


def get_task_for_page(students,page,PER_PAGE,count):
    #After get for the page 
    PER_PAGE = PER_PAGE
    if page >= 1:
        if page*PER_PAGE < count:
            begin = (page-1)*PER_PAGE
            end = PER_PAGE+begin
            for student in students[begin:end]:
                return students[begin:end]
        else:
            begin = (page-1)*PER_PAGE
            end = count//page+begin
            return students[begin:end]
    else:
        return None


def get_tasks(stmt):
    rs = stmt.execute()
    tasks=[]
    for row in rs:
        tasks.append(row)
    return tasks

def Markexist(studentid):
    marks = session_connect.query(Marks).filter(Marks.studentnum==studentid).first()
    if marks:
        return True
    else:
        return False

@marks.route("/selectstudent/",defaults={'page':1},methods=['GET','POST'])
@marks.route("/selectstudent/<int:page>")
def selectstudent(page):

    PER_PAGE = 10
    #Get all the tasks
    task = {}
    tasks = []
    for row in session_connect.query(Task).filter(Task.pub_teacher==session["user"]).all():
        task = session_connect.query(Task).filter(Task.select_student==row.select_student).first()
        if task:
            tasks.append(task)
        else:
            pass
    task_page = get_task_for_page(tasks,page,PER_PAGE,len(tasks))
    p = SimplePagination(page,PER_PAGE,len(tasks))
    return render_template('selectstudent.html',pagination=p,tasks=task_page)

#@marks.route("/markstudent"methods=['GET','POST'])
@marks.route("/markstudent/<studentid>",methods=['GET','POST'])
def markstudent(studentid):
    session["studentid"]=studentid
    exist = Markexist(studentid)
    if exist==False:
        if session["user"]:
            if request.method=="POST":
                #trans_mark = int(request.form["trans_thesis"])
                thesis_mark = int(request.form["thesis"])
                final_mark = thesis_mark
                mark = Marks(studentnum=studentid,teachernum=session["user"],thesis_mark=thesis_mark,final_mark=final_mark)
                session_connect.add(mark)
                session_connect.commit()
            
        return render_template("markstudent.html")
    else:
        print "run into update!!!!!!"
        mark = session_connect.query(Marks).filter(Marks.studentnum==studentid).first()
        print "run here!!!!"
        print mark.final_mark
        if request.method=="POST":
            thesis_mark = int(request.form["updatethesis"])
            
            mark.thesis_mark = thesis_mark
            mark.final_mark = thesis_mark
            session_connect.commit()
    return render_template("markstudent.html",mark=mark)
   


@marks.route("/showmark",methods=['GET','POST'])
def showmark():
    mark = session_connect.query(Marks).filter(Marks.studentnum==session['user']).first()
    return render_template("showmark.html",mark=mark)

