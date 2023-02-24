from django.contrib import admin
from django.urls import path
from Trade import views
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_1_scalp, name='home_1_scalp'),
    path('signin/',views.signin, name='signin'),
    path('signout/',views.signout, name='signout'),
    path('signup/',views.signup, name='signup'),
    path('profile/',views.profile, name='profile'),
    path('home_1_scalp/',views.home_1_scalp, name='home_1_scalp'),
    path('home_2_swing/',views.home_2_swing, name='home_2_swing'),
    path('home_3_btc/',views.home_3_btc, name='home_3_btc'),
    path('home_4_history/',views.home_4_history, name='home_history'),




]