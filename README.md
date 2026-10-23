
# SecureVault — Web Security Findings Manager

SecureVault is a Python Flask web application for recording, tracking, and managing web security findings.

## Features

- Add and document security findings
- Categorize findings by severity
- Search findings by title
- Filter findings by severity
- View detailed vulnerability reports
- Track status: Open, In Progress, and Resolved
- Delete findings
- Store findings in an SQLite database

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML and CSS

## Installation

1. Clone this repository.
2. Open the project folder in the terminal.
3. Create and activate a virtual environment.
4. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

5. Run the application:

```bash
python app.py
```

6. Open `http://127.0.0.1:5000` in your browser.

## Security Note

This project is intended for local learning and portfolio demonstration. It is not production-ready. Authentication, CSRF protection, and production configuration must be addressed before deployment.

## Author

Cybersecurity learner interested in web application security and vulnerability assessment.
