# Quick Start

## Docker

- Make sure you have `docker-compose` installed on your environment.
- Run `docker-compose up`
- View the application at http://localhost:5000/api/v1 once it's ready

### Test Functionality

- Create a user with the `/signup` endpoint
- Authenticate via `/login` endpoint and add the token to your `Authorization` header
- Hit `/post` endpoints with json content matching the sample models. Non-matching content will be considered bad input.
- To see a specific user's blog posts, get by user id `/user/<id>/posts`
- If you need to figure out a user's id, use the `/user` endpoints
- For admin functionality (ie. most `/user` endpoints):
    - Update the user's permissions in the database

        `docker exec -it -u root blog-app_db_1 bash`

        `mysql -u root -p` (password is "admin")

        `use blog;`

        `update user set admin=1 where username=$(YOUR_USERNAME);`

    - Now you can hit the `@admin_required` endpoints

## Local Development

- Create a virtual environment:
    
    `python3 -m venv venv`

- Activate environment:

    `. venv/bin/activate`

- Export environment variables

    `export FLASK_APP=app.py`

    `export BLOG_APP_ENV='test'`

- Requirements
    - Install some requirements to make mysql work

        `apt update && apt install python3-dev default-libmysqlclient-dev pkg-config build-essential`

    - Install requirements

        `pip install -r requirements.txt`

- Manage database
    - Generate migrations

        `flask db migrate`

    - Apply migrations

        `flask db upgrade`

- Testing
    - Run tests (allowing breakpoints)

        `python -m pytest --capture=no`

    - Run tests with coverage

        `coverage run -m pytest`

    - Get coverage report

        `coverage report -m`

    - Lint

        `pylint *.py`

