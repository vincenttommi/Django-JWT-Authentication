from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    #maps the /token/endpoint to the TokenObtainPairView from jwt_views
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    #used to refresh and expired access token by providing a valid refresh token
]
