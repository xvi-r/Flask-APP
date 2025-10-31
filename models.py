from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# --- Users Table ---
class Users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # NOTE Hashes tend to be long better to use 255 chars
    
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
        return f"User: ID:{self._id}, Name: {self.name} Email:{self.email}"


# --- Streamers Table ---
class Streamers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    twitch_id = db.Column(db.String(50), unique=True, nullable=True)
    date_added = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    channel_link = db.Column(db.String(100), unique=True, nullable=True)

    def __repr__(self):
        return f"ID: {self.id} Streamer: {self.username}, TwitchID: {self.twitch_id}, Date Added: {self.date_added}, Channel Link: {self.channel_link}"
    
    
    
# --- Titanfall Networks Table ---
class TF2_Networks(db.Model):
    __tablename__ = "TF2_Networks" #Avoid auto table name creation
     
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    clantag = db.Column(db.String(100), nullable=True)
    motd = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    type = db.Column(db.String(100), nullable=True)
    visibility = db.Column(db.String(100), nullable=True)
    regions = db.Column(db.String(255), nullable=True)
    languages = db.Column(db.String(100), nullable=True)
    utcHappyHourStart = db.Column(db.Integer, nullable=True)
    happyHourStart = db.Column(db.Integer, nullable=True)
    creatorUID = db.Column(db.Integer, nullable=True)
    creatorName = db.Column(db.String(100), nullable=True)
    kills  = db.Column(db.Integer, nullable=True)
    wins = db.Column(db.Integer, nullable=True)
    xp = db.Column(db.Integer, nullable=True)
    memberCount = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return (
            f"TF2_Networks(id={self.id}, name={repr(self.name)}, clantag={repr(self.clantag)}, motd={repr(self.motd)}, "
            f"category={repr(self.category)}, type={repr(self.type)}, visibility={repr(self.visibility)}, "
            f"regions={repr(self.regions)}, languages={repr(self.languages)}, utcHappyHourStart={self.utcHappyHourStart}, "
            f"happyHourStart={self.happyHourStart}, creatorUID={self.creatorUID}, creatorName={repr(self.creatorName)}, "
            f"kills={self.kills}, wins={self.wins}, xp={self.xp}, memberCount={self.memberCount})"
        )

