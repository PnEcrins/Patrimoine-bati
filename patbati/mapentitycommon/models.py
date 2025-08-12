from django.db import models
from mapentity.models import MapEntityMixin

# Create your models here.
from paperclip.models import (
    FileType as BaseFileType,
    Attachment as BaseAttachment,
    License as BaseLicense,
)

# Create your models here.


class FileType(BaseFileType):
    pass


class License(BaseLicense):
    pass


class Attachment(BaseAttachment):
    pass


# # Used to create the matching url name
# ENTITY_LIST = "list"
# ENTITY_VIEWSET = "drf-viewset"
# ENTITY_FORMAT_LIST = "format_list"
# ENTITY_DETAIL = "detail"
# ENTITY_FILTER = "filter"
# ENTITY_MAPIMAGE = "mapimage"
# ENTITY_DOCUMENT = "document"
# ENTITY_MARKUP = "markup"
# ENTITY_DUPLICATE = "duplicate"
# ENTITY_CREATE = "add"
# ENTITY_UPDATE = "update"
# ENTITY_DELETE = "delete"
# ENTITY_UPDATE_GEOM = "update_geom"

# ENTITY_PERMISSION_CREATE = 'add'
# ENTITY_PERMISSION_READ = 'view'
# ENTITY_PERMISSION_UPDATE = 'change'
# ENTITY_PERMISSION_DELETE = 'delete'
# ENTITY_PERMISSION_EXPORT = 'export'
# ENTITY_PERMISSION_UPDATE_GEOM = 'change_geom'
# ENTITY_PERMISSIONS = (
#     ENTITY_PERMISSION_CREATE,
#     ENTITY_PERMISSION_READ,
#     ENTITY_PERMISSION_UPDATE,
#     ENTITY_PERMISSION_UPDATE_GEOM,
#     ENTITY_PERMISSION_DELETE,
#     ENTITY_PERMISSION_EXPORT
# )

# class BaseMapentityOverridMixin(MapEntityMixin):
#     pass
# @classmethod
# def get_entity_kind_permission(cls, entity_kind):
#     operations = {
#         ENTITY_CREATE: ENTITY_PERMISSION_CREATE,
#         ENTITY_DUPLICATE: ENTITY_PERMISSION_CREATE,
#         ENTITY_UPDATE: ENTITY_PERMISSION_UPDATE,
#         ENTITY_UPDATE_GEOM: ENTITY_PERMISSION_UPDATE_GEOM,
#         ENTITY_DELETE: ENTITY_PERMISSION_DELETE,
#         ENTITY_DETAIL: ENTITY_PERMISSION_READ,
#         ENTITY_LIST: ENTITY_PERMISSION_READ,
#         ENTITY_FILTER: ENTITY_PERMISSION_READ,
#         ENTITY_VIEWSET: ENTITY_PERMISSION_READ,
#         ENTITY_MARKUP: ENTITY_PERMISSION_READ,
#         ENTITY_FORMAT_LIST: ENTITY_PERMISSION_EXPORT,
#         ENTITY_MAPIMAGE: ENTITY_PERMISSION_EXPORT,
#         ENTITY_DOCUMENT: ENTITY_PERMISSION_EXPORT,
#     }
#     perm = operations.get(entity_kind, entity_kind)
#     assert perm in ENTITY_PERMISSIONS
#     return perm
