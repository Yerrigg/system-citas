from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),  
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),  
    path('perfil/cambiar-password/', views.cambiar_password, name='cambiar_password'),  
]