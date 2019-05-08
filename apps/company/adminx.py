import xadmin
from .models import Industries, Companies


class IndustriesAdmin(object):
    search_fields = []


class CompaniesAdmin(object):
    search_fields = []


xadmin.site.register(Industries, IndustriesAdmin)
xadmin.site.register(Companies, CompaniesAdmin)
