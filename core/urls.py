from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('eventos/', views.eventos, name='eventos'),
    path('reunioes/', views.reunioes, name='reunioes'),
    path('missoes/', views.missoes, name='missoes'),
    path('financeiro/', views.financeiro, name='financeiro'),
]
