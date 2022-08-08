from tkinter.tix import Tree
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Produto, Usuario, Evento, Reserva
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse 
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class EmailBackend(ModelBackend):
    def authenticate(request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

class ProdutosPage(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            produtos = Produto.objects.exclude(usuario = request.user.usuario).filter(ehReservado = False)
        else:
            produtos = Produto.objects.exclude(ehReservado = True)
            
        contexto = {'produtos': produtos}
        return render(request, 'index.html', contexto)

class EventoPage(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            eventos = Evento.objects.exclude(usuario_id = request.user.usuario.id)
        else:
            eventos = Evento.objects.all()
        
        contexto = {'eventos': eventos}
        return render(request, 'eventos/index.html', contexto)

def EventoProdutos(request, evento_id):
    evento = Evento.objects.get(id = evento_id)
    produtos = Produto.objects.filter(evento_id = evento_id).exclude(ehReservado = True)
    return render(request, 'eventos/show.html', {'evento': evento ,'produtos': produtos})

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class CadastroEvento(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cadastroEvento/index.html')
    
    def post(self, request, *args, **kwargs):
        nomeEvento = request.POST['nomeEvento']
        descricaoEvento = request.POST['descricaoEvento']

        if nomeEvento and descricaoEvento:
            novoEvento = Evento(usuario=request.user.usuario, nome=nomeEvento, descricao=descricaoEvento)
            novoEvento.save()
            return HttpResponseRedirect(reverse('plataform:meusEventos'))
        else:
            erro = 'Preencha todos os campos'
            return render(request, 'cadatstroEvento/index.html', {'erro': erro})

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class CadastroProduto(View):
    def get(self, request, *args, **kwargs):
        eventos = Evento.objects.all()
        contexto = {'eventos': eventos}
        return render(request, 'cadastroProduto/index.html', contexto)

    def post(self, request, *args, **kwargs):
        eventoId = request.POST['evento']
      #  imagemProduto = request.FILES['imagemProduto']
        nomeProduto = request.POST['nomeProduto']
        descricaoProduto = request.POST['descricaoProduto']
        precoProduto = request.POST['precoProduto']

        try:
            evento = Evento.objects.get(id = eventoId)
            novoProduto = Produto(usuario=request.user.usuario, evento=evento, nome=nomeProduto, descricao=descricaoProduto, preco=precoProduto)# imagem=imagemProduto
            novoProduto.save()
            return HttpResponseRedirect(reverse('plataform:meusAnuncios'))
        except:
            erro = 'Preencha todos os campos corretamente!'
            eventos = Evento.objects.all()
            return render(request, 'cadastroProduto/index.html', {'eventos': eventos, 'erro': erro})

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class MeusEventos(View):
    def get(self, request, *args, **kwargs):
        eventos = Evento.objects.filter(usuario_id = request.user.usuario.id)
        contexto = {'eventos': eventos}
        return render(request, 'meusEventos/index.html', contexto)

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class MeusAnuncios(View):
    def get(self, request, *args, **kwargs):
        produtos = Produto.objects.filter(usuario_id = request.user.usuario.id).filter(ehReservado = False)
        anuncios = Produto.objects.filter(usuario_id = request.user.usuario.id)
        reservados = Reserva.objects.filter(produto__usuario = request.user.usuario)
        contexto = {'anuncios': anuncios, 'reservados': reservados, 'produtos': produtos}
        return render(request, 'meusAnuncios/index.html', contexto)

@method_decorator(login_required(login_url="/login/"), name='dispatch')
class MinhasReservas(View):
    def get(self, request, *args, **kwargs):
        reservas = Reserva.objects.filter(usuario_id = request.user.usuario.id)
        contexto = {'reservas': reservas}
        return render(request, 'minhasReservas/index.html', contexto)

def ReservarProduto(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    produto.ehReservado = True
    produto.save()
    nova_reserva = Reserva(usuario=request.user.usuario, produto=produto)
    nova_reserva.save()
    return redirect('plataform:minhasReservas')  

def deleteAnuncio(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    produto.delete()
    return redirect('plataform:meusAnuncios')

def deleteEvento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    evento.delete()
    return redirect('plataform:meusEventos')

class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login/login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        valuenext= request.POST.get('next')

        user = EmailBackend.authenticate(
            request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if valuenext:
                return redirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect(reverse('plataform:index'))
        else:
            erro = 'Tente novamente! Usuário ou senha incorretos!'
            return render(request, 'login/login.html', {'erro': erro})

def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('plataform:index'))

class CadastroUsuario(View): 
    def get(self, request, *args, **kwargs):
        return render(request, 'login/cadastro.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username):
            erro = 'Usuário já está em uso!'
            return render(request, 'login/cadastro.html', {'erro': erro})
        elif User.objects.filter(email=email):
            erro = 'Email já está em uso!'
            return render(request, 'login/cadastro.html', {'erro': erro})
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            Usuario.objects.create(user=user)
            return HttpResponseRedirect(reverse('plataform:login'))
        
        



