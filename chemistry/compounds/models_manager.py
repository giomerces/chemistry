from decimal import Decimal

from django.db import models
from django.db.models import BooleanField, Case, Count, F, Q, When
from django.db.models.functions import Cast


class CompoundQuerySet(models.QuerySet):
    def with_available_on_stores(self):
        return self.annotate(count=Count("stores")).annotate(available=Cast(Q(count__gt=0), BooleanField()))


class CompoundStoreQuerySet(models.QuerySet):
    def for_compound(self, compound):
        return self.filter(compound=compound)

    def available_on_store(self):
        return self.filter(available=True)

    def only_unit_of_mass(self):
        return self.filter(unit__in=[self.model.GRAMME, self.model.KILO])

    def with_normalized_unit_of_mass(self):
        return self.annotate(
            normalized_price=Case(
                When(unit=self.model.KILO, then=F("unit_price") / Decimal(1000)), default=F("unit_price")
            )
        )

    def with_shipping_cost_params(self):
        return self.annotate(
            shipping_cost_by_km=F("store__shipping_cost_by_km"),
            coordinates=F("store__gps_coordinates"),
        )

    def search_min_cost_for_unit_of_mass(self, compound):
        return (
            self.for_compound(compound)
            .only_unit_of_mass()
            .available_on_store()
            .with_normalized_unit_of_mass()
            .with_shipping_cost_params()
            .values("store", "shipping_cost_by_km", "coordinates", "normalized_price")
        )
