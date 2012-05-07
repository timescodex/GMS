#usr/bin/python
import os

from flask import Flask,config,session,g,redirect,url_for,abort,render_template,flash,request,Blueprint

import sys
sys.path.append("..")
from models.database import User,Thesis
from models.database import session_connect as db_session
#from database import User   #import the orm user model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
thesis = Blueprint('thesis',__name__,template_folder='templates')
from werkzeug import secure_filename
from pymongo import Connection
import gridfs
from datetime import datetime

UPLOAD_FOLDER = './Thesis'
ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


                            
            


@thesis.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #print filename
            #put into mongodb GridFS
            db = Connection().thesis
            fs = gridfs.GridFS(db)
            thesis_id = session["user"]
            if fs.exists(thesis_id):
                file2 = fs.get(thesis_id)
                print file2.name

                fs.delete(thesis_id)
                fs.put(file,_id=thesis_id,filename=file.filename)
                pass
                #do something else
            else:
                a = fs.put(file,_id=thesis_id,filename=file.filename)
                file2 = fs.get(thesis_id)
                print file2.name
                print file2.upload_date
            
            if session["user"]:
                if session["role"]=="student":
                    print "run into upload"
                    thesispath = os.path.join(UPLOAD_FOLDER, filename)
                    thesisuptime=str(datetime.now())
                    thesis = Thesis(thesisname=filename,thesispath=thesispath,thesisuptime=thesisuptime,studentno=session["user"])
                    db_session.add(thesis)
                    db_session.commit()
                    #db_session 
            
            file.save(os.path.join(UPLOAD_FOLDER, filename))

    return render_template("upload.html")

@thesis.route("/showthesis",methods=['GET','POST'])
def showthesis():
    return render_template("showthesis.html") 

