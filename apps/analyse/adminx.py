import xadmin
from .models import JobMap

class JobMapAdmin(object):
    search_fields = []

xadmin.site.register(JobMap, JobMapAdmin)
