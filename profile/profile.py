#!/usr/bin/python

from flask import Flask,config,session,g,redirect,url_for,abort,render_template,flash,request,Blueprint

import sys
sys.path.append("..")
from models.database import User
from models.database import session_connect as db_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


pf = Blueprint('pf',__name__,template_folder='templates')


@pf.route("/profile",methods=['GET','POST'])
def profile():
        if session['user']:
            if request.method=="POST":
                name = request.form["name"]
                email = request.form["email"]
                role = request.form["role"]
                cls = request.form["class"]
                grade = request.form["grade"]
                tel = request.form["tel"]
                passwd1 = request.form["password"]
                passwd2 = request.form["repassword"]
                if passwd1==passwd2:
                    user = db_session.query(User).filter(User.num==session["user"]).first()
                    user.name = name
                    user.passwd = passwd1
                    user.cls = cls
                    user.grd = grade
                    user.role = role
                    user.email = email
                    db_session.commit()
                    return redirect(url_for("app_login.firstpage"))
        return render_template("profile.html")



@pf.route("/showinfo/<userid>",methods=['GET','POST'])
def showinfo(userid):
    if userid:
        user = db_session.query(User).filter(User.num==userid).first()
        return render_template("showinfo.html",user=user)
    else:
        return redirect("app_login.firstpage")



