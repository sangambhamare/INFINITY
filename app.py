from flask import Flask, request, redirect, url_for, flash, session, render_template_string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Basic configuration
app.secret_key = "21038175e1ecaf5abba836607a163f20"  # Your session secret key
app.config['WTF_CSRF_SECRET_KEY'] = 'a_different_csrf_secret_key'  # CSRF secret key for Flask-WTF
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize CSRF protection and database
csrf = CSRFProtect(app)
db = SQLAlchemy(app)

# --------------------
# Database Model
# --------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# --------------------
# Inline Templates
# --------------------

login_template = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Login</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f2f2f2; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
    .container { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center; }
    input { width: 90%; padding: 10px; margin: 5px 0; }
    button { padding: 10px 20px; background: #007BFF; color: #fff; border: none; border-radius: 4px; cursor: pointer; }
    button:hover { background: #0056b3; }
    .flash { color: red; }
  </style>
</head>
<body>
  <div class="container">
    <h2>Login</h2>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="flash">
          {% for message in messages %}
            <p>{{ message }}</p>
          {% endfor %}
        </div>
      {% endif %}
    {% endwith %}
    <form method="POST">
      <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
      <input type="text" name="username" placeholder="Username" required><br>
      <input type="password" name="password" placeholder="Password" required><br>
      <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <a href="{{ url_for('register') }}">Register here</a></p>
  </div>
</body>
</html>
"""

register_template = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Register</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f2f2f2; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
    .container { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center; }
    input { width: 90%; padding: 10px; margin: 5px 0; }
    button { padding: 10px 20px; background: #28a745; color: #fff; border: none; border-radius: 4px; cursor: pointer; }
    button:hover { background: #218838; }
    .flash { color: red; }
  </style>
</head>
<body>
  <div class="container">
    <h2>Register</h2>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="flash">
          {% for message in messages %}
            <p>{{ message }}</p>
          {% endfor %}
        </div>
      {% endif %}
    {% endwith %}
    <form method="POST">
      <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
      <input type="text" name="username" placeholder="Username" required><br>
      <input type="password" name="password" placeholder="Password" required><br>
      <button type="submit">Register</button>
    </form>
    <p>Already have an account? <a href="{{ url_for('login') }}">Login here</a></p>
  </div>
</body>
</html>
"""

dashboard_template = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; background: #e9ecef; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
    .container { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center; }
    a { color: #007BFF; text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Dashboard</h1>
    <p>Welcome, {{ username }}!</p>
    <p><a href="{{ url_for('profile') }}">Edit Profile</a> | <a href="{{ url_for('logout') }}">Logout</a></p>
  </div>
</body>
</html>
"""

profile_template = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Profile</title>
  <style>
    body { font-family: Arial, sans-serif; background: #e9ecef; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
    .container { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center; }
    input { width: 90%; padding: 10px; margin: 5px 0; }
    button { padding: 10px 20px; background: #17a2b8; color: #fff; border: none; border-radius: 4px; cursor: pointer; }
    button:hover { background: #138496; }
    a { color: #007BFF; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .flash { color: red; }
  </style>
</head>
<body>
  <div class="container">
    <h2>Update Profile</h2>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="flash">
          {% for message in messages %}
            <p>{{ message }}</p>
          {% endfor %}
        </div>
      {% endif %}
    {% endwith %}
    <form method="POST">
      <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
      <input type="text" name="username" value="{{ username }}" placeholder="Username" required><br>
      <button type="submit">Update Profile</button>
    </form>
    <p><a href="{{ url_for('dashboard') }}">Back to Dashboard</a></p>
  </div>
</body>
</html>
"""

# --------------------
# Routes
# --------------------

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.")
    return render_template_string(login_template)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for('register'))
        
        # Create a new user and hash their password
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))
    return render_template_string(register_template)

@app.route("/dashboard")
def dashboard():
    if 'username' not in session:
        return redirect(url_for("login"))
    return render_template_string(dashboard_template, username=session['username'])

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if 'username' not in session:
        return redirect(url_for("login"))
    user = User.query.filter_by(username=session['username']).first()
    if request.method == "POST":
        new_username = request.form.get("username")
        # Check if the new username is taken by someone else
        if new_username != user.username and User.query.filter_by(username=new_username).first():
            flash("That username is already taken.")
        else:
            user.username = new_username
            db.session.commit()
            session['username'] = new_username  # Update session data
            flash("Profile updated successfully.")
            return redirect(url_for("profile"))
    return render_template_string(profile_template, username=user.username)

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out successfully.")
    return redirect(url_for("login"))

# --------------------
# Run the App
# --------------------
if __name__ == "__main__":
    app.run(debug=True)
