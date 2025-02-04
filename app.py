from flask import Flask, request, redirect, url_for, flash, session, render_template_string

app = Flask(__name__)
app.secret_key = "21038175e1ecaf5abba836607a163f20"

# Dummy user data: Replace with a database or a secure storage for production.
allowed_users = {
    "user1": "password1",
    "user2": "password2"
}

# Inline HTML template with embedded CSS and JavaScript
login_template = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Interactive Login Page</title>
  <style>
    /* CSS for styling the login page */
    body {
      font-family: Arial, sans-serif;
      background: #f2f2f2;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
    }
    .login-container {
      background: #fff;
      padding: 30px 40px;
      border-radius: 8px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
      width: 320px;
      text-align: center;
    }
    h2 {
      margin-bottom: 20px;
    }
    .input-group {
      position: relative;
      margin-bottom: 20px;
    }
    .input-group input {
      width: 100%;
      padding: 12px 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
      outline: none;
      transition: border-color 0.3s;
    }
    .input-group input:focus {
      border-color: #007BFF;
    }
    .input-group label {
      position: absolute;
      top: 12px;
      left: 12px;
      color: #aaa;
      pointer-events: none;
      transition: all 0.2s ease-out;
    }
    .input-group input:focus + label,
    .input-group input:not(:placeholder-shown) + label {
      top: -10px;
      left: 8px;
      font-size: 12px;
      background: #fff;
      padding: 0 4px;
      color: #007BFF;
    }
    button {
      width: 100%;
      padding: 12px;
      background: #007BFF;
      color: #fff;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      transition: background 0.3s;
    }
    button:hover {
      background: #0056b3;
    }
    .flash-messages {
      list-style: none;
      padding: 0;
      margin-bottom: 10px;
      color: red;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="login-container">
    <h2>Login</h2>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul class="flash-messages">
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    <form method="POST">
      <div class="input-group">
        <input type="text" name="username" required placeholder=" ">
        <label for="username">Username</label>
      </div>
      <div class="input-group">
        <input type="password" name="password" required placeholder=" ">
        <label for="password">Password</label>
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
  <script>
    // JavaScript to enhance interactivity
    document.addEventListener("DOMContentLoaded", function() {
      console.log("Interactive Login Page Loaded");
    });
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Retrieve username and password from the form
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Check against our dummy user data
        if username in allowed_users and allowed_users[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.")
    
    # Render the inline template
    return render_template_string(login_template)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return f"""
    <h1>Dashboard</h1>
    <p>Welcome, {session['user']}!</p>
    <p><a href="{url_for('logout')}">Logout</a></p>
    """

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
