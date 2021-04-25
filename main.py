import json
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask import Flask, request, render_template, redirect, flash, url_for
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 

from models import db, User, Item
from forms import SignUp, LogIn, AddItem


login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
  app.config['SECRET_KEY'] = "MYSECRET"
  login_manager.init_app(app)
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()
db.create_all(app=app)


@app.route('/', methods=['GET'])
def index():
  form = LogIn()
  return render_template('login.html', form=form)


#login route
@app.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit(): 
      data = request.form
      user = User.query.filter_by(username = data['username']).first()
      if user and user.check_password(data['password']): 
        flash('Logged in successfully.')
        login_user(user) 
        return redirect(url_for('home')) 
  return redirect(url_for('index'))


#signup route
@app.route('/signup', methods=['GET','POST'])
def signupAction():
    form = SignUp()
    if form.validate_on_submit():
        userdata = request.form 
        newuser = User(username=userdata['username'], email=userdata['email']) 
        newuser.set_password(userdata['password']) 
        db.session.add(newuser)
        db.session.commit() 

        flash('Account Created Successfully!')

        return redirect(url_for('index'))  

    return render_template('signup.html', form=form)
 

#login redirect route
@app.route('/login', methods=['GET','POST'])
def login():
    return redirect(url_for('index'))


#homepage route
@app.route('/HomePage', methods=['GET','POST'])
@login_required
def home():
    items = Item.query.filter_by(userid = current_user.id).all()
    if items is None:
        items = []
    form = AddItem()
    if form.validate_on_submit():
        data = request.form 
        newitem = Item(text=data['text'], done=False, userid=current_user.id) 
        db.session.add(newitem) 
        db.session.commit()
        flash('Item was added successfully') 
        return redirect(url_for('home')) 
    return render_template('HomePage.html', form=form, items=items) 


# Delete an entry from databade
@app.route('/remitem/<id>', methods=['GET'])
@login_required
def removeitem(id):
    item = Item.query.filter_by(userid=current_user.id, id=id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('HomePage.html')


# logout
@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('index')) 


app.run(host='0.0.0.0', port=8080, debug=True)