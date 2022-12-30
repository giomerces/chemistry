from compounds.filters import CompoundFilterSet
from compounds.models import Compound, Store
from compounds.serializers import CompoundSerializer, StoreSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet


class CompoundViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CompoundFilterSet
    ordering_fields = "__all__"
    ordering = ["name"]
    serializer_class = CompoundSerializer
    queryset = Compound.objects.all()


class StoreViewSet(ModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()


class CompoundStore(ModelViewSet):
    pass
