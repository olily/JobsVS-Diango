import xadmin
from .models import JobFunctions, Jobs


class JobFunctionsAdmin(object):
    search_fields = []


class JobsAdmin(object):
    search_fields = []


xadmin.site.register(JobFunctions, JobFunctionsAdmin)
xadmin.site.register(Jobs, JobsAdmin)
