# ZFunds Django Project

Welcome to the ZFunds Django project! This project enables advisors and users to invest in various financial products through a user-friendly platform.

## Getting Started

These instructions will guide you through setting up and running the project on your local machine.

### Prerequisites

- Python (3.7+ recommended)
- pip (Python package manager)
- Virtual environment tool (e.g., `venv` or `virtualenv`)
- PostgreSQL (or another SQL database)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/zfunds-django.git
    cd zfunds
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your PostgreSQL database:
   
   - Create a database in PostgreSQL for your project.
   - Update the `DATABASES` configuration in `settings.py` with your database credentials.

5. Apply migrations to set up the database:

    ```bash
    python manage.py migrate
    ```

6. Create a superuser for the Django admin:

    ```bash
    python manage.py createsuperuser
    ```

7. Start the development server:

    ```bash
    python manage.py runserver
    ```

8. Access the Django admin at `http://127.0.0.1:8000/admin/` and log in using the superuser credentials.

## Usage

- Access the API endpoints at `http://127.0.0.1:8000/api/v1/` (assuming the default development server).

## Live Backend Access

You can access the live backend of the project on PythonAnywhere using the following URL:

- Base URL: `https://dhruv23.pythonanywhere.com/`
- API Endpoints: `https://dhruv23.pythonanywhere.com/api/v1/`
- Admin Access : `https://dhruv23.pythonanywhere.com/admin/`
- Admin credentials:
  - username : dhruv23 
  - password : dhruv