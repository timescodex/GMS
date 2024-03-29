#!usr/bin/python

from flask import Flask,config,session,g,redirect,url_for,abort,render_template,flash,request,Blueprint

import sys
sys.path.append("..")
from models.database import User
from models.database import session_connect as db_session
#from database import User   #import the orm user model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app_login = Blueprint('app_login',__name__,template_folder='templates')

#app_login.config.from_envvar('gms_settings')
#app_login = Flask(__name__)

@app_login.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        login_num = request.form['num']
        password = request.form['passwd']
        print login_num
        print password
        if login_num:
            login_user = db_session.query(User).filter_by(num=login_num).first()
            if login_user:
                #get the password for login_num:
                if password == login_user.passwd:
                    session["user"] = login_user.num
                    session["role"] = login_user.role
                    print session['role']
                    flash("login Succeed")
                    return redirect(url_for('app_login.firstpage'))
                else:
                    error = "invalid password"
            else:
                error = 'invalid user'
    return render_template('login.html',error=error) 


@app_login.route('/firstpage')
def firstpage():
    return render_template("firstpage.html")


@app_login.route('/hello')
def hello(): #Test
    print session["user"]
    return render_template('hello.html',user=session["user"])

@app_login.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('app_login.login'))
    

#if __name__ == '__main__':
#   app.run(debug=True)

