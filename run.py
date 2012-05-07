from flask import Flask,session,request,url_for
from login.login import app_login
from task.task import st
from profile.profile import pf
from thesis.thesis import thesis
from marks.marks import marks
from progress.progress import progress
app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config.from_envvar("gms_settings")
app.register_blueprint(app_login,url_prefix='/lg')
app.register_blueprint(st,url_prefix='/st')
app.register_blueprint(pf,url_prefix='/pf')
app.register_blueprint(thesis,url_prefix='/thesis')
app.register_blueprint(marks,url_prefix='/marks')
app.register_blueprint(progress,url_prefix='/progress')
def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


print app.url_map
app.run(debug=True)
