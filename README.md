# Flask Hello App

Hi! This is a web app I built using Python and Flask. It's my first real web app and I'm pretty proud of it. Here's what it does and how to run it yourself.

---

## What is this?

This app lets you create an account, log in, and then submit your name and mood. Based on what you pick, it gives you a personalised greeting — like if it's morning it says "Good Morning", and if you're hungry it says "Time for makan! 🍜". Every time you submit, it saves your entry so you can look back at your visit history later.

It also tracks how many times you've visited and shows your last 5 submissions on the greeting page, and a full history page where you can see all your past moods too.

---

## What I used to build it

- **Python + Flask** — this is the main framework that runs the app
- **SQLite + Flask-SQLAlchemy** — this is the database that saves users and visits as a simple file called `app.db`
- **Werkzeug** — this handles passwords safely by scrambling them before saving (so even I can't read your password)

---

## How to run it on your computer

1. Download or clone this project
2. Open a terminal in the project folder
3. Install what you need:

pip install flask flask-sqlalchemy werkzeug

4. Start the app:

5. Open your browser and go to `http://127.0.0.1:5000`

The database file creates itself automatically so you don't need to set anything up!

---

## A few things to know

- You need to register an account before you can use the hello form
- Passwords are never saved as plain text, they get scrambled for safety
- The app is set to Singapore time (SGT) so the greetings match the right time of day
- Please don't put this online as-is — the secret key needs to be changed first and debug mode should be turned off

