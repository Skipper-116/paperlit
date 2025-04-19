# Welcome to Paperlit

A powerful open-source platform for checking document originality and ensuring content integrity. Whether you're an educator, student, or researcher, Paperlit helps you maintain academic standards with ease.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/paperlit.git
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
    cd src
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
│   ├── app.py
│   └── templates/
│       ├── home.html
│       ├── login.html
│       ├── register.html
│       ├── 404.html
│       └── 500.html
├── README.md
```
