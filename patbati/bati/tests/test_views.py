from django.http import HttpRequest
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from patbati.bati.models import (
    Bati, DemandeTravaux, Travaux, Structure, MateriauxFinFinitionStructure,
    SecondOeuvre, MateriauxFinFinitionSecondOeuvre, Perspective, Enquetes
)
from patbati.bati.views import (
    BatiDetail, BatiList, BatiFormat, BatiViewSet,
    EnquetesCreate, EnquetesUpdate, EnquetesDelete,
    PerspectiveCreate, PerspectiveUpdate, PerspectiveDelete,
    DemandeTravauxCreate, DemandeTravauxUpdate, DemandeTravauxDelete,
    TravauxCreate, StructureFinitionCreate, StructureFinitionUpdate, StructureFinitionDelete,
    SecondOeuvreCreate, SecondOeuvreUpdate, SecondOeuvreDelete,
    SecondOeuvreFinitionCreate, SecondOeuvreFinitionUpdate, SecondOeuvreFinitionDelete,
    BatiDocumentPdfPublic, BatiDocumentPdfDetail
)
from patbati.bati.forms import BatiForm
from django.contrib.auth import get_user_model
from . import factories

User = get_user_model()

class BatiDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('testuser', 'test@example.com', 'password')
        self.bati = factories.BatiFactory(appelation="Test")

    def test_detail_view_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get(self.bati.get_detail_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test", response.content)

class BatiListViewTest(TestCase):
    def setUp(self):
        self.bati = factories.BatiFactory(appelation="Test")

    def test_list_columns(self):
        view = BatiList()
        self.assertIn("appelation", view.columns)
        self.assertIn("appelation", view.searchable_columns)

class BatiCreateViewTest(TestCase):
    def setUp(self):
        self.bati = factories.BatiFactory()

        self.data = {
            "appelation": "Bâtiment A",
            "type_bat": self.bati.type_bat.pk,
            "classe": self.bati.classe.pk,
            "implantation": self.bati.implantation.pk,
            "faitage": self.bati.faitage.pk,
            "indivision": True,
            "proprietaire": "Alice",
            "cadastre": "CadA",
            "lieu_dit": "LieuA",
            "altitude": 123.4,
            "x": 1.1,
            "y": 2.2,
            "situation_geo": "SituA",
            "denivelle": 10.5,
            "exposition": self.bati.exposition.pk,
            "pente": 15.0,
            "capacite": 100.0,
            "bat_suppr": False,
            "notepatri": self.bati.notepatri.pk,
            "patrimonialite": "PatriA",
            "ancien_index": 1.23,
            "conservation": self.bati.conservation.pk,
            "commentaire_masque": "MasqueA",
            "remarque_risque": "RisqueA",
            "geom": "POINT(1 2)",
            "remarque_generale": "RemarqueA",
            "masques": [m.pk for m in self.bati.masques.all()],
            "perspectives": [p.pk for p in self.bati.perspectives.all()],
        }

    def test_create_form(self):
        form = BatiForm(data=self.data)
        self.assertTrue(form.is_valid())

class BatiFormatViewTest(TestCase):
    def test_format_inherits(self):
        view = BatiFormat()
        self.assertTrue(hasattr(view, "columns"))

class BatiViewSetTest(TestCase):
    def setUp(self):
        self.bati = factories.BatiFactory(appelation="Test")

    def test_viewset_queryset(self):
        viewset = BatiViewSet()
        self.assertEqual(viewset.queryset.count(), Bati.objects.count())
        self.assertEqual(viewset.get_view_perm(), "bati.view_bati")

class EnquetesViewTest(TestCase):
    def setUp(self):
        self.bati = factories.BatiFactory(appelation="Test")
        self.enquete = factories.EnqueteFactory(bati=self.bati)

    def test_enquetes_create(self):
        view = EnquetesCreate()
        self.assertEqual(view.model, Enquetes)
        self.assertEqual(view.parent_model, Bati)
        self.assertEqual(view.form_class.__name__, "EnquetesForm")

    def test_enquetes_update(self):
        view = EnquetesUpdate()
        self.assertEqual(view.model, Enquetes)
        self.assertEqual(view.parent_model, Bati)

    def test_enquetes_delete(self):
        view = EnquetesDelete()
        self.assertEqual(view.model, Enquetes)
        self.assertEqual(view.parent_model, Bati)

class PerspectiveViewTest(TestCase):
    def setUp(self):
        self.bati = factories.BatiFactory(appelation="Test")
        self.perspective = factories.PerspectiveFactory(bati=self.bati)

    def test_perspective_create(self):
        view = PerspectiveCreate()
        self.assertEqual(view.model, Perspective)
        self.assertEqual(view.parent_model, Bati)

    def test_perspective_update(self):
        view = PerspectiveUpdate()
        self.assertEqual(view.model, Perspective)
        self.assertEqual(view.parent_model, Bati)

    def test_perspective_delete(self):
        view = PerspectiveDelete()
        self.assertEqual(view.model, Perspective)
        self.assertEqual(view.parent_model, Bati)

class DemandeTravauxViewTest(TestCase):
    def setUp(self):
        self.bati = factories.BatiFactory(appelation="Test")
        self.demande = self.bati.demandes_travaux.first()

    def test_demande_create(self):
        view = DemandeTravauxCreate()
        self.assertEqual(view.model, DemandeTravaux)
        self.assertEqual(view.parent_model, Bati)

    def test_demande_update(self):
        view = DemandeTravauxUpdate()
        self.assertEqual(view.model, DemandeTravaux)
        self.assertEqual(view.parent_model, Bati)

    def test_demande_delete(self):
        view = DemandeTravauxDelete()
        self.assertEqual(view.model, DemandeTravaux)
        self.assertEqual(view.parent_model, Bati)

class TravauxViewTest(TestCase):
    def setUp(self):
        self.bati = factories.BatiFactory(appelation="Test")
        self.demande = self.bati.demandes_travaux.first()
        self.travaux = self.demande.travaux.first()

    def test_dispatch_sets_demande(self):
        view = TravauxCreate()
        request = HttpRequest()
        request.user = AnonymousUser()
        request.method = "GET"
        view.request = request
        kwargs = {"pk": self.demande.pk, "parent_pk": self.demande.pk}
        view.dispatch(request, **kwargs)
        self.assertEqual(view.demande, self.demande)
        self.assertEqual(view.parent_object, self.demande)

    def test_form_valid_sets_demande(self):
        view = TravauxCreate()
        view.demande = self.demande
        view.parent_object = self.bati
        class DummyForm:
            instance = Travaux()
            def save(self):
                return self.instance
        result = view.form_valid(DummyForm())
        self.assertEqual(DummyForm.instance.demande, self.demande)

    def test_get_context_data_includes_demande(self):
        view = TravauxCreate()
        view.demande = self.demande
        view.parent_object = self.bati
        view.object = self.travaux
        request = HttpRequest()
        request.user = AnonymousUser()
        view.request = request
        context = view.get_context_data()
        self.assertIn("demande", context)
        self.assertEqual(context["demande"], self.demande)

    def test_get_success_url_returns_bati_url(self):
        view = TravauxCreate()
        view.demande = self.demande
        url = view.get_success_url()
        self.assertEqual(url, self.bati.get_detail_url())

class StructureFinitionViewTest(TestCase):
    def setUp(self):
        self.bati = factories.BatiFactory(appelation="Test")
        self.structure = self.bati.structure.first()
        self.mff_structure = self.structure.finitions.first()

    def test_structure_finition_create(self):
        view = StructureFinitionCreate()
        self.assertEqual(view.model, MateriauxFinFinitionStructure)
        self.assertEqual(view.parent_model, Structure)

    def test_structure_finition_update(self):
        view = StructureFinitionUpdate()
        self.assertEqual(view.model, MateriauxFinFinitionStructure)
        self.assertEqual(view.parent_model, Structure)

    def test_structure_finition_delete(self):
        view = StructureFinitionDelete()
        self.assertEqual(view.model, MateriauxFinFinitionStructure)
        self.assertEqual(view.parent_model, Structure)

class SecondOeuvreViewTest(TestCase):
    def setUp(self):
        self.bati = factories.BatiFactory(appelation="Test")
        self.second_oeuvre = self.bati.second_oeuvre.first()

    def test_second_oeuvre_create(self):
        view = SecondOeuvreCreate()
        self.assertEqual(view.model, SecondOeuvre)
        self.assertEqual(view.parent_model, Bati)

    def test_second_oeuvre_update(self):
        view = SecondOeuvreUpdate()
        self.assertEqual(view.model, SecondOeuvre)
        self.assertEqual(view.parent_model, Bati)

    def test_second_oeuvre_delete(self):
        view = SecondOeuvreDelete()
        self.assertEqual(view.model, SecondOeuvre)
        self.assertEqual(view.parent_model, Bati)

class SecondOeuvreFinitionViewTest(TestCase):
    def setUp(self):
        self.bati = factories.BatiFactory(appelation="Test")
        self.second_oeuvre = self.bati.second_oeuvre.first()
        self.mff_second_oeuvre = self.second_oeuvre.materiaux_fin.first()

    def test_second_oeuvre_finition_create(self):
        view = SecondOeuvreFinitionCreate()
        self.assertEqual(view.model, MateriauxFinFinitionSecondOeuvre)
        self.assertEqual(view.parent_model, SecondOeuvre)

    def test_second_oeuvre_finition_update(self):
        view = SecondOeuvreFinitionUpdate()
        self.assertEqual(view.model, MateriauxFinFinitionSecondOeuvre)
        self.assertEqual(view.parent_model, SecondOeuvre)

    def test_second_oeuvre_finition_delete(self):
        view = SecondOeuvreFinitionDelete()
        self.assertEqual(view.model, MateriauxFinFinitionSecondOeuvre)
        self.assertEqual(view.parent_model, SecondOeuvre)

class BatiDocumentPdfPublicTest(TestCase):
    def test_pdf_public_template(self):
        view = BatiDocumentPdfPublic()
        self.assertEqual(view.template_name, "bati/bati_public_pdf.html")
        self.assertEqual(view.model, Bati)

class BatiDocumentPdfDetailTest(TestCase):
    def test_pdf_detail_template(self):
        view = BatiDocumentPdfDetail()
        self.assertEqual(view.template_name, "bati/bati_detail_pdf.html")
        self.assertEqual(view.model, Bati)

class StructureFinitionCreateViewTest(TestCase):
    def setUp(self):
        self.bati = factories.BatiFactory(appelation="Test")
        self.structure = self.bati.structure.first()

    def test_dispatch_sets_structure(self):
        view = StructureFinitionCreate()
        request = HttpRequest()
        request.user = AnonymousUser()
        request.method = "GET"
        view.request = request
        kwargs = {"structure_pk": self.structure.pk, "parent_pk": self.structure.pk}
        view.dispatch(request, **kwargs)
        self.assertEqual(view.structure, self.structure)

    def test_form_valid_sets_structure(self):
        view = StructureFinitionCreate()
        view.structure = self.structure
        view.parent_object = self.structure 
        class DummyForm:
            instance = MateriauxFinFinitionStructure()
            def save(self):
                return self.instance
        view.form_valid(DummyForm())
        self.assertEqual(DummyForm.instance.structure, self.structure)

    def test_get_success_url_returns_structure_url(self):
        view = StructureFinitionCreate()
        view.object = MateriauxFinFinitionStructure(structure=self.structure)
        url = view.get_success_url()
        self.assertEqual(url, self.structure.get_detail_url())

class StructureFinitionUpdateViewTest(TestCase):
    def setUp(self):
        self.bati = factories.BatiFactory(appelation="Test")
        self.structure = self.bati.structure.first()
        self.mff_structure = self.structure.finitions.first()

    def test_dispatch_sets_structure(self):
        view = StructureFinitionUpdate()
        request = HttpRequest()
        request.user = AnonymousUser()
        request.method = "GET"
        view.request = request
        kwargs = {
            "structure_pk": self.structure.pk,
            "parent_pk": self.structure.pk,
            "pk": self.mff_structure.pk,
        }
        view.kwargs = kwargs
        view.dispatch(request, **kwargs)
        self.assertEqual(view.structure, self.structure)

    def test_form_valid_sets_structure(self):
        view = StructureFinitionUpdate()
        view.structure = self.structure
        view.parent_object = self.structure
        class DummyForm:
            instance = MateriauxFinFinitionStructure()
            def save(self):
                return self.instance
        view.form_valid(DummyForm())
        self.assertEqual(DummyForm.instance.structure, self.structure)

    def test_get_success_url_returns_structure_url(self):
        view = StructureFinitionUpdate()
        view.object = MateriauxFinFinitionStructure(structure=self.structure)
        url = view.get_success_url()
        self.assertEqual(url, self.structure.get_detail_url())

class SecondOeuvreFinitionCreateViewTest(TestCase):
    def setUp(self):
        self.bati = factories.BatiFactory(appelation="Test")
        self.second_oeuvre = self.bati.second_oeuvre.first()

    def test_dispatch_sets_second_oeuvre(self):
        view = SecondOeuvreFinitionCreate()
        request = HttpRequest()
        request.user = AnonymousUser()
        request.method = "GET"
        view.request = request
        kwargs = {"second_pk": self.second_oeuvre.pk, "parent_pk": self.second_oeuvre.pk}
        view.dispatch(request, **kwargs)
        self.assertEqual(view.second_oeuvre, self.second_oeuvre)

    def test_form_valid_sets_second_oeuvre(self):
        view = SecondOeuvreFinitionCreate()
        view.second_oeuvre = self.second_oeuvre
        view.parent_object = self.second_oeuvre
        class DummyForm:
            instance = MateriauxFinFinitionSecondOeuvre()
            def save(self):
                return self.instance
        view.form_valid(DummyForm())
        self.assertEqual(DummyForm.instance.second_oeuvre, self.second_oeuvre)

    def test_get_success_url_returns_second_oeuvre_url(self):
        view = SecondOeuvreFinitionCreate()
        view.object = MateriauxFinFinitionSecondOeuvre(second_oeuvre=self.second_oeuvre)
        url = view.get_success_url()
        self.assertEqual(url, self.second_oeuvre.get_detail_url())

class SecondOeuvreFinitionUpdateViewTest(TestCase):
    def setUp(self):
        self.bati = factories.BatiFactory(appelation="Test")
        self.second_oeuvre = self.bati.second_oeuvre.first()
        self.mff_second_oeuvre = factories.MateriauxFinFinitionSecondOeuvreFactory(second_oeuvre=self.second_oeuvre)

    def test_dispatch_sets_second_oeuvre(self):
        view = SecondOeuvreFinitionUpdate()
        request = HttpRequest()
        request.user = AnonymousUser()
        request.method = "GET"
        view.request = request
        kwargs = {
            "second_pk": self.second_oeuvre.pk,
            "parent_pk": self.second_oeuvre.pk,
            "pk": self.mff_second_oeuvre.pk,
        }
        view.kwargs = kwargs
        view.dispatch(request, **kwargs)
        self.assertEqual(view.second_oeuvre, self.second_oeuvre)

    def test_form_valid_sets_second_oeuvre(self):
        view = SecondOeuvreFinitionUpdate()
        view.second_oeuvre = self.second_oeuvre
        view.parent_object = self.second_oeuvre
        class DummyForm:
            instance = MateriauxFinFinitionSecondOeuvre()
            def save(self):
                return self.instance
        view.form_valid(DummyForm())
        self.assertEqual(DummyForm.instance.second_oeuvre, self.second_oeuvre)

    def test_get_success_url_returns_second_oeuvre_url(self):
        view = SecondOeuvreFinitionUpdate()
        view.object = MateriauxFinFinitionSecondOeuvre(second_oeuvre=self.second_oeuvre)
        url = view.get_success_url()
        self.assertEqual(url, self.second_oeuvre.get_detail_url())