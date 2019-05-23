import xadmin
from .models import JobMap, FareCloud, CompanyMap, CompanyHot


class JobMapAdmin(object):
    search_fields = []


class FareCloudAdmin(object):
    search_fields = []


class CompanyMapAdmin(object):
    search_fields = []


class CompanyHotAdmin(object):
    search_fields = []


class CompanyQualityAdmin(object):
    search_fields = []


xadmin.site.register(JobMap, JobMapAdmin)
xadmin.site.register(FareCloud, FareCloudAdmin)
xadmin.site.register(CompanyMap, CompanyMapAdmin)
xadmin.site.register(CompanyHot, CompanyHotAdmin)
