from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.BasicUser)
admin.site.register(models.Etf)
admin.site.register(models.EtfPrice)