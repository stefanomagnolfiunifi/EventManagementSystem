from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.custom_login_view, name='login'),
    path('register/', views.signup_view, name='signup'),
    path('logout/', views.custom_logout_view, name='logout')
]    
