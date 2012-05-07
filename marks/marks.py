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




@marks.route("/selectstudent/",defaults={'page':1},methods=['GET','POST'])
@marks.route("/selectstudent/<int:page>")
def selectstudent(page):

    PER_PAGE = 10
    #Get all the tasks
    task = {}
    tasks = []
    for row in session_connect.query(Task).filter(Task.pub_teacher==session["user"]).all():
        #mark = session_connect.query(Marks).filter(Marks.studentnum==row.select_student).first()
        #task["name"] = row.name
        #task["pub_teacher"] = row.pub_teacher
        #task["select_stduent"] = row.select_student
        #s = select([Task,Marks],row.select_student==Marks.studentnum)
        #task = get_tasks(s) 
        task = session_connect.query(Task.id,Task.pub_teacher,Task.select_student,Task.name,Task.studentname,Task.teachername,Marks.studentnum,Marks.final_mark).filter(Marks.studentnum==row.select_student,Task.select_student==Marks.studentnum).first()
        print dir(task)
        #print task.final_mark
        tasks.append(task)
        #print mark.final_mark

    #Paginator    
    task_page = get_task_for_page(tasks,page,PER_PAGE,len(tasks))
    p = SimplePagination(page,PER_PAGE,len(tasks))
    return render_template('selectstudent.html',pagination=p,tasks=task_page)

#@marks.route("/markstudent"methods=['GET','POST'])
@marks.route("/markstudent/<studentid>",methods=['GET','POST'])
def markstudent(studentid):
    session["studentid"]=studentid
    if studentid:
        if session["user"]:
            if request.method=="POST":
                trans_mark = int(request.form["trans_thesis"])
                thesis_mark = int(request.form["thesis"])
                final_mark = trans_mark+thesis_mark
                mark = Marks(studentnum=studentid,teachernum=session["user"],trans_mark=trans_mark,thesis_mark=thesis_mark,final_mark=final_mark)
                session_connect.add(mark)
                session_connect.commit()
            
        return render_template("markstudent.html")
    else:
        return redirect("marks.selectstudent")
    
