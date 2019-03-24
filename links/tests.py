from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Links
from .serializers import LinksSerializer

class BaseViewTest(APITestCase):
  client = APIClient()

  @staticmethod
  def create_link(link='', slug='', clicks=3):
    if link != '' and slug != '':
      Links.objects.create(link=link, slug=slug, clicks=clicks)

  def setUp(self):
    self.create_link('eagle', 'eagle', 4)
    self.create_link('worm', 'worm', 2)
    self.create_link('mongoose', 'mongoose', 3)
    self.create_link('pine', 'pine', 6)


class LinksModelTest(APITestCase):
  def setUp(self):
    self.a_link = Links.objects.create(
      link="eagle",
      slug="eagle",
      clicks=3,
    )

  def test_link(self):
    self.assertEqual(self.a_link.link, "eagle")
    self.assertEqual(self.a_link.slug, "eagle")
    self.assertEqual(self.a_link.clicks, 3)

class GetAllLinksTest(BaseViewTest):

  def test_get_all_links(self):
    response = self.client.get(
      reverse("links-all", kwargs={"version": "v1"})
    )
    expected = Links.objects.all()
    serialized = LinksSerializer(expected, many=True)
    self.assertEqual(response.data, serialized.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)