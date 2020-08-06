from .settings import *

USE_DEVELOPMENT_ENV = True
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}