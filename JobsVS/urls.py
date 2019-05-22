"""JobsVS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
import xadmin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from django.conf import settings
from django.conf.urls.static import static
from apps.users.views import UserRegViewSet, UserViewSet, UserProfileListViewSet, UserWantJobListViewSet
from apps.education.views import EducationViewSet
from apps.company.views import CompaniesViewSet, CompanySizeViewSet, CompanyQualityViewSet, IndustriesViewSet
from apps.city.views import CitiesViewSet, ProvincesViewSet
from apps.job.views import JobsViewSet, JobFunctionsViewSet
from apps.user_operation.views import UserCollectJobViewSet, UserFocusCompanyViewSet
from apps.analyse.views import JobsMapViewSet,JobsPointViewSet,FareCloudViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, base_name="users")
router.register(r'register', UserRegViewSet, base_name="register")
router.register(
    r'userprofile',
    UserProfileListViewSet,
    base_name="userprofile")
router.register(
    r'userwantjob',
    UserWantJobListViewSet,
    base_name="userwantjob")
router.register(
    r'education',
    EducationViewSet,
    base_name="education")
router.register(
    r'company',
    CompaniesViewSet,
    base_name="company")
router.register(
    r'companysize',
    CompanySizeViewSet,
    base_name="companysize")
router.register(
    r'companyquality',
    CompanyQualityViewSet,
    base_name="companyquality")
router.register(
    r'industry',
    IndustriesViewSet,
    base_name="industry")
router.register(
    r'city',
    CitiesViewSet,
    base_name="city")
router.register(
    r'province',
    ProvincesViewSet,
    base_name="province")
router.register(
    r'jobs',
    JobsViewSet,
    base_name="jobs")
router.register(
    r'jobfunctions',
    JobFunctionsViewSet,
    base_name="jobfunctions")
router.register(
    r'usercollectjob',
    UserCollectJobViewSet,
    base_name="usercollectjob")
router.register(
    r'userfocuscompany',
    UserFocusCompanyViewSet,
    base_name="userfocuscompany")
router.register(
    r'jobsmap',
    JobsMapViewSet,
    base_name="jobsmap")
router.register(
    r'jobspoint',
    JobsPointViewSet,
    base_name="jobspoint")
router.register(
    r'farecloud',
    FareCloudViewSet,
    base_name="farecloud")
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # jwt的认证接口
    url(r'^api/login/', obtain_jwt_token),
    url(r'^api/', include(router.urls)),
    url(r'docs/', include_docs_urls(title="OnlineJudgeBE")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
