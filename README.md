## Django Website Admin User (database superuser) Account:\
-username: vsgadmin\
-password: vsgadmin
-email: ntufyp20demo@gmail.com

## Google Email Account:
email: ntufyp20demo@gmail.com
password: 3ydkycz5

## Database:
-MongoDB\
-database name: vsgenerator

## System Requirements
+ Python==3.6
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
```
$sudo service mongod start
```
### 3. Start web server
+ Configure the host server in vsgenerator/settings.py:
```
ALLOWED_HOSTS=['Your host IP here']
```
+ Run server:
```
$python manage.py 0.0.0.0:8000 
```
### Open browser and go to:
```
172.21.47.106:8000
```