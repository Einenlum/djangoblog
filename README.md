# Djangoblog

This is just a toy project to play with Django, its permissions, its ORM, how to deploy… etc.

Visit the [heroku app](https://djangoblog-einenlum.herokuapp.com/).

## Technical details

* File storage: S3 (thanks to `django-storages`)
* DB: postgres in production, sqlite in development

## Install

`cp .env.dist .env`
`poetry install`

## Tests

In your virtual env:

`python manage.py test blog`

## Run

In your virtual env:

`python manage.py runserver`