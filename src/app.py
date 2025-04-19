from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Home Route (Requires Login)
@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', username=session['user'])
    return redirect(url_for('login_register'))

# Combined Login and Registration Route
@app.route('/', methods=['GET', 'POST'])
def login_register():
    try:
        if request.method == 'POST':
            if 'login' in request.form:
                # Handle login
                username = request.form['username']
                password = request.form['password']
                user = User.query.filter_by(username=username).first()

                if user and check_password_hash(user.password, password):
                    session['user'] = username
                    flash('Login successful!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Invalid credentials. Please try again.', 'danger')

            elif 'register' in request.form:
                # Handle registration
                username = request.form['username']
                password = request.form['password']
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

                if User.query.filter_by(username=username).first():
                    flash('Username already exists. Please log in.', 'warning')
                    return redirect(url_for('login_register'))

                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login_register'))

        return render_template('login.html')
    except Exception as e:
        logging.error(f"Error during login or registration: {e}")
        return render_template('500.html'), 500

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login_register'))

# Error handling
@app.errorhandler(500)
def internal_error(error):
    logging.error(f"Server Error: {error}")
    return render_template('500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    logging.error(f"Page Not Found: {error}")
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
