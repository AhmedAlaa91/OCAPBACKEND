from __future__ import annotations

from django.urls import path

from .views.auth import AuthView

urlpatterns = [
    path('login/', AuthView.login, name='website.login'),
    path('logout/', AuthView.logout, name='website.logout'),
]
