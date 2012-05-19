from flask import Flask,render_template,request,Blueprint,session,redirect,url_for
st = Blueprint('st',__name__,template_folder='templates',static_folder='static')
import sys
sys.path.append("..")
from models.database import session_connect,Task,User
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

@st.route("/createtask",methods=['GET','POST'])
def createtask():
    #Login session judge:
    print session["user"]
    print session["role"]
    if session["role"]=="teacher":
        if session['user']: 
            if request.method == 'POST':
                taskname = request.form['taskname']
                taskcontent = request.form['content']
                if taskname:
                    print "run into taskname"
                    if taskcontent:
                        print session["user"]
                        user = session_connect.query(User).filter(User.num==session["user"]).first()
                        print user.name
                        task = Task(name = taskname,content = taskcontent,pub_teacher=session["user"],teachername=user.name)
                        session_connect.add(task)
                        session_connect.commit()
    else:
        pass
        #if the task for one teacher is less than 15 insert

    return render_template("createtask.html")

@st.route("/selecttask/",defaults={'page':1},methods=['GET','POST'])
@st.route("/selecttask/<int:page>")
def selecttask(page):
    
    content=None
    teacher=None

    print "select task",session['user']
    PER_PAGE = 4
    #Get all the tasks
    tasks = []
    for row in session_connect.query(Task).all():
        tasks.append(row)
 
    #Paginator    
    task_page = get_task_for_page(tasks,page,PER_PAGE,len(tasks))
    p = SimplePagination(page,PER_PAGE,len(tasks))
       
    if request.method == 'POST':
        content = request.form['what']
        teacher = request.form['who']
        server = xmlrpclib.ServerProxy('http://localhost:8001')
    if content and teacher:
           #search by content and teacher
        print content
        print teacher
       
    elif content:
        matches = server.search(content)
        #search by content
        tasks = []
        for mid in matches:
           task = session_connect.query(Task).filter(Task.id == mid).first()
           tasks.append(task)
    
    elif teacher:
       tasks = []
       for row in session_connect.query(Task).filter(Task.pub_teacher == teacher).all():
           tasks.append(row)
       #search by teacher
    else:
       #No search 
       pass
        
    task_page = get_task_for_page(tasks,page,PER_PAGE,len(tasks))
    p = SimplePagination(page,PER_PAGE,len(tasks))
     
    return render_template('selecttask.html',pagination=p,tasks=task_page)

@st.route("/showdetail/<int:tid>")
def showdetail(tid):
    #session["tid"] = tid
    print tid
    session["tid"] = tid
    task = session_connect.query(Task).filter(Task.id==tid).first()
    return render_template('showdetail.html',task=task)




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




#if __name__=="__main__":
#    st.run(debug=True)









