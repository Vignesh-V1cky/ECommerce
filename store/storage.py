from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class OverriteFile(FileSystemStorage):
    def get_available_name(self, filename, max_length=None):
        if self.exists(filename):
            os.remove(os.path.join(settings.MEDIA_ROOT, filename))
        return filename