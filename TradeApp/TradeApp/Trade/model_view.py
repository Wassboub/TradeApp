import decimal
from click import DateTime

# Create your models here.
class Alert():

    Numero = int()
    Time = DateTime()
    Price = decimal.Decimal()
    VolumeChange = decimal.Decimal()
    Up = bool()
    Emoji = ""


    def __init__(self,Time, Numero, Price, VolumeChange, Up, Emoji,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.Time = Time
        self.Numero = Numero
        self.Price = Price
        self.VolumeChange = VolumeChange
        self.Up = Up
        self.Emoji = Emoji



