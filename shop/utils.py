from .models import AddressChipping, Commande, CommandeArticle, Produit
import json


def panier_cookie(request):
    try:
        panier = json.loads(request.COOKIES.get("panier"))
    except:
        panier = {}
    articles = []
    commande = {
        "get_panier_total": 0,
        "get_panier_article": 0,
        "produit_physique": False,
    }
    nombre_article = commande["get_panier_article"]
    try:
        for obj in panier:
            nombre_article += panier[obj]["qte"]
            produit = Produit.objects.get(id=obj)
            total = produit.price * panier[obj]["qte"]
            commande["get_panier_article"] += panier[obj]["qte"]
            commande["get_panier_total"] += total
            article = {
                "produit": {
                    "id": produit.id,
                    "name": produit.name,
                    "price": produit.price,
                    "imageUrl": produit.imageUrl,
                },
                "quantite": panier[obj]["qte"],
                "get_total": total,
            }
            articles.append(article)
            if produit.digital == False:
                commande["produit_physique"] = True
    except:
        pass
    context = {
        "articles": articles,
        "commande": commande,
        "nombre_article": nombre_article,
    }
    return context
