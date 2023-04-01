from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required 
from django.shortcuts import HttpResponseRedirect
from Trade.forms import LoginForm
from .models import CoinInfo, CoinInfo_2
from .model_view import Alert
import csv
from datetime import datetime
import os
from binance.client import Client
import random
import string

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
    coinsInfos = CoinInfo.objects.order_by('-Time')[:1500]
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
     if request.method == 'POST':
        form = CoinForm(request.POST)
        if request.POST['Coin'] != "":
            symbol = request.POST['Coin']
            alerts = echo_message(symbol)
            date = datetime.strptime('08/12/2022 18:35',  '%d/%m/%Y %H:%M')
            return render(request, 'home_4_history.html', {"alerts" : alerts , "Symbol": symbol , "date": date,'form': form})
        else:
            return render(request, 'home_4_history.html', {'form': form, 'notif':'Coin not exist'})
     else:
        form = CoinForm(request.POST)
        symbol = "---"
        return render(request, 'home_4_history.html', {'form': form, "Symbol": symbol})
   
   
  
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


def getcoin(coin,path):
    #print("getcoin")
    y = []
    with open(path) as file:
        reader = csv.reader(file)
        for x in reader:
            y.append(str(x).split("\\t"))
    for x in range(len(y)):
        y[x][6] = y[x][6][:len(y[x][6]) - 2]
        y[x][0] = y[x][0][2:]

    return y

def echo_message(message):
       my_list_alerts = []
       list_alerts = []
       #print("echo")
       x=0
       #chatid=message.chat.id
       msg=""
       for s in exchange_info['symbols']:
         if(message.upper()==s['symbol']):
             VALUE=message.upper()
             path = "D:/Perso/Work/Freelance/Django/TradeApp/TradeApp/Trade/data/" + VALUE + ".csv"
             isExist = os.path.exists(path)
             if isExist:
                X = getcoin(VALUE,path)[1:]
                volume24h = []
                k = 288
                ycolne = []
                xclone = []
                for i in range(288, len(X) - 1):
                    volume = 0
                    for j in range(i - k, i - 1):
                        volume = volume + float(X[j][6])

                    volume24h.append(volume)
                alert=[]
                num=0
                yy=[]
                sum1 = 0
                sum2 = 0
                for i in range(288, len(X) - 1):
                    y = float(X[i][6]) / float(volume24h[i - 288])
                    z = ((float(X[i][2]) - float(X[i][4])) / float(X[i][2])) * 100

                    if (z >= 0):
                        sum1 = sum1 + y
                    else:
                        #print(z, "ddddddddd", y)
                        sum2 = sum2 - y
                    if (y > 0.05):
                        alert.append(num + 1)
                        num=num+1
                        xclone.append(X[i][0] + " " + X[i][1])



                        if z >= 0:
                            if(y>=0.15):
                                msg = "" + ("⏳"+str(X[i][0]) + "___" + str(X[i][1]) +"\n"+"📣"+ "alert:"+str(alert[num-1])+"    "+"\N{eyes}"+"\n"+"〽️"+"price:  "  +"+"+ str('%.3f' % z) + "%"+"\n" +"🚨"+ "volume_change:"   +str('%.3f' % (y*100))) +"%"+"🔥"+ "\n"+"********"+"\n"
                                up = True
                                emoji = "🔥"
                            else:
                                msg = "" + ("⏳"+str(X[i][0]) + "___" + str(X[i][1]) + "\n" +"📣"+ "alert:" + str(alert[num - 1]) + "    " + "\N{eyes}" + "\n" + "〽️" +"price:  " + "+" + str('%.3f' % z) + "%" + "\n" +"🚨"+ "volume_change:" + str('%.3f' % (y * 100))) + "%" + "⚡️" + "\n" + "********" + "\n"
                                up = True
                                emoji = "⚡️"
                            ycolne.append(y)
                        else:
                                msg = "" + ("⏳"+str(X[i][0]) + "___" + str(X[i][1]) +"alert"+str(alert[num-1])+"  "+"\N{eyes}"+"\n"+ "\n" + "price:  " + ":" + "-" + str('%.3f' % z) + "%" + "\n" +"🚨" +"volume_change:" + str('%.3f' % (y*100))) +"%"+ "🩸🩸" +"\n" + "********" + "\n"
                                up = False
                                emoji = "🩸🩸"
                                ycolne.append(-y)
                        my_list_alerts.append(msg)
                        time = datetime.strptime(str(X[i][0]) + " " + str(X[i][1]),  '%d/%m/%Y %H:%M:%S')
                        list_alerts.append( Alert(time , alert[num-1] , str('%.3f' % z) , str('%.3f' % (y*100)) ,up, emoji ) )
                        #print(time)

                #print(message)
                #print(msg)

                volume12h = []
                k = 144
                for i in range(144, len(X) - 1):
                    volume = 00
                    for j in range(i - k, i - 1):
                        volume = volume + float(X[j][6])

                    volume12h.append(volume)

                for i in range(144, len(X) - 1):
                    y = float(X[i][6]) / float(volume12h[i - 288])

                    if (y > 0.050):
                        volume12h[i - 288] = 0



                x=1
                break
        #if x==0:
            #print(message)
        #return my_list_alerts
       return list_alerts