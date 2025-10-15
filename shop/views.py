import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .models import Commande, CommandeArticle, Produit


# Create your views here.
def shop(request, *args, **kwargs):

    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(
            client=client, complete=False
        )

        nombre_article = commande.get_panier_article
    else:
        articles = []
        commande = {"get_panier_total": 0, "get_panier_article": 0}
        nombre_article = commande["get_panier_article"]
    context = {"nombre_article": nombre_article, "produits": Produit.objects.all()}

    return render(request, "index.html", context)


def panier(request, *args, **kwargs):

    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(
            client=client, complete=False
        )

        articles = commande.commandearticle_set.all()  # type: ignore
        nombre_article = commande.get_panier_article
    else:
        articles = []
        commande = {"get_panier_total": 0, "get_panier_article": 0}
        nombre_article = commande["get_panier_article"]
    context = {
        "articles": articles,
        "commande": commande,
        "nombre_article": nombre_article,
    }

    return render(request, "panier.html", context)


def commande(request, *args, **kwargs):
    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(
            client=client, complete=False
        )

        articles = commande.commandearticle_set.all()  # type: ignore
        nombre_article = commande.get_panier_article
    else:
        articles = []
        commande = {"get_panier_total": 0, "get_panier_article": 0}
        nombre_article = commande["get_panier_article"]
    context = {
        "articles": articles,
        "commande": commande,
        "nombre_article": nombre_article,
    }

    return render(request, "commande.html", context)


@login_required()
def update_article(request, *args, **kwargs):
    data = json.loads(request.body)
    produit_id = data["produit_id"]
    action = data["action"]
    produit = Produit.objects.get(id=produit_id)
    client = request.user.client
    commande, created = Commande.objects.get_or_create(client=client, complete=False)
    commande_article, created = CommandeArticle.objects.get_or_create(
        commande=commande, produit=produit
    )

    if commande_article.quantite is None:
        commande_article.quantite = 0
    if action == "add":
        commande_article.quantite += 1
    elif action == "remove":
        commande_article.quantite -= 1

    commande_article.save()

    if commande_article.quantite <= 0:
        commande_article.delete()

    return JsonResponse("Panier modifié", safe=False)
