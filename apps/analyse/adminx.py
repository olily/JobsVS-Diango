import xadmin
from .models import JobMap,FareCloud

class JobMapAdmin(object):
    search_fields = []

xadmin.site.register(JobMap, JobMapAdmin)


class FareCloudAdmin(object):
    search_fields = []

xadmin.site.register(FareCloud, FareCloudAdmin)