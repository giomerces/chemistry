from core.models import ChemistryModelMixin
from django.db import models


class Compound(ChemistryModelMixin):
    PHASES = [
        ("S", "Solid"),
        ("L", "Liquid"),
        ("G", "Gas"),
        ("P", "Plasma"),
    ]

    name = models.CharField(max_length=50)
    formula = models.CharField(max_length=50)
    boiling_point = models.DecimalField(decimal_places=8, max_digits=16)
    melting_point = models.DecimalField(decimal_places=8, max_digits=16)
    phase_at_room_temperature = models.CharField(choices=PHASES, max_length=10)
    density = models.DecimalField(decimal_places=8, max_digits=16)
    stores = models.ManyToManyField("compounds.Store", through="compounds.CompoundStore", related_name="stores")

    def __str__(self):
        return "%s, %s" % (self.name, self.formula)


class Store(ChemistryModelMixin):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=250, null=True)
    shipping_cost_by_km = models.DecimalField(decimal_places=8, max_digits=16)
    min_purchase = models.DecimalField(decimal_places=8, max_digits=16)


class CompoundStore(ChemistryModelMixin):
    UNITS = [
        ("g", "Gramme"),
        ("Kg", "Kilo"),
        ("mL", "Milliliter"),
        ("L", "Liter"),
    ]
    compound = models.ForeignKey("compounds.Compound", on_delete=models.CASCADE)
    store = models.ForeignKey("compounds.Store", on_delete=models.CASCADE)
    unit_price = models.DecimalField(decimal_places=8, max_digits=16)
    unit = models.CharField(choices=UNITS, max_length=10)
    available = models.BooleanField(default=True)
