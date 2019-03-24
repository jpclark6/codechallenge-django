from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

from .models import Links
from .serializers import LinksSerializer


class ListLinksView(generics.ListAPIView):
  queryset = Links.objects.all()
  serializer_class = LinksSerializer


class LinksDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Links.objects.all()
  serializer_class = LinksSerializer

  def get(self, request, *args, **kwargs):
    try:
      link = self.queryset.get(pk=kwargs["pk"])
      return Response(LinksSerializer(link).data)
    except Links.DoesNotExist:
      return Response(
        data = {
          "error": "Link not found"
        },
        status=status.HTTP_404_NOT_FOUND
      )