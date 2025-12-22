# Architecture Overview

## Project Structure

The **Shree Rastriya Secondary School** project is a Django-based web application designed to manage school operations. It follows a modular architecture with separate apps for different functional areas.

### Core Components

- **`Shree_Rastriya_Secondary_School/`**: The main project configuration directory containing `settings.py`, `urls.py`, and WSGI/ASGI configurations.
- **`manage.py`**: The command-line utility for administrative tasks.

### Applications

The project is divided into several Django apps:

1.  **`login`**
    *   **Purpose**: Handles user authentication, registration, and login flows.
    *   **Key Features**: Custom login views, middleware for session management (`is_Loggedin`).

2.  **`Home`**
    *   **Purpose**: Manages the landing page and general site navigation.
    *   **Key Features**: Home page views, static content display.

3.  **`student`**
    *   **Purpose**: dedicated portal and functionality for students.
    *   **Key Features**: Student dashboard, profile management, academic records.

4.  **`teacher`**
    *   **Purpose**: Dedicated portal and functionality for teachers.
    *   **Key Features**: Teacher dashboard, class management, grading.

5.  **`school_admin`**
    *   **Purpose**: Administrative interface for school management.
    *   **Key Features**: User management, system configuration, high-level oversight.

6.  **`data_class`**
    *   **Purpose**: Manages data structures and models related to classes or academic data.

7.  **`u_task`**
    *   **Purpose**: Handles background tasks and asynchronous operations.
    *   **Key Features**: Celery task definitions, periodic tasks.

### Key Technologies

- **Backend Framework**: Django 5.2.7
- **Database**: SQLite (Default), extensible to PostgreSQL/MySQL.
- **Asynchronous Tasks**: Celery 5.6.0 with Redis broker.
- **Task Scheduling**: Celery Beat.
- **Environment Management**: `python-decouple` for `.env` file handling.

### User Roles

The system is designed with role-based access control (RBAC) in mind, supporting:
1.  **Head/Admin**: Full system access.
2.  **Teacher**: Access to class and student management.
3.  **Student**: Access to personal academic records and information.

### Background Processes

The application utilizes **Celery** for handling time-consuming tasks asynchronously, such as sending emails or processing large datasets. This ensures a responsive user interface.
