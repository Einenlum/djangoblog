# Djangoblog

This is just a toy project to play with Django, its permissions, its ORM, how to deploy… etc.

Visit the [heroku app](https://djangoblog-einenlum.herokuapp.com/).

## Technical details

* File storage: S3 (thanks to `django-storages`)
* DB: postgres in production, sqlite in development
* Search: Algolia is used (overkill for a blog toy project, but just for fun)

## Install

`cp .env.dist .env`
`poetry install`

## Tests

In your virtual env:

`python manage.py test blog`

Tests are also automatically run on Github Actions.

## Run

In your virtual env:

`python manage.py runserver`
