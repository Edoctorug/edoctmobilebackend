from django.urls import path
from . import views

urlpatterns = [
    path("auth/",views.auth_user),
    path("register/",views.reg_user),
    path("",views.mainPage)
]