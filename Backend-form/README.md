# Backend-form

## Installation

Install the project dependencies:

```bash
virtualenv venv

source venv/bin/activate

cd src

pip install -r requirements.txt

# Database Migrations

# Apply database migrations for the authapp and confapp apps:

bash

python3 manage.py makemigrations
python3 manage.py migrate authapp
python3 manage.py migrate confapp

# Apply all remaining migrations:

bash

python3 manage.py migrate


python3 manage.py runserver



