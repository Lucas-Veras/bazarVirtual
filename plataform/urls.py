from django.urls import path
from . import views

app_name = 'plataform'

urlpatterns = [
    path('', views.ProdutosPage.as_view(), name="index"),
    path('eventos/', views.EventoPage.as_view(), name="eventos"),
    path('eventos/<int:evento_id>/', views.EventoProdutos, name='eventoProdutos'),
    path('cadastrarevento/', views.CadastroEvento.as_view(), name="cadastroEvento"),

    path('cadastrarevento/', views.CadastroEvento.as_view(), name="cadastroEvento"),
    path('cadastrarproduto/', views.CadastroProduto.as_view(), name="cadastroProduto"),

    path('meuseventos/', views.MeusEventos.as_view(), name="meusEventos"),
    path('meusanuncios/', views.MeusAnuncios.as_view(), name="meusAnuncios"),
    path('minhasreservas/', views.MinhasReservas.as_view(), name="minhasReservas"),

    path("anuncio/<int:produto_id>/", views.deleteAnuncio, name="deleteAnuncio"),
    path("evento/<int:evento_id>/", views.deleteEvento, name="deleteEvento"),

    path("produto/<int:produto_id>/", views.ReservarProduto, name="reservar"),

    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.logoutView, name='logout'),
    path('cadastro/', views.CadastroUsuario.as_view(), name="cadastro"),
]
