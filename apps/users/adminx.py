import xadmin
from xadmin import views
from .models import UserProfile


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "OnlineJudge"
    site_footer = "957824770@qq.com"


class UserProfileAdmin(object):
    search_fields = []


xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
