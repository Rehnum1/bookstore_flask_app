# Book Store Flask App with Reviews

This is a simple Flask **Book Store** web application prepared for your cloud deployment assignment.

## Features

- List all books
- View details for a single book
- Add a review for a specific book
- View existing reviews for that book
- SQLite database using SQLAlchemy ORM

## Local Setup

1. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open a browser and visit:

```
http://127.0.0.1:5000
```

The app will automatically create `bookstore.db` and seed a few sample books on the first request.

## Deployment Notes (Azure App Service Example)

- Make sure `app.py` contains the Flask application instance called `app`.
- Push this folder to GitHub.
- In Azure App Service:
  - Create a new Web App (Python runtime).
  - Configure deployment from your GitHub repository.
  - Set the startup command (if required) to something like:

    ```bash
    gunicorn --bind=0.0.0.0 --timeout 600 app:app
    ```

- After deployment, visit your Azure URL and confirm:
  - Homepage loads
  - Books list displays
  - You can add reviews
  - Reviews are visible after submission
