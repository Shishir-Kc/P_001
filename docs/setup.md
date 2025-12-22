# Setup Guide

This guide provides detailed instructions on how to set up and run the **Shree Rastriya Secondary School** project locally.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Redis**: Required for Celery background tasks. [Install Redis](https://redis.io/docs/getting-started/)
- **Git**: [Download Git](https://git-scm.com/downloads)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Shishir-Kc/MAIN_PROJECT.git
cd MAIN_PROJECT
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory. You can use `.example.env` as a reference if it exists, or create one with the following keys (based on `settings.py`):

```ini
# Security
SECRET_KEY=your_secret_key_here
DEBUG=True

# Email Configuration (Gmail Example)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

> **Note:** For Gmail, you will need to generate an [App Password](https://support.google.com/accounts/answer/185833).

### 5. Database Setup

Apply the database migrations to set up the SQLite database:

```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)

To access the Django admin interface, create a superuser:

```bash
python manage.py createsuperuser
```

## Running the Application

### Start the Django Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

### Start Celery Worker (for Background Tasks)

Open a new terminal window, activate your virtual environment, and run:

**Linux/macOS:**
```bash
celery -A Shree_Rastriya_Secondary_School worker -l info
```

**Windows:**
```bash
celery -A Shree_Rastriya_Secondary_School worker -l info --pool=solo
```

### Start Celery Beat (for Periodic Tasks)

If the project uses periodic tasks (scheduled tasks), run Celery Beat in another terminal:

```bash
celery -A Shree_Rastriya_Secondary_School beat -l info
```
