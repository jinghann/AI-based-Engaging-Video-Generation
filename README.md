# AI-based-Engaging-Video-Generation
A web app for AI-empowered video generation built with Django and Bootstrap.
### Web App Demo Link
+ Youtube : https://youtu.be/NoRzEVd8zfg

## System Requirements
+ Python==3.6
+ Install required libraries (Recommend using python virtual environment):
```
$pip install -r requirements.txt
```
## Database Requirement:
+ MongoDB

## How to start hosting the web app
### 1. If starting a new MongoDB database, first initialize the database to create collections.
```$python manage.py makemigrations
$python manage.py migrate
```
### 2. Start mongodb server

### 3. Start web server
+ Configure the host server in vsgenerator/settings.py:
```
ALLOWED_HOSTS=['Your host IP here']
```
+ Run server:
```
$python manage.py runserver 0.0.0.0:8000
```
