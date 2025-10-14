import json
from django.shortcuts import render

from .models import *

from django.http import JsonResponse

# Create your views here.
def shop(request, *args, **kwargs):

    context = {"produits": Produit.objects.all()}
    return render(request, "index.html", context)


def panier(request, *args, **kwargs):

    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(
            client=client, complete=False
        )

        articles = commande.commandearticle_set.all()  # type: ignore
    else:
        articles = []
        commande = {"get_panier_total": 0, "get_panier_article": 0}
    context = {"articles": articles, "commande": commande}

    return render(request, "panier.html", context)


def commande(request, *args, **kwargs):
    if request.user.is_authenticated:
        client = request.user.client
        commande, created = Commande.objects.get_or_create(
            client=client, complete=False
        )

        articles = commande.commandearticle_set.all()  # type: ignore
    else:
        articles = []
        commande = {"get_panier_total": 0, "get_panier_article": 0}
    context = {"articles": articles, "commande": commande}

   

    return render(request, "commande.html", context)

def update_article(request, *args, **kwargs):
    data = json.loads(request.body)
    Produit_id = data["produit_id"]
    action = data["action"]
#    print(action, Produit_id,data)
    return JsonResponse("Produit modifié", safe=False)