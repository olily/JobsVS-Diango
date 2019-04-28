from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Industries, Companies
from .filters import IndustriesFilter, CompaniesFilter
from .serializers import IndustriesSerializer, CompaniesSerializer

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


class CompaniesViewSet(mixins.ListModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filter_class = CompaniesFilter
