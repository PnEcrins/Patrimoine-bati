from unittest.mock import PropertyMock, patch
from django.test import TestCase
from django.contrib.gis.geos import Point
from patbati.bati.models import (
    Bati, Nomenclature, NomenclatureType,
    Enquetes, DemandeTravaux, Travaux, Structure,
    MateriauxFinFinitionStructure, SecondOeuvre,
    MateriauxFinFinitionSecondOeuvre, Equipement,
    ElementPaysager, Perspective
)
from patbati.bati.serializers import BatiGeojsonSerializer, BatiSerializer

import django_filters
from django.test import TestCase
from django.db import models

from patbati.bati.filters import EmptyLabelChoiceFilterMixin

class DummyModel(models.Model):
    pass

class DummyFilterSet(django_filters.FilterSet):
    dummy = django_filters.ModelChoiceFilter(queryset=DummyModel.objects.none(), label="Dummy Label")
    class Meta:
        model = DummyModel
        fields = ['dummy']

class DummyFilter(EmptyLabelChoiceFilterMixin, DummyFilterSet):
    pass

class EmptyLabelChoiceFilterMixinTest(TestCase):
    def test_init_sets_empty_label(self):
        filterset = DummyFilter(data={}, queryset=DummyModel.objects.none())
        field = filterset.form.fields['dummy']

class BatiFilterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create all needed NomenclatureTypes
        types = {}
        for code in [
            "TYPE_BAT", "CL_ARCHI", "IMPLA", "FAITAGE", "EXPO", "NOTE_PAT",
            "CONSERVATION", "STRUCT", "MAT_GE", "MEOEUVRE", "MASQUE", "RISQUE",
            "PERSONNES", "USAGE_TRAVAUX", "NATURE_TRAVAUX", "MAT_FIN", "FIN",
            "SO", "EQUIP", "ELEM_PAYS", "PERSP"
        ]:
            types[code], _ = NomenclatureType.objects.get_or_create(label=code, code=code)

        # Create Nomenclatures for each type
        noms = {}
        for code, typ in types.items():
            noms[code] = Nomenclature.objects.create(id_type=typ, label=f"{code}_label")

        # Create Bati objects with all fields filled
        cls.bati1 = Bati.objects.create(
            appelation="Bâtiment A",
            type_bat=noms["TYPE_BAT"],
            classe=noms["CL_ARCHI"],
            implantation=noms["IMPLA"],
            faitage=noms["FAITAGE"],
            indivision=True,
            proprietaire="Alice",
            cadastre="CadA",
            lieu_dit="LieuA",
            altitude=123.4,
            x=1.1,
            y=2.2,
            situation_geo="SituA",
            denivelle=10.5,
            exposition=noms["EXPO"],
            pente=15.0,
            capacite=100.0,
            bat_suppr=False,
            notepatri=noms["NOTE_PAT"],
            patrimonialite="PatriA",
            ancien_index=1.23,
            conservation=noms["CONSERVATION"],
            commentaire_masque="MasqueA",
            remarque_risque="RisqueA",
            geom=Point(1, 2),
            remarque_generale="RemarqueA",
        )
        cls.bati2 = Bati.objects.create(
            appelation="Bâtiment B",
            type_bat=noms["TYPE_BAT"],
            classe=noms["CL_ARCHI"],
            implantation=noms["IMPLA"],
            faitage=noms["FAITAGE"],
            indivision=False,
            proprietaire="Bob",
            cadastre="CadB",
            lieu_dit="LieuB",
            altitude=234.5,
            x=3.3,
            y=4.4,
            situation_geo="SituB",
            denivelle=20.5,
            exposition=noms["EXPO"],
            pente=25.0,
            capacite=200.0,
            bat_suppr=True,
            notepatri=noms["NOTE_PAT"],
            patrimonialite="PatriB",
            ancien_index=2.34,
            conservation=noms["CONSERVATION"],
            commentaire_masque="MasqueB",
            remarque_risque="RisqueB",
            geom=Point(3, 4),
            remarque_generale="RemarqueB",
        )
        cls.bati3 = Bati.objects.create(
            valide = True,
            appelation="Bâtiment C",
            type_bat=noms["TYPE_BAT"],
            classe=noms["CL_ARCHI"],
            implantation=noms["IMPLA"],
            faitage=noms["FAITAGE"],
            indivision=True,
            proprietaire="Charlie",
            cadastre="CadC",
            lieu_dit="LieuC",
            altitude=345.6,
            x=5.5,
            y=6.6,
            situation_geo="SituC",
            denivelle=30.5,
            exposition=noms["EXPO"],
            pente=35.0,
            capacite=300.0,
            bat_suppr=False,
            notepatri=noms["NOTE_PAT"],
            patrimonialite="PatriC",
            ancien_index=3.45,
            conservation=noms["CONSERVATION"],
            commentaire_masque="MasqueC",
            remarque_risque="RisqueC",
            geom=Point(5, 6),
            remarque_generale="RemarqueC",
        )

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

    def test_serializer_fields(self):
        b = Bati.objects.get(appelation="Bâtiment A")
        with patch.object(Bati, "secteurs", new_callable=PropertyMock) as mock_secteurs:
            mock_secteurs.return_value = ""
            data = BatiSerializer(b).data
            self.assertIn("appelation", data)
            self.assertIn("type_bat", data)
            self.assertIn("conservation", data)
            self.assertIn("notepatri", data)
            self.assertIn("secteurs", data)
            self.assertEqual(data["appelation"], b.appelation_link())
            self.assertEqual(data["type_bat"], b.type_bat_label)
            self.assertEqual(data["conservation"], str(b.conservation))
            self.assertEqual(data["notepatri"], str(b.notepatri))
            self.assertEqual(data["secteurs"], "")

    def test_get_color_true(self):
        b = Bati.objects.get(appelation="Bâtiment C")
        serializer = BatiGeojsonSerializer()
        color = serializer.get_color(b)
        self.assertEqual(color, "#48EE15")

    def test_get_color_false(self):
        b = Bati.objects.get(appelation="Bâtiment A")
        serializer = BatiGeojsonSerializer()
        color = serializer.get_color(b)
        self.assertEqual(color, "#EE2E15")