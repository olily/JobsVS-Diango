import xadmin
from .models import Provinces, Cities


class ProvincesAdmin(object):
    search_fields = []


class CitiesAdmin(object):
    search_fields = []


xadmin.site.register(Provinces, ProvincesAdmin)
xadmin.site.register(Cities, CitiesAdmin)
