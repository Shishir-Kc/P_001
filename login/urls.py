from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name="login"
urlpatterns = [
    path('',views.user_login, name="login"),
    path('user/logout',views.user_logout,name="logout"),
    path('user/signup/',views.user_signup,name='signup')
    

]





#  solve the static files not loading problem ! ah its just ned to be serverd by apache 