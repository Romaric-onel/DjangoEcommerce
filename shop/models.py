from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="client"
    )
    name = models.CharField(_("The name of the customer"), max_length=100, null=True)
    models.EmailField(_("The email of the customer"), max_length=254, null=True)

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customer")

    def __str__(self):  # type: ignore
        return self.name


class Category(models.Model):
    name = models.CharField(
        _("The name of the categoty"), max_length=100, null=True, blank=True
    )
    description = models.TextField(
        _("The description of the category"), null=True, blank=True
    )

    def __str__(self):  # type: ignore
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Produit(models.Model):
    category = models.ForeignKey(
        "shop.Category",
        verbose_name=_("The category of the product"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(_("The name of the product"), max_length=100, null=True)
    price = models.DecimalField(
        _("The price of the product"), max_digits=10, decimal_places=2
    )
    digital = models.BooleanField(
        _("Designed if the product is digital or not"), null=True, blank=True
    )
    image = models.ImageField(
        _("The image for the product presentation"),
        null=True,
        blank=True,
        upload_to="shop",
    )
    date_ajout = models.DateTimeField(
        _("The date of the product created"), auto_now_add=True
    )

    def __str__(self):  # type: ignore
        return self.name

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["price"]


class Commande(models.Model):
    client = models.ForeignKey(
        "shop.Client",
        verbose_name=_("the customer who places the order"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date_commande = models.DateField(
        _("The date which the order is placed"), auto_now_add=True
    )
    complete = models.BooleanField(
        _("Designed if the order is completed or not"),
        default=False,
        null=True,
        blank=True,
    )
    status = models.CharField(_("The status of the commande"), max_length=200)
    transaction_id = models.CharField(
        _("The ID of the transaction"), max_length=200, null=True, blank=True
    )
    total_trans = models.DecimalField(
        _("The total price of the transaction"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    @property
    def get_panier_total(self):
        articles = self.commandearticle_set.all()  # type: ignore
        total = sum(article.get_total for article in articles)
        return total

    @property
    def get_panier_article(self):
        articles = self.commandearticle_set.all()  # type: ignore
        total = sum(article.quantite for article in articles)
        return total

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return str(self.id)  # type: ignore


class CommandeArticle(models.Model):
    produit = models.ForeignKey(
        "shop.Produit",
        verbose_name=_("The articles"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    commande = models.ForeignKey(
        "shop.Commande",
        verbose_name=_("The order"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    quantite = models.IntegerField(
        _("The quantity of a article"), null=True, blank=True
    )
    date_added = models.DateTimeField(_("The date who it's added"), auto_now_add=True)

    @property
    def get_total(self):
        total = self.produit.price * self.quantite  # type: ignore
        return total

    class Meta:
        verbose_name = "ItemOrder"
        verbose_name_plural = "ItemOrders"


class AddressChipping(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    commande = models.ForeignKey(
        Commande, on_delete=models.SET_NULL, blank=True, null=True
    )
    addresse = models.CharField(max_length=100, null=True)
    ville = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=100, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # type: ignore
        return self.addresse
