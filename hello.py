import os
from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask import session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager 
from flask_script import Shell  
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail

app=Flask(__name__)

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY']='hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
# app.config['MAIL_SERVER']='smtp.qq.com'
# app.config['MAIL_PORT']=25
# app.config['MAIL_USE_TLS']=True
# app.config['MAIL_USERNAME']='1546331221@qq.com'
# app.config['MAIL_PASSWORD']='plusone19941212'

bootstrap=Bootstrap(app)
moment=Moment(app)
db=SQLAlchemy(app)
manager=Manager(app)
migrate=Migrate(app, db)
mail=Mail(app)

manager.add_command('db', MigrateCommand)

class NameForm(Form):
    name=StringField('What is your name?', validators=[Required()])
    submit=SubmitField('Submit')
    
class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(64), unique=True)
    users=db.relationship('User', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return '<Role %r>' % self.name
        
class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(64), unique=True, index=True)
    role_id=db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/', methods=['GET', 'POST'])
def index():
    # user_agent=request.headers.get('User-Agent')
    # return '<p>Your browser is %s</p>' % user_agent
    # response=make_response('<h1>This document carries a cookie!</h1>')
    # response.set_cookie('answer','42')
    # return response
    # return redirect('http://www.baidu.com')
    
    mydict={'key':'mao','key2':'jiayi'}  
    #name=None
    form=NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
            session['known']=False
        else:
            session['known']=True
        
        # old_name=session.get('name')
        # if old_name is not None and old_name != form.name.data:
            # flash('Looks like you have changed your name!')
            
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html', mydict=mydict, current_time=datetime.utcnow(), 
        form=form, name=session.get('name'), known=session.get('known', False))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name1=name)
    
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
    
@app.errorhandler(404)     
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

if __name__=='__main__':
    #app.run(debug=True)
    manager.run()
    
    
    
    
    
    
    
    
    
    
   