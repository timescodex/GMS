#usr/bin/python
import os

from flask import Flask,config,session,g,redirect,url_for,abort,render_template,flash,request,Blueprint

import sys
sys.path.append("..")
from models.database import User,Thesis,Task
from models.database import session_connect 
#from database import User   #import the orm user model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
thesis = Blueprint('thesis',__name__,template_folder='templates')
from werkzeug import secure_filename
from pymongo import Connection
import gridfs
from datetime import datetime
from flaskext.sqlalchemy import Pagination
from math import ceil

UPLOAD_FOLDER = './Thesis'
ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



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

def get_thesis_for_page(thesis,page,PER_PAGE,count):
    #After get for the page 
    PER_PAGE = PER_PAGE
    if page >= 1:
        if page*PER_PAGE < count:
            begin = (page-1)*PER_PAGE
            end = PER_PAGE+begin
            for t in thesis[begin:end]:
                return thesis[begin:end]
        else:
            begin = (page-1)*PER_PAGE 
            end = count//page+begin 
            return thesis[begin:end]
    else:
        return None



@thesis.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            db = Connection().thesis
            fs = gridfs.GridFS(db)
            thesis_id = session["user"]
            if fs.exists(thesis_id):
                file2 = fs.get(thesis_id)
                print file2.name

                fs.delete(thesis_id)
                fs.put(file,_id=thesis_id,filename=file.filename)
            else:
                a = fs.put(file,_id=thesis_id,filename=file.filename)
                file2 = fs.get(thesis_id)
            
            if session["user"]:
                if session["role"]=="student":
                    print "run into upload"
                    thesispath = os.path.join(UPLOAD_FOLDER, filename)
                    thesisuptime=str(datetime.now())
                    student = session_connect.query(User).filter(User.num==session["user"]).first()
                    task = session_connect.query(Task).filter(Task.select_student==session["user"]).first()
                    thesis = Thesis(thesisname=filename,thesispath=thesispath,thesisuptime=thesisuptime,studentnum=session["user"],studentname=student.name,teachernum=task.pub_teacher,teachername=task.teachername)
                    session_connect.add(thesis)
                    session_connect.commit()
            #file.save(os.path.join(UPLOAD_FOLDER, filename))
    return render_template("upload.html")

@thesis.route("/showthesis",methods=['GET','POST'])
def showthesis():
    return render_template("showthesis.html") 


@thesis.route("/collectthesis",defaults={'page':1},methods=['GET','POST'])
@thesis.route("/collectthesis/<int:page>")
def collectthesis(page):
    session["user"] = "123"
    print "run 1"
    PER_PAGE = 5
    #Get all the tasks
    thesis = []
    for row in session_connect.query(Thesis).filter(Thesis.teachernum==session["user"]).all():
        thesis.append(row)
    print len(thesis)
    #Paginator    
    thesis_page = get_thesis_for_page(thesis,page,PER_PAGE,len(thesis))
    p = SimplePagination(page,PER_PAGE,len(thesis))
    return render_template("thesis_collect.html",pagination=p,thesis=thesis_page)
