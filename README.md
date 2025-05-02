# Welcome to Paperlit

A powerful open-source platform for checking document originality and ensuring content integrity. Whether you're an educator, student, or researcher, Paperlit helps you maintain academic standards with ease.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusernameKytonThaundi/paperlit.git
    cd paperlit
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python src/app.py
    ```

## Database Setup

1. Install PostgreSQL:
    ```bash
    sudo apt update
    sudo apt install postgresql postgresql-contrib
    ```

2. Create the database and user:
    ```bash
    sudo -u postgres psql
    CREATE DATABASE paperlit;
    CREATE USER paperlit_user WITH PASSWORD 'securepassword';
    GRANT ALL PRIVILEGES ON DATABASE paperlit TO paperlit_user;
    \q
    ```

3. Configure the database in `app.py`:
    Update the `SQLALCHEMY_DATABASE_URI` in your Flask app:
    ```python
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://paperlit_user:securepassword@localhost/paperlit'
    ```

4. Install required Python packages:
    ```bash
    pip install flask-sqlalchemy psycopg2
    ```

5. Initialize the database:
    ```bash
    python app.py
    ```

## Usage

- Navigate to `http://127.0.0.1:5000/` to access the login page.
- Register a new user at `http://127.0.0.1:5000/register`.
- After logging in, you will be redirected to the home page.
- Logout by navigating to `http://127.0.0.1:5000/logout`.

## Error Handling

- A custom 404 error page is displayed when a page is not found.
- A custom 500 error page is displayed when an internal server error occurs.

## License

This project is licensed under the MIT License.

## Project Structure

```
/paperlit/
├── src/
│   ├── app.py                # Main Flask application
│   ├── models.py             # Database models (if separated)
│   ├── templates/            # HTML templates
│   │   ├── home.html         # Home page
│   │   ├── login.html        # Login page
│   │   ├── register.html     # Registration page
│   │   ├── edit_profile.html # Edit profile page
│   │   ├── 404.html          # Custom 404 error page
│   │   └── 500.html          # Custom 500 error page
│   ├── static/               # Static files (CSS, JS, images)
│   │   ├── home.css          # Styles for the home page
│   │   ├── login.css         # Styles for the login page
│   │   ├── images/           # Placeholder images and icons
│   │   │   └── avatar-placeholder.png
│   │   └── scripts.js        # JavaScript files
│   ├── config.py             # Configuration settings (e.g., database URI)
│   └── utils.py              # Utility functions (if applicable)
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore                # Git ignore file
└── venv/                     # Virtual environment (not included in Git)
```
