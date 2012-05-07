from flaskext.wtf import Form, TextField, Required
from flask import Flask,render_template

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

class MyForm(Form):
    name = TextField("name", validators=[Required()])
    number = TextField("number")


@app.route('/form',methods=['GET','POST'])
def profile_form():
    profile_form = MyForm()
    return render_template('form.html',form=profile_form)


    

if __name__=="__main__":
    app.run(debug=True)

