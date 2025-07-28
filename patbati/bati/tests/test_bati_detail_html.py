from django.test import TestCase
from bs4 import BeautifulSoup


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