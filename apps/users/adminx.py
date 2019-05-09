import xadmin
from xadmin import views
from .models import UserProfile, UserWantJob


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "JobsVS"
    site_footer = "1135569701@qq.com"


class UserProfileAdmin(object):
    search_fields = []


class UserWantJobAdmin(object):
    search_fields = []


xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(UserWantJob, UserWantJobAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
