from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, game
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

#login/registration page 
@app.route("/")
def index():
    return render_template("login.html")

# /dashboard- shows everyone's game - but you must be logged in 
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("dashboard.html", user = user.User.get_by_id(data), all_games = game.Game.get_all_games_with_users())

@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("home.html")

# /register
@app.route("/register_form")
def register_form():
    return render_template("register.html")

# /register database
@app.route("/register", methods=["POST"])
def register():
    if not user.User.validate_registration(request.form):
        return redirect("/")
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    session["user_id"] = user.User.register_user(data) 
    return redirect("/dashboard")

@app.route("/login_form")
def login_form():
    return render_template("login.html")

# /login 
@app.route("/login", methods=["POST"])
def login():
    if not user.User.validate_login(request.form):
        return redirect("/")
    data = {
        "email": request.form["email"]
    }
    logged_in_user = user.User.get_by_email(data)
    session["user_id"] = logged_in_user.id
    return redirect("/dashboard")

# /logout 
@app.route("/logout")
def logout():
    session.clear() 
    return redirect("/")