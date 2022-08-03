from django.urls import path
from . import views

app_name = 'plataform'

urlpatterns = [
    path('', views.ProdutosPage.as_view(), name="index"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.logoutView, name='logout'),
    path('cadastro/', views.CadastroUsusario.as_view(), name="cadastro"),
]
