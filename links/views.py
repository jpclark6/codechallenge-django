from django.shortcuts import render
from rest_framework import generics
from .models import Links
from .serializers import LinksSerializer


class ListLinksView(generics.ListAPIView):
  queryset = Links.objects.all()
  serializer_class = LinksSerializer

# Create your views here.
