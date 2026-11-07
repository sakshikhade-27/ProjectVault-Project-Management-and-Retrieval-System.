# ProjectVault

A hierarchical project archive: categories and subcategories on the left as a tree,
project details on the right, with login and search. Flask + SQLite + HTML/CSS/JS.

## Run it

    python -m venv venv
    venv\Scripts\activate          (Windows)   |   source venv/bin/activate   (Mac/Linux)
    pip install -r requirements.txt
    python app.py

Open http://127.0.0.1:5000, click "Create an account", then log in.

## First use

1. Click "New top-level category" (for example: Software projects).
2. Hover a folder, click the three dots, choose "New subcategory" or "Add project here".
3. Fill the form: title, developed by, date, category, description, optional file.
4. Use the search box to find a project by title, developer, date or category.

## Before real use

- Set a strong SECRET_KEY (environment variable) in config.py.
- Run behind a proper server (waitress or gunicorn) instead of app.run(debug=True).
