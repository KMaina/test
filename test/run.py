from flask import Flask, render_template, request, url_for, redirect, session

from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email

from flask.ext.bcrypt import Bcrypt


app = Flask(__name__)
db = SQLAlchemy(app)
flask_bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:home1234@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'keniscoolobviously'

class Name(db.Model):

    __tablename__ = 'names'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    #admin = db.Column(db.String(11), nullable=False)
    
    def __init__(self, name, password):
        self.name = name
        self.password = password
        #self.admin = admin

    def __rep__(self):
        return '<User %r>' % self.username

class Organization(db.Model):

    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    address = db.Column(db.String(45))
    telephone = db.Column(db.String(45))
    pin = db.Column(db.String(45))
    vat = db.Column(db.String(45))

class LoginForm(FlaskForm):
    username = StringField(label = 'username', validators = [InputRequired('Username is required.')])
    password = PasswordField(label = 'password', validators = [InputRequired('Password is required.')])

class SettingsForm(FlaskForm):
    oname = StringField(label = 'ORGANIZATION NAME', validators = [InputRequired('An Organization Name Is Required')])
    email = StringField(label='EMAIL', validators = [InputRequired('An Email Is Required'), Email('This Is Not A Valid Email Address')])
    address = StringField(label = 'ADDRESS')
    tel = StringField(label = 'TELEPHONE', validators = [InputRequired('A Telephone Number Is Required')])
    PIN = StringField(label = 'PIN')
    VAT = StringField(label= 'VAT')

class AddUser(FlaskForm):
    name = StringField(label= 'username', validators = [InputRequired('Username is required')])
    password = StringField(label = 'password', validators = [InputRequired('Password is required')])
    #admin = BooleanField('Admin')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit:
        user = Name.query.filter_by(name=form.username.data).first()
        password = Name.query.filter_by(password=form.password.data).first()
        if user  and password:
            session['username'] = form.username.data
            return redirect(url_for('home'))
        else:
            return 'Error'

    else:
        return render_template('index.html', form=form)  

@app.route('/home')
def home():
    return render_template('home.html')   

@app.route('/settings')
def settings():
    settingsform = SettingsForm()
    return render_template('settings.html', settingsform=settingsform)     

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/manage-users')
def manage_users():
    infos = Name.query.all()
    return render_template('manage-users.html', infos=infos)

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/add_user', methods=['GET','POST'])
def add_user():
    form = AddUser()

    if request.method == 'POST' and form.validate_on_submit():
        print form.name.data
        user = Name(name=form.name.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return render_template('add-user.html')
          
    else:
        return render_template('add-user.html', form=form)

@app.route('/delete_user')
def delete_user():
    names = Name.query.all()
    return render_template('delete-user.html', names=names)
    
if __name__ == '__main__':
    app.run(debug=True)