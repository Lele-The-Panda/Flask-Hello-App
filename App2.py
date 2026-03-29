from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import random
import os

app = Flask(__name__)
visit_count = 0
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


name_history = []
greetings = [
    "Nice to meet you!",
    "Welcome!",
    "Greetings! :)",
    "你好, Welcome :D",
    "Vanakkam!",
    "Hai!"
]

# Models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    mood = db.Column(db.String(20), nullable=False, default = "happy")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


def time_based_greeting():
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 18:
        return "Good Afternoon"
    elif 18 <= hour < 23:
        return "Good Evening"
    else:
        return "Late at Night?"

with app.app_context():
    db.create_all()

# @app.get("/init-db")
# def init_db():
#     db.create_all()
#     return "DB initialized."

@app.get("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "")
        password = request.form.get("password") or ""

        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for("register"))

        if len(username) > 80:
            flash ("Username too long.")
            return redirect(url_for("register"))

        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for("register"))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return redirect(url_for("index"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip().lower()
        password = (request.form.get("password") or "")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            return redirect(url_for("index"))

        flash("Invalid credentials.")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))

@app.post("/hello")
def hello():
    global visit_count, name_history
    visit_count += 1
    name = request.form.get("name", "Stranger")
    mood = request.form.get("mood")
    name_history.append(name)
    name_history = name_history[-3:]
    greeting = f"{time_based_greeting()}! {random.choice(greetings)}"

    if mood == "happy":
        response = "Time for a fun day! :)"
    elif mood == "excited":
        response = "Wanna fly? hehehe..."
    elif mood == "sleepy":
        response = "Go sleep! Stop playing on your device! :<"
    else:
        response = "Go eat then..."

    return render_template("hello lol.html", 
                           name=name, 
                           count=visit_count, 
                           greeting=greeting, 
                           history=name_history, 
                           response=response
)

def login_required(f):
    @wraps(f)
    def wrapper (*args, **kwargs):
        if"user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

@app.context_processor
def inject_user():
    user = None
    if "user_id" in session:
        user = User.query.get(session["user_id"])
    return dict(current_user=user)

if __name__ == "__main__":
    app.run(debug=True)