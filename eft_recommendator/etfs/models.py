from collections.abc import Iterable
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from .etfutils import risk_rating

# Create your models here.
TERM_CHOICES = [
    ("short", "Less than 2 years"),
    ("mid", "Between 2 and 5 years"),
    ("long", "More than 5 years")]
OBJ_CHOICES = [
    ("safeguard", "My priority is to maintain my capital"),
    ("growth", "My priority is to grow my capital")]
LOSS_ABS_CHOICES = [
    ("low", "This are my life-long savings, I can't afford to loose"),
    ("mid", "I can take some risk, but it has to be moderate"),
    ("high", "I am willing to take higher risks if they lead to higher growth")]

class Etf(models.Model):

    ticker = models.CharField(max_length=10, primary_key=True)
    avg_return = models.FloatField()
    volatility = models.FloatField()
    max_drop = models.FloatField()
    sharpe_ratio = models.FloatField()
    risk_cluster = models.IntegerField()

    class Meta:
        managed = True

    def __str__(self):
        return self.ticker

    def get_absolute_url(self):
        return reverse("etfs:etf_graph", kwargs={"ticker": self.ticker})

class EtfPrice(models.Model):

    date = models.DateField(auto_now=False, auto_now_add=False)
    ticker = models.CharField(max_length=10)
    price = models.FloatField()

    class Meta:
        db_table = "etf_prices"
        managed = False

    def __str__(self):
        return self.ticker

    def get_absolute_url(self):
        return reverse("etfs:etf_graph", kwargs={"ticker": self.ticker})
    
class BasicUser(models.Model):

    email = models.EmailField(max_length=100, unique=True, blank=False)
    name = models.CharField(max_length=100)
    inv_term = models.CharField(max_length=50, choices=TERM_CHOICES)
    inv_objective = models.CharField(max_length=50, choices=OBJ_CHOICES)
    loss_absortion = models.CharField(max_length=50, choices=LOSS_ABS_CHOICES)
    risk_rating = models.IntegerField()
    last_update_date = models.DateTimeField(auto_now=True)
    recommended_etfs = models.ManyToManyField(Etf, related_name="etfs")

    class Meta:
        verbose_name = "BasicUser"
        verbose_name_plural = "BasicUsers"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.risk_rating = risk_rating.get_risk_rating(term=self.inv_term, obj=self.inv_objective, absortion=self.loss_absortion)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("etfs:user_detail", kwargs={"pk": self.pk})
