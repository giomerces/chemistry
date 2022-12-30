from compounds.models import Compound
from django.db.models import BooleanField, Count, Q
from django.db.models.functions import Cast
from django_filters import BooleanFilter, CharFilter, FilterSet


class CompoundFilterSet(FilterSet):
    name_contains = CharFilter(field_name="name", lookup_expr=["contains"])
    phase_at_room_temperature_eq = CharFilter(field_name="phase_at_room_temperature")
    available_on_store_eq = BooleanFilter(field_name="stores", method="_count_many_to_many")

    def _count_many_to_many(self, queryset, name, value):
        return (
            queryset.annotate(count=Count(name))
            .annotate(available=Cast(Q(count__gt=0), BooleanField()))
            .filter(available=value)
        )

    class Meta:
        model = Compound
        fields = ["name_contains", "phase_at_room_temperature_eq", "available_on_store_eq"]
