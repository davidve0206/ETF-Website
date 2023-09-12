from collections.abc import Iterable
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from .etfutils import risk_rating

# Create your models here.
class BasicUser(models.Model):

    email = models.EmailField(max_length=100, unique=True, blank=False)
    name = models.CharField(max_length=100)
    inv_term = models.CharField(max_length=50)
    inv_objective = models.CharField(max_length=50)
    loss_absortion = models.CharField(max_length=50)
    risk_rating = models.IntegerField()
    last_update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "BasicUser"
        verbose_name_plural = "BasicUsers"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.risk_rating = risk_rating.get_risk_rating(term=self.inv_term, obj=self.inv_objective, absortion=self.loss_absortion)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("etf:user_results", kwargs={"pk": self.pk})
