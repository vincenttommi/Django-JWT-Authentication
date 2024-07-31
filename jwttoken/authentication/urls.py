from django.urls import path
from .views import Register,login,logout




urlpatterns = [
    path('register/', Register, name='register'),
    path('login/', login,  name='login'),
    path('logout/', logout, name='logout')
]