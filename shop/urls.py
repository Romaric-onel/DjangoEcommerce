from django.urls import path
from .views import shop, panier, commande, update_article

app_name = "shop"
urlpatterns = [
    path("", shop, name="shop"),
    path("panier/", panier, name="panier"),
    path("commande/", commande, name="commande"),
    path("update_article/", update_article, name = "update_article")
]
