from django.urls import path
from .views import ListLinksView


urlpatterns = [
    path('links/', ListLinksView.as_view(), name="links-all")
]
