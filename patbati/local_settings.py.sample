AUTHENTICATION_BACKENDS += ['authent.backend.DatabaseBackend']


AUTHENT_DATABASE = 'authent'
AUTHENT_TABLENAME = 'utilisateurs.ma_table'

DATABASES['authent'] = {
    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    'NAME': '',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
    'OPTIONS' : {'options': '-c search_path=public,utilisateurs'}

}

#AUTHENT_DEFAULT_USER_GROUP_NAME = "test"