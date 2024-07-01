## Clone the Repository
    https://github.com/DS9709/user_management.git

## Create virtual enviorrnment
    cd user_management
    python3 -m venv venv

## Activate virtual enviorrnment
* Windows:
    venv\Scripts\activate

* macOS/Linux:
    source venv/bin/activate

## Install Requirements
    pip install -r requirements.txt

## Install PostgreSQL
* Install postgres and pgAdmin on your system
* After completing the setup go to teh settings and do teh following:
    Find 'DATABASES' dictonary in settings and fill the details 'NAME', 'USER', 'PASSWORD' which you created at the time of setup.

## Run Migrations
    python manage.py migrate

## Run the Development Server
    python manage.py runserver 8002
