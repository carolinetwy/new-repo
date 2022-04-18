from flask import Flask, redirect, render_template, request, session, flash
from flask_app import app
from flask_app.models.user import Users
from flask_app.models.recipe import Recipes
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

#List 4 visible route > invisible 

@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # validation starts here
    if not Users.validate_user(request.form):
        return redirect('/')
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        # "password": request.form["password"]
        "password": pw_hash
    }
    user_id = Users.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')


@app.route("/login", methods=["POST"])
def login():
    data = { "email" : request.form["email"] }
    user_email = Users.get_email(data)
    login_pw_hash = bcrypt.check_password_hash(user_email.password, 
                                            request.form['password'])

    if not user_email:
        flash("Invalid Login/Email")
        return redirect('/')
    if not login_pw_hash:
        flash("Invalid Login/Password")
        return redirect('/')
    session['user_id'] = user_email.id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("dashboard.html",id=Users.get_id(data), recipes=Recipes.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    

