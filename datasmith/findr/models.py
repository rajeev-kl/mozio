from django.contrib.gis.db import models

# Create your models here.


class Provider(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30)
    language = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    provider = models.ForeignKey(Provider, related_name="service_areas", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    geojson = models.PolygonField()

    def __str__(self):
        return f"{self.name} ({self.provider.name})"
