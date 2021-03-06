from django.urls import path
from .views import ListLinksView, LinksDetailView, LinksInfo


urlpatterns = [
    path('links/', ListLinksView.as_view(), name="links-all"),
    path('links/<int:pk>/', LinksDetailView.as_view(), name="links-detail"),
    path('', LinksInfo.as_view())
]
