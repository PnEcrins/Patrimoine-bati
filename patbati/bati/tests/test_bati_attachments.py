from django.test import TestCase
from bs4 import BeautifulSoup

class BatiAttachmentsHTMLTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with open("patbati/bati/templates/bati/bati_attachments.html") as fp:
            cls.soup = BeautifulSoup(fp, "html.parser")

    def test_carousel_photos_structure(self):
        carousel = self.soup.find("div", {"id": "carouselPhotos"})
        self.assertIsNotNone(carousel)
        self.assertIn("carousel", carousel.get("class", []))
        self.assertIn("slide", carousel.get("class", []))

    def test_carousel_plans_structure(self):
        carousel = self.soup.find("div", {"id": "carouselPlans"})
        self.assertIsNotNone(carousel)
        self.assertIn("carousel", carousel.get("class", []))
        self.assertIn("slide", carousel.get("class", []))

    def test_carousel_photos_indicators(self):
        indicators = self.soup.select("#carouselPhotos ol.carousel-indicators li")
        for li in indicators:
            self.assertIn("data-target", li.attrs)
            self.assertIn("data-slide-to", li.attrs)

    def test_carousel_plans_indicators(self):
        indicators = self.soup.select("#carouselPlans ol.carousel-indicators li")
        for li in indicators:
            self.assertIn("data-target", li.attrs)
            self.assertIn("data-slide-to", li.attrs)

    def test_carousel_photos_inner_and_items(self):
        carousel_inner = self.soup.select_one("#carouselPhotos .carousel-inner")
        self.assertIsNotNone(carousel_inner)
        items = carousel_inner.find_all("div", class_="carousel-item")
        for item in items:
            self.assertIn("carousel-item", item.get("class", []))
            img = item.find("img")
            self.assertIsNotNone(img)
            self.assertIn("d-block", img.get("class", []))
            self.assertIn("w-100", img.get("class", []))
            self.assertTrue("src" in img.attrs)
            self.assertTrue("alt" in img.attrs)

    def test_carousel_plans_inner_and_items(self):
        carousel_inner = self.soup.select_one("#carouselPlans .carousel-inner")
        self.assertIsNotNone(carousel_inner)
        items = carousel_inner.find_all("div", class_="carousel-item")
        for item in items:
            self.assertIn("carousel-item", item.get("class", []))
            img = item.find("img")
            self.assertIsNotNone(img)
            self.assertIn("d-block", img.get("class", []))
            self.assertIn("w-100", img.get("class", []))
            self.assertTrue("src" in img.attrs)
            self.assertTrue("alt" in img.attrs)

    def test_carousel_photos_controls(self):
        prev = self.soup.select_one("#carouselPhotos a.carousel-control-prev")
        nxt = self.soup.select_one("#carouselPhotos a.carousel-control-next")
        self.assertIsNotNone(prev)
        self.assertIsNotNone(nxt)
        self.assertIn("data-slide", prev.attrs)
        self.assertIn("data-slide", nxt.attrs)
        self.assertIn("carousel-control-prev-icon", [span.get("class", [None])[0] for span in prev.find_all("span")])
        self.assertIn("carousel-control-next-icon", [span.get("class", [None])[0] for span in nxt.find_all("span")])

    def test_carousel_plans_controls(self):
        prev = self.soup.select_one("#carouselPlans a.carousel-control-prev")
        nxt = self.soup.select_one("#carouselPlans a.carousel-control-next")
        self.assertIsNotNone(prev)
        self.assertIsNotNone(nxt)
        self.assertIn("data-slide", prev.attrs)
        self.assertIn("data-slide", nxt.attrs)
        self.assertIn("carousel-control-prev-icon", [span.get("class", [None])[0] for span in prev.find_all("span")])
        self.assertIn("carousel-control-next-icon", [span.get("class", [None])[0] for span in nxt.find_all("span")])

    def test_carousel_caption(self):
        captions = self.soup.select("div.carousel-caption")
        for caption in captions:
            h5 = caption.find("h5")
            self.assertIsNotNone(h5)
            self.assertIn("text-light", h5.get("class", []))

    def test_empty_state_message(self):
        p = self.soup.find("p", class_="text-muted")
        self.assertIsNotNone(p)
        self.assertIn("Aucune pièce jointe disponible", p.text)