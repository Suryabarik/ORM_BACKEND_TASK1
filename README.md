# Steps to Run the Django Project

This guide explains how to set up and run the Django project locally.

## Prerequisites

- Python 3.8 or higher
- Django 5.1.4 or higher
- pip (Python package installer)
- Virtual environment tool (optional but recommended)

## Steps to Set Up and Run the Project

### 1. Clone the Repository

Clone the repository from GitHub:
```bash
git clone <repository-url>
```

Navigate to the project directory:
```bash
cd orm_backend/orm/companyapi
```

### 2. Set Up a Virtual Environment (Optional)

Create a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 4. Delete Migration Files

Navigate to the `migrations` folder inside the `api` app and delete all files except `__init__.py`:
```bash
cd api/migrations
rm -f *.py
```
Ensure that `__init__.py` remains in the folder.

### 5. Apply Migrations

Create and apply the database migrations:
```bash
python manage.py makemigrations api
python manage.py migrate api
```

### 6. Run the Development Server

Start the Django development server:
```bash
python manage.py runserver
```

Access the application at:
```
http://127.0.0.1:8000/
```

### 7. Quit the Server

To stop the server, press `CTRL-BREAK` (Windows) or `CTRL-C` (Mac/Linux).

## Notes

- Ensure you have the correct database settings configured in `settings.py`.
- Use a virtual environment to avoid dependency conflicts.
- For production, set up a proper web server and database.

Happy Coding!
