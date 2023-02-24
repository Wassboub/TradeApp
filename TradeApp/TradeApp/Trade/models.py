from django.db import models

# Create your models here.
class CoinInfo(models.Model):

    symbol = models.CharField(max_length=20)
    Time = models.DateTimeField()
    Ticks = models.IntegerField()
    RelativePriceChange = models.DecimalField(max_digits=20,decimal_places=5)
    TotalPriceChange = models.DecimalField(max_digits=20,decimal_places=5)
    VolumeChange = models.DecimalField(max_digits=20,decimal_places=5)
    LastPrice = models.DecimalField(max_digits=20,decimal_places=5)
    LastVolume = models.DecimalField(max_digits=20,decimal_places=5)
 


class CoinInfo_2(models.Model):

    symbol = models.CharField(max_length=20)
    Time = models.DateTimeField()
    Ticks = models.IntegerField()
    RelativePriceChange = models.DecimalField(max_digits=20,decimal_places=5)
    TotalPriceChange = models.DecimalField(max_digits=20,decimal_places=5)
    VolumeChange = models.DecimalField(max_digits=20,decimal_places=5)
    LastPrice = models.DecimalField(max_digits=20,decimal_places=5)
    LastVolume = models.DecimalField(max_digits=20,decimal_places=5)