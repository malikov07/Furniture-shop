from django.urls import path
from .views import LoginView,RegisterView,LogOutView

urlpatterns = [
    path("login/",LoginView.as_view(), name="login" ),
    path("register/",RegisterView.as_view(), name="register" ),
    path("logout/",LogOutView.as_view(), name="logout" ),
]