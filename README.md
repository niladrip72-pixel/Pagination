Django Pagination with Celery

A small Django project that fetches posts from a public REST API in the background using Celery and Redis, stores them in a database, and displays them in a paginated table. You can also search for a single post by its ID.

Features
Background fetching – A Celery task downloads all posts from JSONPlaceholder without blocking the web request.
No duplicates – Posts are saved with update_or_create() on the API ID, so fetching repeatedly updates existing rows instead of creating copies.
Pagination – Saved posts are shown 10 per page using Django's Paginator, with Previous / Next links and a "Showing 1–10 of 100 posts" summary.
Search by ID – Look up one post by its original API ID, with validation for non-integer and negative values.
Task results – Celery results are stored in the Django database through django-celery-results.
Admin site – Available at /admin/.
Tech Stack
Python 3
Django (sqlite3 database)
Celery with Redis as the message broker
django-celery-results (stores task results in the database)
requests (calls the external API)
Bootstrap 5.3 (loaded from CDN)
Project Structure
Pagination/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── Pagination/              # Project settings
│   ├── settings.py          # Includes Celery / Redis configuration
│   ├── celery.py            # Celery app setup
│   ├── urls.py
│   └── ...
├── paginationApp/           # Main app
│   ├── models.py            # Post model
│   ├── tasks.py             # fetch_posts Celery task
│   ├── views.py             # home, retrieve_posts, all_posts, search_post
│   ├── urls.py
│   └── migrations/
└── templates/
    ├── base.html            # Layout and navbar
    └── home.html            # Fetch button, search form, posts table
Prerequisites
Python 3
A running Redis server on localhost:6379 (the Celery broker)

Install Redis:

bash
# macOS
brew install redis && brew services start redis

# Ubuntu / Debian
sudo apt install redis-server && sudo service redis-server start

# Windows: use WSL, or run Redis with Docker
docker run -d -p 6379:6379 redis
Getting Started
1. Go to the project folder
bash
cd Pagination
2. Create and activate a virtual environment (recommended)
bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
3. Install dependencies
bash
pip install -r requirements.txt
4. Apply migrations
bash
python manage.py migrate
5. Start the Django server (terminal 1)
bash
python manage.py runserver
6. Start the Celery worker (terminal 2)
bash
# macOS / Linux
celery -A Pagination worker -l info

# Windows (Celery needs the solo pool)
celery -A Pagination worker -l info --pool=solo

Open http://127.0.0.1:8000/ in your browser.

Usage
URL	Method	Description
/	GET	Home page with the fetch button and search form
/retrieve/	POST	Starts the Celery task that fetches the API data
/posts/	GET	Paginated list of saved posts (?page=2, etc.)
/search/	POST	Looks up one post by its API ID
/admin/	GET	Django admin
Click Fetch API Data Using Celery. The task runs in the background, so watch the Celery terminal for the "100 posts saved successfully" message.
Click Retrieve All Data in the navbar to see the posts, 10 per page.
Enter an ID (for example 5) in Search Post by ID to view a single post.
Notes
If you click Fetch while the Celery worker or Redis isn't running, the task won't be processed. Start both first.
DEBUG = True and the SECRET_KEY in settings.py are for development only. Before deploying, move the secret key to an environment variable, set DEBUG = False, and configure ALLOWED_HOSTS.
Add a .gitignore with __pycache__/, *.pyc, db.sqlite3 and venv/ before pushing to GitHub.