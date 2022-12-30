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
        )

    def test_object_str_name(self):
        compound = Compound.objects.get(id=1)
        expected_object_name = f"{compound.name}, {compound.formula}"
        self.assertEqual(str(compound), expected_object_name)
