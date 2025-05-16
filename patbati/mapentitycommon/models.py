from django.db import models

# Create your models here.
from paperclip.models import FileType as BaseFileType, Attachment as BaseAttachment, License as BaseLicense

# Create your models here.

class FileType(BaseFileType):
    pass


class License(BaseLicense):
    pass


class Attachment(BaseAttachment):
    pass
