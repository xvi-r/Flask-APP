import os
import pytz
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta, datetime
import external_api
import emailing
from models import db, Users, Streamers, TF2_Networks

if os.environ.get("FLASK_ENV") == "development":
    from dotenv import load_dotenv
    load_dotenv()
    # Use the SQLite URI for fast local dev (read from .env)
    DB_URI = os.environ.get("DATABASE_URI_LOCAL")

else:
    # Use the MySQL URI injected by DigitalOcean (read from DO settings)
    DB_URI = os.environ.get("DATABASE_URI")
    
    
bannedIPs = []

SPAIN_TIMEZONE = pytz.timezone("Europe/Madrid")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://doadmin:AVNS_77telqMtl1t0UktN45T@flask-user-mysql-db-do-user-28139050-0.d.db.ondigitalocean.com:25060/defaultdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

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
        #NOTE when you get back current code breaks when string NONE is returned if streamer is not live, add check to see if is_streamer_live() returned a dict or None
        streamer_to_check = Streamers.query.filter_by(username= streamerName).first()
        if not streamer_to_check:
            streamerData = external_api.is_streamer_live(streamerName, db=True)
        
            if streamerData != "🔴 NOT LIVE":
        
                print(streamerData["id"])
                
                if not streamerData:
                    live = False
                else:
                    live = True
                
                newStreamer = Streamers(username = streamerName, twitch_id = streamerData["id"], channel_link = f"https://twitch.tv/{streamerName}")
                db.session.add(newStreamer)
                db.session.commit()
                flash(f"Added {streamerData["user_name"]} To The Database")
            else:
                flash("Only online users can be added to the database")
    
        
    return render_template(
        "index.html", 
        curDate = datetime.now(SPAIN_TIMEZONE).strftime('%a %d %b %Y'),   #USES SPAIN TIMEZONE
        curTime = datetime.now(SPAIN_TIMEZONE).strftime('%I:%M%p'),
        seshTS = session.get("time_stamp"), 
        session = session,
        isLive = external_api.is_streamer_live(streamerName, db=False),
        streamerName = streamerName
    )
    
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        session.permanent = True

        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        session["time_stamp"] = datetime.now((SPAIN_TIMEZONE)).strftime('%a %d %b %Y, %I:%M%p')
        
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
            emailing.sendMail(name, email, "signed up admin email.txt")
            
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
        
        #TODO change later current test 
        currentUser = Users.query.filter_by(email = email, name = username).first()
        
        return render_template("userview.html", username = username, email = email, creationDate = currentUser.creationDate, is_admin = currentUser.is_admin)


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
    
    if "username" not in session:
        flash("You Must Be Logged In")
        return redirect(url_for("home"))
    
    if Users.query.filter_by(email = session.get("email"), is_admin=True).first() !=None:
            flash(f"Access Granted {session["username"]} is admin")
            return render_template("admin.html", userList=Users.query.all())
    else:
        flash("ERROR: User is not an admin")
        return redirect(url_for("home"))
    

@app.route("/emailMe", methods=["POST","GET"])
def emailMe():
    
    if request.method == "POST":
        userMsg = request.form.get("userMsg")
        emailing.sendMail(session["username"], session["email"], "email me.txt", userMsg)
        flash("Email sent!")
        return render_template("email Me.html")
    
    if "username" in session:
        return render_template("email Me.html")
    
    else:
        flash("You must be logged in")
    return redirect(url_for("home"))

#TODO rewrite with better logic later
@app.route("/tfnetworks", methods = ["POST", "GET"])
def tfnetworks():
    if request.method == "POST":
        networkName = request.form.get("networkName")
        networkID = request.form.get("networkID")
        creatorName = request.form.get("creatorName")
        
        #This will run if user searched via network ID
        if networkID:
            
            network = TF2_Networks.query.filter_by(id = networkID).all() #changed to return a list even if it's just one value
        
        
        #This will run if user searched via network name (This can be cleaned up but atm this is what i've thought off, might use a matchcase or better queries)
        elif networkName:
            search_term = f"%{networkName}%"
            
            network = TF2_Networks.query.filter(TF2_Networks.name.ilike(search_term)).all()
        
        else :
            search_term = f"%{creatorName}%"
            network = TF2_Networks.query.filter(TF2_Networks.creatorName.ilike(search_term)).all()
        
        print(network)
        
        if not network:
            print("HIT")
            flash(f"Inaccessible private network")
        else:
            return render_template("tfnetworks.html", networklist = network)
        
        
    return render_template("tfnetworks.html")

