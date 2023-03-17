from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required 
from django.shortcuts import HttpResponseRedirect
from Trade.forms import LoginForm
from .models import CoinInfo, CoinInfo_2
  

@permission_required('is_superuser')
@login_required(login_url="/signin")
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

@login_required(login_url="/signin")
def home_1_scalp(request): 
    coinsInfos = CoinInfo.objects.order_by('-Time')[:3000]
    return render(request, 'home_1_scalp.html', {"coinsInfo" : coinsInfos})

@login_required(login_url="/signin")
def home_2_swing(request): 
    coinsInfos = CoinInfo_2.objects.all().order_by('-Time')
    return render(request, 'home_2_swing.html', {"coinsInfo" : coinsInfos})
   
@login_required(login_url="/signin")
def home_3_btc(request): 
    coinsInfos = CoinInfo_2.objects.all().order_by('-Time')
    return render(request, 'home_3_btc.html', {"coinsInfo" : coinsInfos})

@login_required(login_url="/signin")
def home_4_history(request): 
    coinsInfos = CoinInfo_2.objects.all().order_by('-Time')
    return render(request, 'home_4_history.html', {"coinsInfo" : coinsInfos})
   
   
  
def signin(request):
    if request.user.is_authenticated:
        return render(request, 'home_1_scalp.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            msg = 'Error Login'
            form = LoginForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
  
def profile(request): 
    return render(request, 'profile.html')
   
def signout(request):
    logout(request)
    return redirect('/')
