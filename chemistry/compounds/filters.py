from compounds.models import Compound, CompoundStore, Store
from django_filters import BooleanFilter, CharFilter, FilterSet, RangeFilter


class CompoundFilterSet(FilterSet):
    name_icontains = CharFilter(field_name="name", lookup_expr=["icontains"])
    phase_at_room_temperature_eq = CharFilter(field_name="phase_at_room_temperature")
    available_on_stores_eq = BooleanFilter(field_name="stores", method="_available_on_stores")

    def _available_on_stores(self, queryset, name, value):
        return queryset.with_available_on_stores().filter(available=value)

    class Meta:
        model = Compound
        fields = ["name_icontains", "phase_at_room_temperature_eq", "available_on_stores_eq"]


class StoreFilterSet(FilterSet):
    name_icontains = CharFilter(field_name="name", lookup_expr=["icontains"])
    address_icontains = CharFilter(field_name="address", lookup_expr=["icontains"])
    shipping_cost_by_km = RangeFilter()
    min_purchase = RangeFilter()

    class Meta:
        model = Store
        fields = ["name_icontains", "address_icontains", "shipping_cost_by_km", "min_purchase"]


class CompoundStoreFilterSet(FilterSet):
    compound_icontains = CharFilter(field_name="compound__name", lookup_expr=["icontains"])
    store_icontains = CharFilter(field_name="store__name", lookup_expr=["icontains"])
    unit_price = RangeFilter()
    unit_eq = CharFilter(field_name="unit")
    available_eq = BooleanFilter(field_name="available")

    class Meta:
        model = CompoundStore
        fields = ["compound_icontains", "store_icontains", "unit_price", "unit_eq", "available_eq"]
