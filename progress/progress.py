from flask import Flask,render_template,request,Blueprint,session,redirect,url_for
progress = Blueprint('progress',__name__,template_folder='templates',static_folder='static')
import sys
sys.path.append("..")
from models.database import session_connect,Task,User,Progress
from flaskext.sqlalchemy import Pagination
from math import ceil
import xmlrpclib

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



def get_task_for_page(tasks,page,PER_PAGE,count):
    #After get for the page 
    PER_PAGE = PER_PAGE
    if page >= 1:
        if page*PER_PAGE < count:
            begin = (page-1)*PER_PAGE
            end = PER_PAGE+begin
            for task in tasks[begin:end]:
                return tasks[begin:end]
        else:
            begin = (page-1)*PER_PAGE 
            end = count//page+begin 
            return tasks[begin:end]
    else:
        return None

@progress.route("/publish",methods=['GET','POST'])
def publish():
    #Login session judge:
    print session["user"]
    print session["role"]
    if session["role"]=="student":
        if session['user']: 
            if request.method == 'POST':
                progressname = request.form['name']
                progresscontent = request.form['content']
                if progressname:
                    print "run into progress"
                    if progresscontent:
                        print session["user"]
                        user = session_connect.query(User).filter(User.num==session["user"]).first()
                        print user.name
                        progress = Progress(name = progressname,content = progresscontent,studentnum=session["user"],studentname=user.name)
                        session_connect.add(progress)
                        session_connect.commit()
    else:
        pass
        #if the task for one teacher is less than 15 insert

    return render_template("progress_pub.html")

@progress.route("/showprogress/",defaults={'page':1},methods=['GET','POST'])
@progress.route("/showprogress/<int:page>")
def showprogress(page):
    if session["role"] == 'student':
        studentnum = session['user']
    else:
        studentnum = session["studentnum"]
    PER_PAGE = 4 
    #Get all the tasks
    progresses = []
    for row in session_connect.query(Progress).filter(Progress.studentnum==studentnum).all():
        progresses.append(row)
 
    #Paginator    
    progress_page = get_task_for_page(progresses,page,PER_PAGE,len(progresses))
    p = SimplePagination(page,PER_PAGE,len(progresses))
    return render_template('progress_show.html',pagination=p,progresses=progress_page)



@progress.route("/showdetail/<int:pid>")
def showdetail(pid):
    print pid
    session["pid"] = pid
    progress = session_connect.query(Progress).filter(Progress.id==pid).first()
    return render_template('progress_detail.html',progress=progress)



"""
@st.route("/confirmselect",methods=['GET','POST'])
def confirmselect():
    if session["tid"]:
        task = session_connect.query(Task).filter(Task.id==session["tid"]).first()
        task.select_student = session["user"]
        user = session_connect.query(User).filter(User.num==session["user"]).first()
        task.studentname = user.name
        #session_connect.add(task)
        session_connect.commit()
     
    return redirect(url_for("st.selecttask"))


@st.route("/delete",methods=['GET','POST'])
def delete():
    if session["tid"]:
        task = session_connect.query(Task).filter(Task.id==session["tid"]).first()
        session_connect.delete(task)
        session_connect.commit()

    return redirect(url_for("st.selecttask"))



@st.route("/edit",methods=['GET','POST'])
def edit():
    print session["tid"]
    print session["role"]
    if session["tid"]:
        task = session_connect.query(Task).filter(Task.id==session["tid"]).first()
        if session["role"]=="teacher":
            if session['user']:
                if request.method == 'POST':
                    taskname = request.form['taskname']
                    taskcontent = request.form['content']
                    if taskname:
                        print "run into taskname"
                        if taskcontent:
                            task.name = taskname
                            task.content = taskcontent
                            session_connect.commit() 
                            return redirect(url_for("st.edit"))

    return render_template("edit_task.html",task=task)

"""


#if __name__=="__main__":
#    st.run(debug=True)









