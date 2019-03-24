import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Links
from .serializers import LinksSerializer


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
    self.valid_data = {
      "link": "bird",
      "slug": "bird",
      "clicks": 4,
    }
    self.valid_data_post = {
      "link": "bird",
    }
    self.valid_data_post_response = {
      "link": "bird",
      "slug": "bird",
      "clicks": 0,
    }
    self.invalid_data = {
      "link": "",
      "slug": "",
      "clicks": "",
    }
    self.valid_link_id = 1
    self.invalid_link_id = 99

  def make_a_link(self, **kwargs):
    return self.client.post(
        reverse("links-all", kwargs={"version": "v1"}),
        data=json.dumps(kwargs["data"]),
        content_type='application/json',
    )

  def edit_a_link(self, **kwargs):
    return self.client.put(
        reverse("links-detail", kwargs={"version": "v1", "pk": kwargs["id"]}),
        data=json.dumps(kwargs["data"]),
        content_type='application/json',
    )

  def fetch_a_link(self, pk=0):
    return self.client.get(
        reverse("links-detail", kwargs={"version": "v1", "pk": pk})
    )

  def delete_a_link(self, pk=0):
    return self.client.delete(
        reverse("links-detail", kwargs={"version": "v1", "pk": pk})
    )

class GetAllLinksTest(BaseViewTest):
  def test_get_all_links(self):
    response = self.client.get(
      reverse("links-all", kwargs={"version": "v1"})
    )
    expected = Links.objects.all()
    serialized = LinksSerializer(expected, many=True)
    self.assertEqual(response.data, serialized.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetASingleLinkTest(BaseViewTest):
  def test_get_a_link(self):
    expected = Links.objects.all()[0]
    response = self.fetch_a_link(Links.objects.all()[0].id)
    serialized = LinksSerializer(expected)
    self.assertEqual(response.data['link'], serialized.data['link'])
    self.assertEqual(response.data['slug'], serialized.data['slug'])
    self.assertEqual(response.data['clicks'], serialized.data['clicks'] + 1)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    response = self.fetch_a_link(self.invalid_link_id)
    self.assertEqual(
      response.data["error"],
      "Link not found"
    )
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateALinkTest(BaseViewTest):
  def test_create_a_link(self):
    response = self.make_a_link(
      version="v1",
      data=self.valid_data_post,
    )
    self.assertEqual(response.data['link'], self.valid_data_post_response['link'])
    self.assertEqual(response.data['slug'], self.valid_data_post_response['slug'])
    self.assertEqual(response.data['clicks'], self.valid_data_post_response['clicks'])
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    response = self.make_a_link(
      version="v1",
      data=self.invalid_data,
    )
    self.assertEqual(
      response.data["error"],
      "Link not created",
    )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateLinkTest(BaseViewTest):
  def test_update_a_link(self):
    response = self.edit_a_link(
      version="v1",
      data=self.valid_data_post,
      id=Links.objects.all()[0].id,
    )
    self.assertEqual(response.data['link'], self.valid_data_post_response['link'])
    self.assertEqual(response.data['slug'], self.valid_data_post_response['slug'])
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    response = self.edit_a_link(
      version="v1",
      data=self.invalid_data,
      id=Links.objects.all()[1].id,
    )
    self.assertEqual(
      response.data["error"],
      "Link not updated"
    )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteALinkTest(BaseViewTest):
  def test_delete_a_link(self):
    linkId = Links.objects.all()[0].id
    response = self.delete_a_link(linkId)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    response = self.delete_a_link(Links.objects.all()[0].id + 50)
    self.assertEqual(
        response.data["error"],
        "Link not found"
    )
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
