from decimal import Decimal

from compounds.models_manager import CompoundQuerySet, CompoundStoreQuerySet
from compounds.validators import gps_coordinates_validator
from core.models import BaseNameMixin, ChemistryModelMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from haversine import haversine


class Compound(ChemistryModelMixin, BaseNameMixin):
    PHASES = [
        ("S", "Solid"),
        ("L", "Liquid"),
        ("G", "Gas"),
        ("P", "Plasma"),
    ]

    formula = models.CharField(max_length=50)
    boiling_point = models.DecimalField(decimal_places=8, max_digits=16)
    melting_point = models.DecimalField(decimal_places=8, max_digits=16)
    phase_at_room_temperature = models.CharField(choices=PHASES, max_length=10)
    density = models.DecimalField(decimal_places=8, max_digits=16)
    molar_mass = models.DecimalField(decimal_places=8, max_digits=16)
    stores = models.ManyToManyField("compounds.Store", through="compounds.CompoundStore", related_name="compounds")

    objects = models.Manager.from_queryset(CompoundQuerySet)()

    def __str__(self):
        return "%s, %s" % (self.name, self.formula)

    def calculate_cost(
        self,
        amount: Decimal,
        normalized_price: Decimal,
        origin_coordinates: list[Decimal],
        coordinates: list[Decimal],
        shipping_cost_by_km: Decimal,
        store: str,
    ) -> dict:
        # assuming individual shipping and using haversine formula
        product_cost = abs(amount * normalized_price)
        shipping_cost = Decimal(haversine(tuple(origin_coordinates), tuple(coordinates))) * shipping_cost_by_km
        return {
            "product_cost": "%.2f" % product_cost,
            "shipping_cost": "%.2f" % shipping_cost,
            "total": "%.2f" % (product_cost + shipping_cost),
            "store": store,
        }

    def search_min_cost_for_unit_of_mass(self, **kwargs) -> dict:
        available_options = CompoundStore.objects.search_min_cost_for_unit_of_mass(compound=self)
        better_deal = None
        for option in available_options:
            calculated_result = self.calculate_cost(**option, **kwargs)

            if better_deal is None:
                better_deal = calculated_result
            elif calculated_result["total"] < better_deal["total"]:
                better_deal = calculated_result

        return better_deal


class Store(ChemistryModelMixin, BaseNameMixin):
    address = models.CharField(max_length=250, null=True)
    shipping_cost_by_km = models.DecimalField(decimal_places=8, max_digits=16)
    min_purchase = models.DecimalField(decimal_places=8, max_digits=16)
    gps_coordinates = ArrayField(
        models.DecimalField(decimal_places=8, max_digits=16), size=2, validators=[gps_coordinates_validator]
    )

    def __str__(self):
        return "%s, %s" % (self.name, self.address)


class CompoundStore(ChemistryModelMixin):
    GRAMME = "g"
    KILO = "Kg"
    MILLILITER = "mL"
    LITER = "L"
    UNITS = [
        (GRAMME, "Gramme"),
        (KILO, "Kilo"),
        (MILLILITER, "Milliliter"),
        (LITER, "Liter"),
    ]
    compound = models.ForeignKey("compounds.Compound", on_delete=models.CASCADE)
    store = models.ForeignKey("compounds.Store", on_delete=models.CASCADE)
    unit_price = models.DecimalField(decimal_places=8, max_digits=16)
    unit = models.CharField(choices=UNITS, max_length=10)
    available = models.BooleanField(default=True)

    objects = models.Manager.from_queryset(CompoundStoreQuerySet)()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["compound", "store"], name="compound_store_unique")]

    def __str__(self):
        return "%s, %s" % (self.compound.name, self.store.name)
