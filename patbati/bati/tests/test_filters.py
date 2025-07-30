from unittest.mock import PropertyMock, patch
from django.test import TestCase
from django.contrib.gis.geos import Point
from patbati.bati.models import (
    Bati, Nomenclature, NomenclatureType,
)
from patbati.bati.serializers import BatiGeojsonSerializer, BatiSerializer

from django.test import TestCase
from django.db import models

from patbati.bati.filters import EmptyLabelChoiceFilterMixin
from . import factories

class BatiFilterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.batiA = factories.BatiFactory(appelation="Bâtiment A", proprietaire="Alice", indivision=True)
        cls.batiB = factories.BatiFactory(appelation="Bâtiment B", proprietaire="Joe", bat_suppr=True )
        cls.batiC = factories.BatiFactory(appelation="Bâtiment C", proprietaire="Dalton", indivision=True)

    def test_filter_by_appelation(self):
        qs = Bati.objects.filter(appelation="Bâtiment A")
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().proprietaire, "Alice")

    def test_filter_by_indivision(self):
        qs = Bati.objects.filter(indivision=True)
        self.assertEqual(qs.count(), 2)
        appelations = set(qs.values_list("appelation", flat=True))
        self.assertSetEqual(appelations, {"Bâtiment A", "Bâtiment C"})

    def test_filter_by_bat_suppr(self):
        qs = Bati.objects.filter(bat_suppr=True)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().appelation, "Bâtiment B")

class BatiSerializerTest(BatiFilterTest):
    mandatory_cols = {"appelation", "type_bat", "conservation", "notepatri", "secteurs"}

    def test_serializer_fields(self):
        serializer = BatiSerializer(instance=self.batiA)
        data = serializer.data
        assert self.mandatory_cols.issubset(set(data.keys()))

        self.assertEqual(data["appelation"], self.batiA.appelation_link())
        self.assertEqual(data["type_bat"], self.batiA.type_bat_label)
        self.assertEqual(data["conservation"], str(self.batiA.conservation))
        self.assertEqual(data["notepatri"], str(self.batiA.notepatri))


    def test_get_color_false(self):
        b = Bati.objects.get(appelation="Bâtiment A")
        serializer = BatiGeojsonSerializer()
        color = serializer.get_color(b)
        self.assertEqual(color, "#EE2E15")