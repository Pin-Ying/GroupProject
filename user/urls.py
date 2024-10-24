"""
URL configuration for djangoDEMO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from . import views
from django.urls import path

urlpatterns = [
    # path("", views.index),
    path("", views.user_profile, name="profile"),
    path("login/", views.user_login, name="login"),
    path("register/", views.user_register, name="register"),
    # path("a4/", views.a4, name="a4"),
    path("logout/", views.user_logout, name="logout"),
]
