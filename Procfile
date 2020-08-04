release: python manage.py migrate && python manage.py algolia_clearindex && python manage.py algolia_reindex
web: gunicorn djangoblog.wsgi --log-file -