#!/usr/bin/python
from sqlalchemy import create_engine,Column,Integer,String,Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_engine = create_engine("mysql://root:123456@localhost/gms?charset=utf8",echo=True)
Base = declarative_base()

#define the tables:
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer,primary_key=True)
    name = Column(String(20))   #username
    num = Column(String(20))    #login username
    passwd = Column(String(20)) #password
    cls = Column(String(20))    #class
    grd = Column(String(20))    #grade
    role = Column(String(20))   #role student or teacher or admin
    tel = Column(String(20))    #telephone
    email = Column(String(40))  #email
    
    def __init__(self,name=None,num=None,passwd='123456',cls=None,grd=None,role=None,tel=None,email=None):
        #initialize the columns:
        self.name =  name
        self.num = num
        self.passwd =passwd
        self.cls = cls
        self.grd = grd
        self.role = role
        self.tel = tel
        self.email = email
    
    def __repr__(self):
        return "User:('%s','%s','%s','%s')",(self.name,self.num,self.cls,self.grd)

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer,primary_key=True)
    name = Column(String(100)) #task name
    content = Column(Text) #content of the task
    pub_teacher = Column(String(20)) #publish teacher No.
    select_student = Column(String(20)) #select the task student No.
    studentname = Column(String(20))
    teachername = Column(String(20))
    time = Column(String(100))

    def __init__(self,name=None,content=None,pub_teacher=None,select_student=None,studentname=None,teachername=None,time=None):
        self.name = name
        self.content = content
        self.pub_teacher = pub_teacher
        self.teachername = teachername
        self.select_student = select_student
        self.studentname = studentname
        self.time = time

class Thesis(Base):
    __tablename__ = 'thesis'

    id = Column(Integer,primary_key=True)
    thesisname = Column(String(100))
    thesispath = Column(String(250))
    thesisuptime = Column(String(100))
    studentno = Column(String(20))
    teacherno = Column(String(20))
    time = Column(String(100))

    def __init__(self,thesisname=None,thesispath=None,thesisuptime=None,studentno=None,teacherno=None,time=None):
        self.thesisname = thesisname
        self.thesispath = thesispath
        self.thesisuptime = thesisuptime
        self.studentno = studentno
        self.teacherno = teacherno
        self.time = time



class Marks(Base):
    __tablename__ = 'marks'
    id = Column(Integer,primary_key=True)
    studentnum = Column(String(20))
    teachernum = Column(String(20))
    #make it better later:
    trans_mark = Column(Integer)
    thesis_mark = Column(Integer)
    final_mark = Column(Integer)
    def __init__(self,studentnum=None,teachernum=None,trans_mark=None,thesis_mark=None,final_mark=None):
        self.studentnum = studentnum
        self.teachernum = teachernum
        self.trans_mark = trans_mark
        self.thesis_mark = thesis_mark
        self.final_mark = final_mark

class Progress(Base):
    __tablename__ = 'progress'
    id = Column(Integer,primary_key=True)
    studentnum = Column(String(20))
    teachernum = Column(String(20))
    studentname = Column(String(30))
    teachername = Column(String(30))
    name = Column(String(200))
    content = Column(Text)
    time = Column(String(100))

    def __init__(self,studentnum=None,studentname=None,teachernum=None,teachername=None,name=None,content=None):
        self.studentnum = studentnum
        self.studentname = studentname
        self.teachernum = teachernum
        self.teachername = teachername
        self.name = name
        self.content = content




#initialize the database
Base.metadata.create_all(db_engine)
#Test data
Session = sessionmaker(bind=db_engine)
session_connect = Session()
#test_user = User('liyang','200892465','123456','15','08','student','student','aiesecliyang.dalian@gmail.com')
#test_task = Task('Graduation management system')
#session_connect.add(test_user)
#session.add(test_task)
#session_connect.commit()
