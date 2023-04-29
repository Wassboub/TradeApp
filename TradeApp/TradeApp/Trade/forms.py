from django import forms  
from .models import Coins


class LoginForm(forms.Form):

    username = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control un','placeholder': 'Username', 'style': 'width: 300px;'}))
    password = forms.EmailField(label='',widget=forms.EmailInput(attrs={'class':'form-control pass','placeholder' :'Password','type':'password' ,'style': 'width: 300px;'}))
    
class CoinForm(forms.Form):
    Coin = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control'}))
