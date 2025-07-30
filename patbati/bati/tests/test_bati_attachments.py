from django.test import TestCase
from bs4 import BeautifulSoup

class BatiAttachmentsHTMLTest(TestCase):
    
    with open("patbati/bati/templates/bati/bati_attachments.html") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    def test_carousel_structure(self):
        carousel = self.soup.find("div", {"id": "carouselExampleIndicators"})
        self.assertIsNotNone(carousel)
        self.assertIn("carousel", carousel.get("class", []))
        self.assertIn("slide", carousel.get("class", []))

    def test_carousel_indicators(self):
        indicators = self.soup.select("ol.carousel-indicators li")
        for li in indicators:
            self.assertIn("data-target", li.attrs)
            self.assertIn("data-slide-to", li.attrs)

    def test_carousel_inner_and_items(self):
        carousel_inner = self.soup.find("div", class_="carousel-inner")
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

    def test_carousel_controls(self):
        prev = self.soup.find("a", class_="carousel-control-prev")
        nxt = self.soup.find("a", class_="carousel-control-next")
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

    def test_non_image_attachments_list(self):
        ul = self.soup.find("ul", class_="list-unstyled")
        self.assertIsNotNone(ul)
        for li in ul.find_all("li"):
            a = li.find("a")
            self.assertIsNotNone(a)
            img = a.find("img")
            self.assertIsNotNone(img)
            self.assertTrue("src" in img.attrs)
            self.assertTrue("alt" in img.attrs)

    def test_empty_state_message(self):
        p = self.soup.find("p", class_="text-muted")
        self.assertIsNotNone(p)
        self.assertIn("Aucune pièce jointe disponible", p.text)