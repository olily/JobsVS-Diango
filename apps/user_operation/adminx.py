import xadmin
from .models import UserCollectJob, UserFocusCompany, UserFocusJobFunction, UserFocusIndustry


class UserCollectJobAdmin(object):
    search_fields = []


class UserFocusCompanyAdmin(object):
    search_fields = []


class UserFocusJobFunctionAdmin(object):
    search_fields = []


class UserFocusIndustryAdmin(object):
    search_fields = []


xadmin.site.register(UserCollectJob, UserCollectJobAdmin)
xadmin.site.register(UserFocusCompany, UserFocusCompanyAdmin)
xadmin.site.register(UserFocusJobFunction, UserFocusJobFunctionAdmin)
xadmin.site.register(UserFocusIndustry, UserFocusIndustryAdmin)
