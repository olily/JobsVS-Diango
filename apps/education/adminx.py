import xadmin
from .models import Education


class EducationAdmin(object):
    search_fields = []


xadmin.site.register(Education, EducationAdmin)
