from decimal import Decimal

from compounds.models import Compound
from django.test import TestCase


class CompoundTestCase(TestCase):
    def setUp(self):
        Compound.objects.create(
            name="Water",
            formula="H20",
            boiling_point=100,
            melting_point=0,
            phase_at_room_temperature="L",
            density=1000,
            molar_mass=18,
        )

    def test_object_str_name(self):
        compound = Compound.objects.get(name="Water")
        expected_object_name = f"{compound.name}, {compound.formula}"
        self.assertEqual(str(compound), expected_object_name)

    def test_object_calculate_cost(self):
        compound = Compound.objects.get(name="Water")
        cost = compound.calculate_cost(
            amount=Decimal(1000),
            normalized_price=Decimal(2),
            origin_coordinates=[40, 40],
            coordinates=[40, 42],
            shipping_cost_by_km=Decimal(2.5),
            store=1,
        )
        self.assertEqual(cost["product_cost"], "2000.00")
