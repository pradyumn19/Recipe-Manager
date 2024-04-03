# Recipe-Manager
Recipe Manager is a Flask-based web application for managing recipes. Users can register, log in, add, edit, view, and delete recipes. This README provides an overview of the project, including setup instructions and a description of available endpoints.
Here's a sample README.md file for your project:

## Overview

The project structure includes the following components:

- `app/`: Directory containing the Flask application code
  - `__init__.py`: Initialization of the Flask app and extensions
  - `model.py`: Definition of database models using SQLAlchemy
  - `routes.py`: Implementation of route endpoints for handling requests
  - `templates/`: Directory containing HTML templates for rendering pages
- `instance/`: Configuration directory (not provided in this example)
- `migrations/`: Directory containing database migration scripts
- `test/`: Directory containing test scripts
- `vrecipemanagerenv/`: Virtual environment directory
- `recipes.db`: SQLite database file
- `main.py`: Entry point for running the Flask application

## Installation and Setup

To set up the Recipe Manager application, follow these steps:

1. Clone the repository:

```
git clone <repository_url>
```

2. Navigate to the project directory:

```
cd recipe_manager
```

3. Create a virtual environment:

```
python -m vrecipemanagerenv venv
```

4. Activate the virtual environment:

   - On Windows:

   ```
   venv\Scripts\activate
   ```

   - On macOS and Linux:

   ```
   source vrecipemanagerenv/bin/activate
   ```

5. Install dependencies:

```
pip install -r requirements.txt
```

6. Set up the database:

```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

7. Run the application:

```
python main.py
```

The application should now be running locally. You can access it at `http://localhost:5000`.

## Endpoints

The following endpoints are available:

- **POST /login**: Log in a user with username and password.
- **POST /logout**: Log out the current user.
- **POST /register**: Register a new user.
- **GET /**: Retrieve all recipes.
- **GET /recipe/<int:recipe_id>**: Retrieve a specific recipe by ID.
- **GET /recipe/<username>**: Retrieve all recipes created by a specific user.
- **POST /recipe/add**: Add a new recipe.
- **PUT /recipe/edit/<int:recipe_id>**: Edit an existing recipe.
- **DELETE /recipe/delete/<int:recipe_id>**: Delete an existing recipe.

