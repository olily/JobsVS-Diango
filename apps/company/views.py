from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Industries, CompanyQuality, CompanySize, Companies
from .filters import IndustriesFilter, CompanyQualityFilter, CompanySizeFilter, CompaniesFilter
from .serializers import IndustriesSerializer, CompanyQualitySerializer, CompanySizeSerializer, CompaniesSerializer

# Create your views here.


class IndustriesViewSet(mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    queryset = Industries.objects.all()
    serializer_class = IndustriesSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = IndustriesFilter


class CompanyQualityViewSet(mixins.ListModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    queryset = CompanyQuality.objects.all()
    serializer_class = CompanyQualitySerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = CompanyQualityFilter


class CompanySizeViewSet(mixins.ListModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    queryset = CompanySize.objects.all()
    serializer_class = CompanySizeSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = CompanySizeFilter


class CompaniesPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100000


class CompaniesViewSet(mixins.ListModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer
    pagination_class = CompaniesPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = CompaniesFilter
