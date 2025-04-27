from flask import Flask, render_template, redirect, url_for, request, flash, session, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import os
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# PostgreSQL database configuration
# Ensure the password is URL-encoded if it contains special characters like '#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:deploy123%23@localhost/paperlit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload folder configuration
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# User model (maps to the existing 'users' table in the database)
class User(db.Model):
    __tablename__ = 'users'  # Explicitly map to the existing 'users' table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    documents = db.relationship('Document', backref='user', lazy=True)  # Relationship to Document

# Document model (maps to the 'documents' table in the database)
class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    document_name = db.Column(db.String(255), nullable=False)  # Ensure this matches the database
    file_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Home Route (Requires Login)
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login_register'))

    user_id = session['user_id']
    documents = Document.query.filter_by(user_id=user_id).all()
    return render_template('home.html', username=session['user'], documents=documents)

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
                    session['user_id'] = user.id  # Store user_id in session
                    flash('Login successful!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Invalid credentials. Please try again.', 'danger')

            elif 'register' in request.form:
                # Handle registration
                username = request.form['username']
                email = request.form['email']
                password = request.form['password']
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

                if User.query.filter_by(username=username).first():
                    flash('Username already exists. Please log in.', 'warning')
                    return redirect(url_for('login_register'))

                if User.query.filter_by(email=email).first():
                    flash('Email already exists. Please log in.', 'warning')
                    return redirect(url_for('login_register'))

                new_user = User(username=username, email=email, password=hashed_password)
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
    session.pop('user_id', None)  # Remove user_id from session
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login_register'))

# Upload Document Route
@app.route('/upload_document', methods=['POST'])
def upload_document():
    if 'user' not in session or 'user_id' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login_register'))

    try:
        # Get the uploaded file and document name
        document_name = request.form.get('document_name')
        document_file = request.files.get('document_file')

        if not document_name or not document_file:
            flash('Both document name and file are required.', 'warning')
            return redirect(url_for('home'))

        # Secure the filename and save the file
        filename = secure_filename(document_file.filename)
        user_id = session['user_id']  # Use user_id from session
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        document_file.save(save_path)

        # Save metadata to the database
        new_document = Document(
            user_id=user_id,
            document_name=document_name,
            file_path=save_path
        )
        db.session.add(new_document)
        db.session.commit()

        flash('Document uploaded successfully!', 'success')
        return redirect(url_for('home'))

    except Exception as e:
        logging.error(f"Error uploading document: {e}")
        flash('An error occurred while uploading the document.', 'danger')
        return redirect(url_for('home'))

# Download Document Route
@app.route('/download_document/<int:document_id>')
def download_document(document_id):
    if 'user' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login_register'))

    document = Document.query.filter_by(id=document_id, user_id=session['user_id']).first()
    if not document:
        flash('Document not found or access denied.', 'danger')
        return redirect(url_for('home'))

    return send_file(document.file_path, as_attachment=True)

# Edit Profile Route
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login_register'))

    if request.method == 'POST':
        # Handle profile update logic here
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('edit_profile.html')

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
