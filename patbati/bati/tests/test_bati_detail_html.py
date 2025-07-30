import datetime
from django.test import TestCase
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from patbati.bati.models import (
    Bati, Nomenclature, NomenclatureType,
    Enquetes, DemandeTravaux, Travaux, Structure,
    MateriauxFinFinitionStructure, SecondOeuvre,
    MateriauxFinFinitionSecondOeuvre, Equipement,
    ElementPaysager, Perspective
)

User = get_user_model()


class BatiDetailHTMLTest(TestCase):

    with open("patbati/bati/templates/bati/bati_detail.html") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    def test_tab_panes_exist(self):
        for pane_id in ["enq-pers", "travaux", "structure"]:
            self.assertIsNotNone(
                self.soup.find("div", {"id": pane_id}),
                f"Tab pane '{pane_id}' not found in HTML"
            )

    def test_nav_links(self):
        nav_links = self.soup.select("a.nav-link")
        self.assertTrue(any("Travaux" in link.text for link in nav_links))
        self.assertTrue(any("Gros et Second Oeuvre" in link.text for link in nav_links))
        self.assertTrue(any("Perspectives et Enquetes" in link.text for link in nav_links))
        self.assertTrue(any("Zonage" in link.text for link in nav_links))

    def test_perspectives_table_headers(self):
        pane = self.soup.find("div", {"id": "enq-pers"})
        self.assertIsNotNone(pane)
        table = pane.find("table", class_="table table-striped")
        self.assertIsNotNone(table)
        headers = [th.text.strip() for th in table.find_all("th")]
        expected = ["Date", "Perspective", "Actions"]
        for h in expected:
            self.assertIn(h, headers)

    def test_enquetes_table_headers(self):
        pane = self.soup.find("div", {"id": "enq-pers"})
        self.assertIsNotNone(pane)
        tables = pane.find_all("table", class_="table table-striped")
        self.assertTrue(len(tables) >= 2)
        enq_table = tables[1]
        headers = [th.text.strip() for th in enq_table.find_all("th")]
        expected = ["Personne", "Date enquête", "Date rédaction", "Actions"]
        for h in expected:
            self.assertIn(h, headers)

    def test_empty_state_enquetes(self):
        pane = self.soup.find("div", {"id": "enq-pers"})
        self.assertIsNotNone(pane)
        enq_table = pane.find_all("table", class_="table table-striped")[1]
        self.assertIn("Aucune enquête associée", enq_table.text)

    def test_travaux_header_row(self):
        pane = self.soup.find("div", {"id": "travaux"})
        self.assertIsNotNone(pane)
        header_row = pane.find("div", class_="row font-weight-bold border-bottom pb-2 mb-2")
        self.assertIsNotNone(header_row)
        expected = [
            "Permis", "Date demande", "Autorisation", "Date permis", "Numéro", "Actions"
        ]
        for h in expected:
            self.assertIn(h, header_row.text)

    def test_travaux_empty_state(self):
        pane = self.soup.find("div", {"id": "travaux"})
        self.assertIsNotNone(pane)
        self.assertIn("Aucune demande", pane.text)

    def test_travaux_accordion_structure(self):
        pane = self.soup.find("div", {"id": "travaux"})
        self.assertIsNotNone(pane)
        accordion = pane.find("div", {"id": "demandesAccordion"})
        self.assertIsNotNone(accordion)
        self.assertTrue("accordion" in accordion.get("class", []) or accordion.get("id") == "demandesAccordion")

    def test_travaux_table_headers(self):
        pane = self.soup.find("div", {"id": "travaux"})
        self.assertIsNotNone(pane)
        accordion = pane.find("div", {"id": "demandesAccordion"})
        table = accordion.find("table", class_="table table-sm table-bordered mb-0 text-center")
        if table:
            headers = [th.text.strip() for th in table.find_all("th")]
            expected = [
                "Date des travaux", "Autorisation du parc", "Subvention accordée",
                "Nature des Travaux", "Nouvel usage", "Actions"
            ]
            for h in expected:
                self.assertIn(h, headers)

    def test_travaux_empty_state_for_travaux(self):
        pane = self.soup.find("div", {"id": "travaux"})
        self.assertIsNotNone(pane)
        accordion = pane.find("div", {"id": "demandesAccordion"})
        if accordion:
            self.assertTrue(
                "Aucun travaux pour cette demande" in accordion.text or
                "Aucun travaux pour cette demande." in accordion.text
            )

    def test_structure_section_exists(self):
        pane = self.soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        self.assertIn("Liste des structures", pane.text)
        self.assertIn("Liste des éléments de second oeuvre", pane.text)

    def test_structure_empty_state(self):
        pane = self.soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        self.assertIn("Aucune structure", pane.text)
        self.assertIn("Aucun élément de second oeuvre", pane.text)

    def test_structure_table_headers(self):
        pane = self.soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        tables = pane.find_all("table", class_="table table-sm table-bordered mb-2")
        if tables:
            headers = [th.text.strip() for th in tables[0].find_all("th")]
            self.assertIn("Description de la structure", headers)
            self.assertIn("Structure", tables[0].text)
            self.assertIn("Structure remarquable", tables[0].text)
            self.assertIn("Conservation", tables[0].text)
            self.assertIn("Matériau principal", tables[0].text)
            self.assertIn("Mise en oeuvre", tables[0].text)
            self.assertIn("Commentaire", tables[0].text)

    def test_structure_finitions_table_headers(self):
        pane = self.soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        tables = pane.find_all("table", class_="table table-sm table-bordered mb-0")
        if tables:
            headers = [th.text.strip() for th in tables[0].find_all("th")]
            self.assertIn("Matériau fin", headers)
            self.assertIn("Finition", headers)
            self.assertIn("Actions", headers)

    def test_second_oeuvre_table_headers(self):
        pane = self.soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        tables = pane.find_all("table", class_="table table-sm table-bordered mb-2")
        if len(tables) > 1:
            headers = [th.text.strip() for th in tables[1].find_all("th")]
            self.assertIn("Description de l'élément", headers)
            self.assertIn("Catégorie", tables[1].text)
            self.assertIn("Remarquable", tables[1].text)
            self.assertIn("Conservation", tables[1].text)
            self.assertIn("Commentaire", tables[1].text)

    def test_second_oeuvre_finitions_table_headers(self):
        pane = self.soup.find("div", {"id": "structure"})
        self.assertIsNotNone(pane)
        tables = pane.find_all("table", class_="table table-sm table-bordered mb-0")
        if len(tables) > 1:
            headers = [th.text.strip() for th in tables[1].find_all("th")]
            self.assertIn("Matériau fin", headers)
            self.assertIn("Finition", headers)
            self.assertIn("Actions", headers)

    def test_plus_icons_present(self):
        plus_icons = self.soup.select("i.bi-plus")
        self.assertTrue(len(plus_icons) > 0)

    def test_pencil_icons_present(self):
        pencil_icons = self.soup.select("i.bi-pencil")
        self.assertTrue(len(pencil_icons) > 0 or len(self.soup.select("i.bi-pencil-square")) > 0)

    def test_trash_icons_present(self):
        trash_icons = self.soup.select("i.bi-trash")
        self.assertTrue(len(trash_icons) > 0)

    def test_chevron_icons_present(self):
        chevron_icons = self.soup.select("i.bi-chevron-down")
        self.assertTrue(len(chevron_icons) > 0)

    def test_traverse_dom(self):
        tables = self.soup.find_all("table", class_="table-striped")
        found = False
        for table in tables:
            if table.find_parent("div", class_="mb-3") or table.find_parent("div", class_="card-body"):
                found = True
                break
        self.assertTrue(found)

User = get_user_model()

class BatiListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('testuser', 'test@example.com', 'password')      

    def test_bati_list_html_structure(self):
        self.client.force_login(self.user)
        response = self.client.get('/bati/list/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content)

        table = soup.find("table")
        self.assertIsNotNone(table)

        headers = [th.text.strip().lower() for th in table.find_all("th")]
        expected_headers = [
            "id", "validé", "appelation", "type bat", "notepatri",
            "conservation", "secteur"
        ]
        for header in expected_headers:
            self.assertIn(header, headers)

class BatiDetailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('testuser', 'test@example.com', 'password')

        # Nomenclatures
        ntype = NomenclatureType.objects.create(label="NOTE_PAT", code="NOTE_PAT")
        note_nom = Nomenclature.objects.create(id_type=ntype, label="5")
        ntype2 = NomenclatureType.objects.create(label="TYPE_BAT", code="TYPE_BAT")
        typebat_nom = Nomenclature.objects.create(id_type=ntype2, label="TYPE_BAT_label")
        ntype3 = NomenclatureType.objects.create(label="CL_ARCHI", code="CL_ARCHI")
        classe_nom = Nomenclature.objects.create(id_type=ntype3, label="CL_ARCHI_label")
        ntype4 = NomenclatureType.objects.create(label="PERSONNES", code="PERSONNES")
        personne_nom = Nomenclature.objects.create(id_type=ntype4, label="John Doe")

        # Full Bati
        self.bati = Bati.objects.create(
            appelation="TestBati",
            type_bat=typebat_nom,
            classe=classe_nom,
            notepatri=note_nom,
            indivision=True,
            date_insert=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
            geom=Point(1.23, 4.56),
        )

        # Perspective
        self.perspective = Perspective.objects.create(
            bati=self.bati,
            date=datetime.datetime(2024, 2, 2, tzinfo=datetime.timezone.utc),
            perspective=note_nom
        )

        # Enquete
        self.enquete = Enquetes.objects.create(
            bati=self.bati,
            personne=personne_nom,
            date_enquete=datetime.datetime(2024, 3, 3, tzinfo=datetime.timezone.utc),
            date_redaction=datetime.datetime(2024, 3, 4, tzinfo=datetime.timezone.utc)
        )

        # DemandeTravaux
        self.demande = DemandeTravaux.objects.create(
            bati=self.bati,
            date_demande_permis=datetime.datetime(2024, 4, 4, tzinfo=datetime.timezone.utc),
            autorisation_p=True,
            date_permis=datetime.datetime(2024, 4, 5, tzinfo=datetime.timezone.utc),
            num_permis="1234"
        )

        # Travaux
        self.travaux = Travaux.objects.create(
            demande=self.demande,
            date=datetime.datetime(2024, 5, 5, tzinfo=datetime.timezone.utc),
            autorisation=True,
            subvention_pne=1000,
            nature=note_nom,
            usage=note_nom
        )

        # Structure
        self.structure = Structure.objects.create(
            bati=self.bati,
            type=note_nom,
            est_remarquable=True,
            conservation=note_nom,
            materiaux_principal=note_nom,
            mise_en_oeuvre=note_nom,
            info_structure="Structure info"
        )

        # MateriauxFinFinitionStructure
        self.mff = MateriauxFinFinitionStructure.objects.create(
            structure=self.structure,
            materiaux_fin=note_nom,
            finition=note_nom
        )

        # SecondOeuvre
        self.second_oeuvre = SecondOeuvre.objects.create(
            bati=self.bati,
            type=note_nom,
            est_remarquable=True,
            conservation=note_nom,
            commentaire="Second oeuvre comment"
        )

        # MateriauxFinFinitionSecondOeuvre
        self.mff_so = MateriauxFinFinitionSecondOeuvre.objects.create(
            second_oeuvre=self.second_oeuvre,
            materiaux_fin=note_nom,
            finition=note_nom
        )

        # Empty Bati
        ntype2_empty = NomenclatureType.objects.create(label="TYPE_BAT_EMPTY", code="TYPE_BAT_EMPTY")
        typebat_nom_empty = Nomenclature.objects.create(id_type=ntype2_empty, label="EMPTY")
        ntype3_empty = NomenclatureType.objects.create(label="CL_ARCHI_EMPTY", code="CL_ARCHI_EMPTY")
        classe_nom_empty = Nomenclature.objects.create(id_type=ntype3_empty, label="EMPTY")

        self.bati_empty = Bati.objects.create(
            appelation="",
            type_bat=typebat_nom_empty,
            classe=classe_nom_empty,
            notepatri=None,
            indivision=None,
            date_insert=None,
            geom=Point(0, 0),
        )

    def get_soup(self, pk):
        self.client.force_login(self.user)
        response = self.client.get(f'/bati/{pk}/')
        self.assertEqual(response.status_code, 200)
        return BeautifulSoup(response.content)

    def test_perspectives(self):
        # Filled
        soup = self.get_soup(self.bati.pk)
        self.assertIn("5", soup.select_one('[data-qa="perspective-label"]').text)
        self.assertIn("2024", soup.select_one('[data-qa="perspective-date"]').text)
        # Empty
        soup_empty = self.get_soup(self.bati_empty.pk)
        self.assertIn("Aucune perspective associée", soup_empty.select_one('[data-qa="perspective-empty"]').text)

    def test_enquetes(self):
        soup = self.get_soup(self.bati.pk)
        self.assertIn("John Doe", soup.select_one('[data-qa="enquete-personne"]').text)
        self.assertIn("2024", soup.select_one('[data-qa="enquete-date-enquete"]').text)
        self.assertIn("2024", soup.select_one('[data-qa="enquete-date-redaction"]').text)
        soup_empty = self.get_soup(self.bati_empty.pk)
        self.assertIn("Aucune enquête associée", soup_empty.select_one('[data-qa="enquete-empty"]').text)

    def test_demande_travaux(self):
        soup = self.get_soup(self.bati.pk)
        self.assertIn("2024", soup.select_one('[data-qa="demande-date"]').text)
        self.assertIn("1234", soup.select_one('[data-qa="demande-numero"]').text)
        self.assertTrue("&#10003;" in str(soup.select_one('[data-qa="demande-autorisation"]')) or "✓" in soup.select_one('[data-qa="demande-autorisation"]').text)
        soup_empty = self.get_soup(self.bati_empty.pk)
        self.assertIn("Aucune demande", soup_empty.select_one('[data-qa="demande-empty"]').text)

    def test_travaux(self):
        soup = self.get_soup(self.bati.pk)
        self.assertIn("2024", soup.select_one('[data-qa="travaux-date"]').text)
        self.assertIn("1000", soup.select_one('[data-qa="travaux-subvention"]').text)
        self.assertIn("5", soup.select_one('[data-qa="travaux-nature"]').text)
        self.assertIn("5", soup.select_one('[data-qa="travaux-usage"]').text)
        soup_empty = self.get_soup(self.bati_empty.pk)
        # if no demande travaux table is not rendered -> check for the parent empty state
        self.assertIn("Aucune demande", soup_empty.text)

    def test_structure(self):
        soup = self.get_soup(self.bati.pk)
        self.assertIn("5", soup.select_one('[data-qa="structure-type"]').text)
        self.assertIn("5", soup.select_one('[data-qa="structure-type-value"]').text)
        self.assertTrue("&#10003;" in str(soup.select_one('[data-qa="structure-remarquable"]')) or "✓" in soup.select_one('[data-qa="structure-remarquable"]').text)
        self.assertIn("5", soup.select_one('[data-qa="structure-conservation"]').text)
        self.assertIn("5", soup.select_one('[data-qa="structure-materiaux-principal"]').text)
        self.assertIn("5", soup.select_one('[data-qa="structure-mise-en-oeuvre"]').text)
        self.assertIn("Structure info", soup.select_one('[data-qa="structure-commentaire"]').text)
        soup_empty = self.get_soup(self.bati_empty.pk)
        self.assertIn("Aucune structure", soup_empty.select_one('[data-qa="structure-empty"]').text)

    def test_structure_finitions(self):
        soup = self.get_soup(self.bati.pk)
        self.assertIn("5", soup.select_one('[data-qa="structure-materiaux-fin"]').text)
        self.assertIn("5", soup.select_one('[data-qa="structure-finition"]').text)
        soup_empty = self.get_soup(self.bati_empty.pk)
        # If no structure, finitions table is not rendered -> check for the parent empty state
        self.assertIn("Aucune structure", soup_empty.text)

    def test_second_oeuvre(self):
        soup = self.get_soup(self.bati.pk)
        self.assertIn("5", soup.select_one('[data-qa="second-type"]').text)
        self.assertIn("5", soup.select_one('[data-qa="second-type-value"]').text)
        self.assertTrue("&#10003;" in str(soup.select_one('[data-qa="second-remarquable"]')) or "✓" in soup.select_one('[data-qa="second-remarquable"]').text)
        self.assertIn("5", soup.select_one('[data-qa="second-conservation"]').text)
        self.assertIn("Second oeuvre comment", soup.select_one('[data-qa="second-commentaire"]').text)
        soup_empty = self.get_soup(self.bati_empty.pk)
        self.assertIn("Aucun élément de second oeuvre", soup_empty.select_one('[data-qa="second-empty"]').text)

    def test_second_oeuvre_finitions(self):
        soup = self.get_soup(self.bati.pk)
        self.assertIn("5", soup.select_one('[data-qa="second-materiaux-fin"]').text)
        self.assertIn("5", soup.select_one('[data-qa="second-finition"]').text)
        soup_empty = self.get_soup(self.bati_empty.pk)
        # If no second oeuvre, finitions table is not rendered -> check for the parent empty state
        self.assertIn("Aucun élément de second oeuvre", soup_empty.text)