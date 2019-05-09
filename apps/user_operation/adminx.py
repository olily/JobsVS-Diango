import xadmin
from .models import UserCollectJob, UserFocusCompany


class UserCollectJobAdmin(object):
    search_fields = []


class UserFocusCompanyAdmin(object):
    search_fields = []


xadmin.site.register(UserCollectJob, UserCollectJobAdmin)
xadmin.site.register(UserFocusCompany, UserFocusCompanyAdmin)
