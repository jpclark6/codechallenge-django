from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

from .decorators import validate_request_data
from .models import Links
from .serializers import LinksSerializer


class ListLinksView(generics.ListAPIView):
  queryset = Links.objects.all()
  serializer_class = LinksSerializer

  @validate_request_data
  def post(self, request, *args, **kwargs):
    new_link = Links.objects.create(
      link=request.data["link"],
      slug=request.data["link"],
      clicks = 0,
    )
    return Response(
      data=LinksSerializer(new_link).data,
      status=status.HTTP_201_CREATED
    )


class LinksDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Links.objects.all()
  serializer_class = LinksSerializer

  def get(self, request, *args, **kwargs):
    try:
      link = self.queryset.get(pk=kwargs["pk"])
      serializer = LinksSerializer()
      updated_link = serializer.update(
        link, {'clicks': link.clicks + 1}
      )
      return Response(LinksSerializer(updated_link).data)
    except Links.DoesNotExist:
      return Response(
        data = {
          "error": "Link not found"
        },
        status=status.HTTP_404_NOT_FOUND
      )

  def put(self, request, *args, **kwargs):
    try: 
      link = self.queryset.get(pk=kwargs["pk"])
      serializer = LinksSerializer()
      new_link = request.data['link']
      if(new_link == ''):
        raise ValueError('Empty link title')
      updated_link = serializer.update(link, {'link': new_link, 'slug': new_link})
      return Response(LinksSerializer(updated_link).data)
    except Links.DoesNotExist:
      return Response(
        data={
          "error": "Link not updated"
        },
        status=status.HTTP_400_BAD_REQUEST
      )
    except ValueError:
      return Response(
          data={
              "error": "Link not updated"
          },
          status=status.HTTP_400_BAD_REQUEST
      )

  def delete(self, request, *args, **kwargs):
    try:
      link = self.queryset.get(pk=kwargs["pk"])
      link.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    except Links.DoesNotExist:
      return Response(
        data = {
          "error": "Link not found"
        },
        status=status.HTTP_404_NOT_FOUND
      )
