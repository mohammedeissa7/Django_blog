from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views

# urls.py
from django.contrib.auth.views import LogoutView

class InsecureLogoutView(LogoutView):
    http_method_names = ['get', 'post']  # Allow GET



app_name = 'users'
urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', InsecureLogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
]



