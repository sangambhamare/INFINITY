from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config

app = Flask(__name__, template_folder='.', static_folder='.')

app.config.from_object(Config)




# Dummy users for demonstration purposes (replace with database integration later)
users = {
    'user1': 'password1',
    'user2': 'password2'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Validate credentials
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Protect the dashboard route: only logged-in users can access it.
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
