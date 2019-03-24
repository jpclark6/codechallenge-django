from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Lists
from .serializers import LinksSerializer

class BaseViewTest(APITestCase):
  client = APIClient()

  @staticmethod
  def create_link(link='', slug=''):
    if link != '' and slug != '':
      Link.objects.create(link=link, slug=slug)

  def setUp(self):
    self.create_link('eagle', 'eagle')
    self.create_link('worm', 'worm')
    self.create_link('mongoose', 'mongoose')
    self.create_link('pine', 'pine')

class GetAllLinksTest(BaseViewTest):

  def test_get_all_links(self):
    response = self.client.get(
      reverse("links-all", kwargs={"version": "v1"})
    )
    expected = Links.objects.all()
    serialized = LinksSerializer(expected, many=True)
    self.assertEqual(response.data, serialized.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)