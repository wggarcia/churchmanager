from django.urls import path
from . import views

urlpatterns = [
    # Páginas públicas
    path('', views.index, name='index'),
    path('eventos/', views.eventos, name='eventos'),
    path("cultos/", views.cultos, name="cultos"),
    path('missoes/', views.missoes, name='missoes'),

    # Painel administrativo e financeiro
    path('financeiro/', views.financeiro, name='financeiro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("anotacao/", views.bloco_notas_site, name="bloco_notas"),

    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

