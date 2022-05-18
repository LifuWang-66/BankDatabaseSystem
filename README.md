# cs4400-phase4

## How to start?
### First, create a conda environment with python installed.
```
conda create -n django python
conda activate django
```
### Next, install django and mysql client
```
pip install django
pip install mysqlclient
```
### We now can migrate our database to Django
```
python manage.py migrate
```
### Create a superuser for the admin page
```
python manage.py createsuperuser
```
### Now we can start the server!
```
python manage.py runserver
```
