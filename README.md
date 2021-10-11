# Contacts App

## Prerequisites
* Python 3.10
* pip
* make

## Quickstart
* Ensure that you have pipenv installed `pip install pipenv`
* `cd` to project root folder
* Initialize app with `make init`
* Run app with `make run`

* Check http://localhost:8000/ for the UI
* Check http://localhost:8000/api/ for Swagger UI

## Users and Credentials
For each role `make init` will create a user and output its credentials.
Check outputs of `make init` for something similar to
```
role: regular; username: foo; password: 123
role: admin; username: bar; password: 123
role: superuser; username: example; password: 123
```

* `regular` has read-only access to contacts
* `admin` has read-add-update access to contacts
* `superuser` has full access to contacts

## Generating Sample Data
`make seed_contacts` will provide you with some sample contacts to play with. 


## Project Structure

There are 4 Django apps in this projects:
* `api` provides RESTful interface along with a Swagger endpoint
* `ui` provides user interface
* `contacts` has all the logic as well as Contact model
* `users` contains User model and a migration that creates all the roles

There's also the `templates` folder with all the templates for `ui` app.
