from django.urls import path
from . import views

app_name = 'plataform'

urlpatterns = [
    path('', views.ProdutosPage.as_view(), name="index"),
    path('eventos/', views.EventoPage.as_view(), name="eventos"),
    path('eventos/<int:evento_id>/', views.EventoProdutos, name='eventoProdutos'),

    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.logoutView, name='logout'),
    path('cadastro/', views.CadastroUsusario.as_view(), name="cadastro"),
]
