import logging
from collections import namedtuple

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth.base_user import check_password
from django.contrib.auth.backends import ModelBackend
from django.db import connections

from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)

FIELDS = ['username', 'first_name', 'last_name', 'password', 'email']

Credentials = namedtuple('Credentials', FIELDS)

class DatabaseBackend(ModelBackend):
    """
    Authenticate against a table in Authent database.
    """
    def authenticate(self, request=None, username=None, password=None):
        credentials = self.query_credentials(username)
        if credentials and check_password(password, credentials.password):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username, credentials.email, 'password_never_used')

            self._update_infos(user, credentials)
            return user
        return None
    
    def _update_infos(self, user, credentials):
        user.is_staff = True
        user.is_active = True
        user.first_name = credentials.first_name
        user.last_name = credentials.last_name

        if hasattr(settings, 'AUTHENT_DEFAULT_USER_GROUP_NAME'):
            default_group_name = settings.AUTHENT_DEFAULT_USER_GROUP_NAME
            default_group = Group.objects.get(name=default_group_name)
            user.groups.add(default_group)
        user.save()


    def query_credentials(self, username):
        if not settings.AUTHENT_DATABASE:
            raise ImproperlyConfigured("Database backend is used, without AUTHENT_DATABASE setting.")
        if not settings.AUTHENT_TABLENAME:
            raise ImproperlyConfigured("Database backend is used, without AUTHENT_TABLENAME setting.")
        try:
            result = None
            with connections[settings.AUTHENT_DATABASE].cursor() as cursor:
                table_list = [table.name for table in connections[settings.AUTHENT_DATABASE].introspection.get_table_list(cursor)]
                tablename = settings.AUTHENT_TABLENAME if '.' not in settings.AUTHENT_TABLENAME else settings.AUTHENT_TABLENAME.split('.', 1)[1]
                if tablename not in table_list:
                    raise ImproperlyConfigured("Database backend is used, and AUTHENT_TABLENAME does not exists.")

                sqlquery = "SELECT %s FROM %s WHERE username = " % (', '.join(FIELDS), settings.AUTHENT_TABLENAME)
                cursor.execute(sqlquery + "%s", [username])
                result = cursor.fetchone()
        except ImproperlyConfigured as e:
            logger.exception(e)
            raise
        if result:
            return Credentials(*result)
        return None