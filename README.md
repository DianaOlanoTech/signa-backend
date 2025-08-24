# Signa IP - Technical Test (Backend API)

This repository contains the backend RESTful API for the Signa IP technical test. It is a robust and scalable application built with FastAPI to manage trademark records, providing complete CRUD (Create, Read, Update, Delete) functionality.

## Technologies Used

- **FastAPI**: A modern, high-performance Python web framework for building APIs.
- **Uvicorn**: An ASGI server used to run the FastAPI application.
- **SQLAlchemy**: The primary ORM for interacting with the database, managing models and queries.
- **Alembic**: A database migration tool for version controlling the database schema.
- **Pydantic**: Used for data validation and defining the API's data schemas.
- **SQLite**: The database used for local storage and deployment.

## API Endpoints

The API provides the following endpoints for managing trademark records.

**Base URL**: `[Your Deployed API URL]/api/v1/trademarks`

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Retrieves a paginated list of all trademark records. Returns an object containing the `data` for the current page and the `total` record count. |
| `GET` | `/{id}` | Retrieves a specific trademark record by its ID. |
| `POST` | `/` | Creates a new trademark record. |
| `PUT` | `/{id}`| Updates an existing trademark record by its ID. |
| `DELETE`| `/{id}`| Deletes a trademark record by its ID. |

## Getting Started (Local Setup)

Follow these instructions to get the backend running on your local machine.

### Prerequisites

- Python 3.10 or higher
- `pip` package manager

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/DianaOlanoTech/signa-backend.git
    cd signa_backend
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
    Copy the example environment file to create your local configuration.
    ```bash
    copy .env.example .env
    ```
    *(No changes are needed in `.env` for local SQLite setup).*

5.  **Initialize the database:**
    Run the Alembic migrations to create the `trademarks.db` file and the necessary tables.
    ```bash
    alembic upgrade head
    ```

6.  **(Optional) Load initial data:**
    You can populate the database with a sample dataset by running the script:
    ```bash
    python scripts/load_initial_data.py
    ```

### Running the Application

To start the development server, run the following command:

```bash
uvicorn src.main:app --reload
```

- The API will be available at http://127.0.0.1:8000. 
- You can access the interactive documentation at http://127.0.0.1:8000/docs.
