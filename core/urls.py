from django.urls import path
from . import views

urlpatterns = [
    # Páginas públicas
    path('', views.index, name='index'),
    path('eventos/', views.eventos, name='eventos'),
    path("cultos/", views.cultos, name="cultos"),
    path('missoes/', views.missoes, name='missoes'),
    path("pedido-oracao/", views.pedido_oracao, name="pedido_oracao"),

    # Painel administrativo e financeiro
    path('financeiro/', views.financeiro, name='financeiro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("membros/", views.membros, name="membros"),
    path("visitantes/", views.visitantes, name="visitantes"),
    path("ministerios/", views.ministerios, name="ministerios"),
    path("anotacao/", views.bloco_notas, name="bloco_notas"),

    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
