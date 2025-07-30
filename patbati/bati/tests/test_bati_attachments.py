from django.test import TestCase
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model

from .factories import BatiFactory

User = get_user_model()

class BatiAttachmentsHTMLTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser('testuser', 'test@example.com', 'password')
        cls.bati = BatiFactory()

    def get_soup(self, pk):
        self.client.force_login(self.user)
        response = self.client.get(f'/bati/{pk}/')
        self.assertEqual(response.status_code, 200)
        return BeautifulSoup(response.content, "html.parser")

    def test_carousel_structure(self):
        soup = self.get_soup(self.bati.pk)
        carousel = soup.find("div", {"id": "carouselExampleIndicators"})
        self.assertIsNotNone(carousel)
        self.assertIn("carousel", carousel.get("class", []))
        self.assertIn("slide", carousel.get("class", []))

    def test_carousel_indicators(self):
        soup = self.get_soup(self.bati.pk)
        indicators = soup.select("ol.carousel-indicators li")
        for li in indicators:
            self.assertIn("data-target", li.attrs)
            self.assertIn("data-slide-to", li.attrs)

    def test_carousel_inner_and_items(self):
        soup = self.get_soup(self.bati.pk)
        carousel_inner = soup.find("div", class_="carousel-inner")
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
        soup = self.get_soup(self.bati.pk)
        prev = soup.find("a", class_="carousel-control-prev")
        nxt = soup.find("a", class_="carousel-control-next")
        self.assertIsNotNone(prev)
        self.assertIsNotNone(nxt)
        self.assertIn("data-slide", prev.attrs)
        self.assertIn("data-slide", nxt.attrs)
        self.assertIn("carousel-control-prev-icon", [span.get("class", [None])[0] for span in prev.find_all("span")])
        self.assertIn("carousel-control-next-icon", [span.get("class", [None])[0] for span in nxt.find_all("span")])

    def test_carousel_caption(self):
        soup = self.get_soup(self.bati.pk)
        captions = soup.select("div.carousel-caption")
        for caption in captions:
            h5 = caption.find("h5")
            self.assertIsNotNone(h5)
            self.assertIn("text-light", h5.get("class", []))

    def test_non_image_attachments_list(self):
        soup = self.get_soup(self.bati.pk)
        ul = soup.find("ul", class_="list-unstyled")
        self.assertIsNotNone(ul)
        for li in ul.find_all("li"):
            a = li.find("a")
            self.assertIsNotNone(a)
            img = a.find("img")
            self.assertIsNotNone(img)
            self.assertTrue("src" in img.attrs)
            self.assertTrue("alt" in img.attrs)