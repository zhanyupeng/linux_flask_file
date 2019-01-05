from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask import Flask,request,flash,session,url_for, make_response,redirect,abort,render_template
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLALchemy(app)

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


app.config['SECRET_KEY'] = 'hard to guess string'
class NameForm(Form):
    name = StringField('what is you name?', validators=[Required()])
    submit = SubmitField('submit')

#@app.route('/', methods=['GET','POST'])
#def index():
#    name = None
#    form = NameForm()
#    if form.validate_on_submit():
#        name = form.name.data
#        form.name.data = ''
#    return render_template('index.html', form=form, name=name)

#@app.route('/')
#def index():
    #response = make_response('<h1>This document carries a cookie</h1>')
    #response.set_cookie('answer', '42')
    #return response
    # return redirect('http://www.example.com')
   # return render_template('index.html')
#    return render_template('index.html',current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    #return '<h1>Hello, %s!</h1>' % name
    return render_template('user.html', name=name)



#@app.route('/user/<id>')
#def get_user(id):
#    user = load_user(id)
#    if not id:
#       abort(404)
#    return '<h1>Hello, %s</h1>' % user.name

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#@app.route('/', methods=['GET','POST'])
#def index():
#    form = NameForm()
#    if form.validate_on_submit():
#        session['name']= form.name.data
#        return redirect(url_for('index'))
#    return render_template('index.html',form=form, name=session.get('name'))

@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('looks like you have changed you name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',
            form = form, name = session.get('name'))

if __name__ == '__main__':
    app.run()

