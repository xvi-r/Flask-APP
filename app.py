import os
from dotenv import load_dotenv
# FORCING REBUILD: Fix database URI
from flask import Flask, redirect, url_for, render_template, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
import twitchGet
import emailing
import pymysql

load_dotenv()

adminUsers = os.environ.get("ADMIN_USERS")
bannedIPs = []


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Users(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    ip = db.Column(db.String(100), nullable = False)
    password_hash = db.Column(db.String(255), nullable = False) #NOTE Hashes tend to be long better to use 255 chars
    
    def __init__(self, name, email, ip, password):
        self.name = name
        self.email = email
        self.ip = ip
        self.password_hash = generate_password_hash(password)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @password.setter
    def password(self, plain_text_password):
        print("Hashing and storing the password securely...")
        self._password_hash = generate_password_hash(plain_text_password)
        
    def __repr__(self):
        return f"User: ID:{self.id}, Name: {self.name} Email:{self.email}"

# For getting real ip
def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        ip = request.headers.get("X-Forwarded-For").split(",")[0].strip()
    else:
        ip = request.remote_addr
    return ip    
    
    
@app.before_request
def block_banned_ips():
    if request.path.startswith('/static/'):
        return
    
    if get_client_ip() in bannedIPs:
        return render_template("banned.html")
    
@app.route("/", methods=["POST","GET"])
def home():
    streamerName = ""
    if request.method == "POST":
        if "username" not in session:
            flash("You need to be logged in to target")
            return redirect(url_for("home"))
        
        streamerName = request.form.get("streamerName")
    
        
    return render_template(
        "index.html", 
        curDate = datetime.now().strftime('%a %d %b %Y'),
        curTime = datetime.now().strftime('%I:%M%p'),
        seshTS = session.get("time_stamp"), 
        session = session,
        isLive = twitchGet.is_streamer_live(streamerName),
        streamerName = streamerName
    )
    
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        session.permanent = True

        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        user_to_check = Users.query.filter_by(name = name, email = email).first()
        
        if user_to_check:
            if user_to_check.verify_password(password):
                flash("Logged in")
                session["username"] = name
                session["email"] = email
                
                return redirect(url_for("home"))
            else:
                flash("Password is incorrect")
                return redirect(url_for("login"))
        else:
            flash("no user with such name/email exists")
            return redirect(url_for("login"))

    return render_template("login.html")
    
    
@app.route("/signup", methods=["GET","POST"])
def signup():
    
    if request.method == "POST":
        
        name = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        
        ip =  get_client_ip()
        
        Name_User = Users.query.filter_by(name = name).first()
        Email_User = Users.query.filter_by(email = email).first()
        
        if not Name_User and not Email_User:
            new_user = Users(name=name, email=email, ip=ip, password = password)
            db.session.add(new_user)
            db.session.commit()
            flash(f"Account Successfully created!")
            session["time_stamp"] = datetime.now().strftime('%a %d %b %Y, %I:%M%p')
            emailing.sendMail("refractxvi@gmail.com", f"New User Signed Up", name, email)
            
        elif Name_User:
            flash("User with that name already exists")
            return redirect(url_for("signup"))
        elif Email_User:
            flash("User with that email already exists")
            return redirect(url_for("signup"))
        
        
        return redirect(url_for("home"))
        
    return render_template("signup.html")
    

@app.route("/userview")
def userview():
    if "username" not in session:
        flash("You are not logged in")
        return redirect(url_for("home"))
    else:
        username = session.get("username")
        email = session.get("email")
        return render_template("userview.html", username = username, email = email )


@app.route("/logout")
def logout():
    session.clear()
    flash("User logged out")
    return redirect(url_for('home'))

@app.route("/admin", methods=["POST","GET"])
def admin():
    if request.method == "POST":
        user_to_ban = request.form.get("userBAN")
        if user_to_ban:
            bannedIPs.append(user_to_ban)
            flash(f"IP/User {user_to_ban} has been banned!")
            flash(f"Banned Ips: {bannedIPs}")
            return redirect(url_for("admin"))
        
        email_to_kick = email=request.form.get("emailKick")
        user_to_kick =  Users.query.filter_by(email = email_to_kick).first()
        
        if user_to_kick == None:
            flash("COULDN'T FIND USER: INVALID EMAIL")
            return redirect(url_for("admin"))
        
        db.session.delete(user_to_kick)
        db.session.commit()
        
        flash("USER DELETED")
        
        
    if session.get("username") in adminUsers:
        if not get_client_ip().startswith("192.168."):
            flash("ERROR USER IS NOT ON ADMIN NETWORK")
            return redirect(url_for("home"))
        
        flash(f"Access Granted {session["username"]} is admin")
        return render_template("admin.html", userList=Users.query.all())
    else:
        flash("ERROR: User is not an admin")
        return redirect(url_for("home"))


@app.route("/emailMe")
def emailMe():
    emailing.sendMail(session["email"], "From Web")
    flash(f"Email sent to {session["email"]}")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)