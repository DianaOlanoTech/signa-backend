# Signa IP - Technical Test (Backend API)

This repository contains the backend RESTful API for the Signa IP technical test. It is a robust and scalable application built with FastAPI to manage trademark records, providing complete CRUD (Create, Read, Update, Delete) functionality.

The application is designed to be run locally with SQLite for ease of development and is deployed using a managed PostgreSQL database on Render for production-level persistence and reliability.

## Key Features

- **Modern Tech Stack**: Built with FastAPI, Pydantic, and SQLAlchemy 2.0.
- **Paginated Responses**: The main listing endpoint is paginated to efficiently handle large datasets.
- **Database Migrations**: Uses Alembic to manage database schema changes in a controlled and versioned manner.
- **Dual Database Support**: Seamlessly works with SQLite for local development and PostgreSQL for production.
- **Dependency Injection**: Leverages FastAPI's dependency injection system for clean and testable code.
- **Automated Deployment**: Configured for continuous deployment on platforms like Render.

## Technologies Used

- **FastAPI**: A modern, high-performance Python web framework for building APIs.
- **Uvicorn**: An ASGI server used to run the FastAPI application.
- **SQLAlchemy**: The primary ORM for interacting with the database.
- **Alembic**: A database migration tool for version controlling the database schema.
- **Pydantic**: Used for data validation and defining the API's data schemas.
- **PostgreSQL**: The database used for the production deployment (via `psycopg2-binary`).
- **SQLite**: The database used for local development.

## API Endpoints

The API provides the following endpoints for managing trademark records.

**Base URL**: `https://signa-backend-q1y2.onrender.com/api/v1/trademarks`

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Retrieves a paginated list of all trademark records. Returns an object containing the `data` for the current page and the `total` record count. |
| `GET` | `/{id}` | Retrieves a specific trademark record by its ID. |
| `POST` | `/` | Creates a new trademark record. |
| `PUT` | `/{id}`| Updates an existing trademark record by its ID. |
| `DELETE`| `/{id}`| Deletes a trademark record by its ID. |

## Local Development Setup

Follow these instructions to get the backend running on your local machine.

### Prerequisites

- Python 3.10 or higher
- `pip` package manager

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/DianaOlanoTech/signa-backend.git
    cd signa-backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create your local environment file by copying the example template.
    ```bash
    # For Windows
    copy .env.example .env

    # For macOS/Linux
    cp .env.example .env
    ```
    *(The default `.env` is already configured for SQLite, so no changes are needed to get started).*

5.  **Initialize the database:**
    Run the Alembic migrations to create the `trademarks.db` file and the necessary tables inside the `signa-backend` directory.
    ```bash
    alembic upgrade head
    ```

6.  **(Optional) Load sample data:**
    You can populate the database with a sample dataset by running the provided script. This script is safe to run multiple times.
    ```bash
    python scripts/load_initial_data.py
    ```

### Running the Application

To start the development server, run the following command from the `signa-backend` directory:

```bash
uvicorn src.main:app --reload
```

- The API will be available at http://12- 7.0.0.1:8000.
- You can access the interactive API documentation (Swagger UI) at http://127.0.0.1:8000/docs.

## Deployment (Render):
   - This application is configured for deployment on Render.
   - The render.yaml file (if included) or the manual service configuration uses the DATABASE_URL provided by a managed PostgreSQL service.
   - The Build Command (pip install ... && alembic upgrade head) ensures the database schema is always up-to-date with each deployment.
   - Data Seeding: For the purpose of this technical test, the load_initial_data.py script is included in the build command to ensure the application is populated with sample data upon
   deployment. In a real-world production environment, this step would be removed to ensure user data persistence.
