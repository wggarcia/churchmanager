from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("membros/", views.membros, name="membros"),
    path("eventos/", views.eventos, name="eventos"),
    path("visitantes/", views.visitantes, name="visitantes"),
    path("reunioes/", views.reunioes, name="reunioes"),
    path("missoes/", views.missoes, name="missoes"),
    path("financeiro/", views.financeiro, name="financeiro"),  # restrito
]
