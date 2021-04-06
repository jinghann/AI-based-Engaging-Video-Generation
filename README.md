# AI-based-Engaging-Video-Generation
A web app for AI-empowered e-commerce video generation built with Django and Bootstrap.
![Image of home page](https://github.com/jinghann/AI-based-Engaging-Video-Generation/Images/master/Home-Page.png)

### Features
+ Automatic video generation empowered by AI algorithms from uploaded visual materials (images/video clips).
+ Easy customization on footage sequence, duration and speed.
+ Draft saving and future editing.
+ Share video via post, and comment on posts.
+ Data collection for human-in-the-loop.

### Web App Demo Link
+ Youtube : https://youtu.be/NoRzEVd8zfg

## System Requirements
+ Python==3.6
+ Database: MongoDB
+ Install required libraries (Recommend using python virtual environment):
```
$pip install -r requirements.txt
```


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
