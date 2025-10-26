from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("eventos/", views.eventos, name="eventos"),
    path("cultos/", views.cultos, name="cultos"),
    path("missoes/", views.missoes, name="missoes"),
    path("financeiro/", views.financeiro, name="financeiro"),
    path("dashboard/", views.dashboard, name="dashboard"),  
    path("membros/", views.membros, name="membros"),
    path("visitantes/", views.visitantes, name="visitantes"),
    path("ministerios/", views.ministerios, name="ministerios"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # 🔹 Serve mídia mesmo em produção no Render
    from django.views.static import serve
    from django.urls import re_path

    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
