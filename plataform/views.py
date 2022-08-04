from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Produto, Usuario, Evento
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import login, logout, get_user_model

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
        produtos = Produto.objects.all()
        contexto = {'produtos': produtos}
        return render(request, 'index.html', contexto)

class EventoPage(View):
    def get(self, request, *args, **kwargs):
        eventos = Evento.objects.all()
        contexto = {'eventos': eventos}
        return render(request, 'eventos/index.html', contexto)

def EventoProdutos(request, evento_id):
    evento = Evento.objects.get(id = evento_id)
    produtos = Produto.objects.filter(evento_id = evento_id)
    return render(request, 'eventos/show.html', {'evento': evento ,'produtos': produtos})

class CadastroEvento(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cadastroEvento/index.html')
    
    def post(self, request, *args, **kwargs):
        nomeEvento = request.POST['nomeEvento']
        descricaoEvento = request.POST['descricaoEvento']

        if nomeEvento and descricaoEvento:
            novoEvento = Evento(usuario=request.user.usuario, nome=nomeEvento, descricao=descricaoEvento)
            novoEvento.save()
            return HttpResponseRedirect(reverse('plataform:eventos'))
        else:
            erro = 'Preencha todos os campos'
            return render(request, 'cadatstroEvento/index.html', {'erro': erro})
        
class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login/login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

        user = EmailBackend.authenticate(
            request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('plataform:index'))
        else:
            erro = 'Tente novamente! Email ou senha incorretos!'
            return render(request, 'login/login.html', {'erro': erro})

def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('plataform:index'))

class CadastroUsusario(View): 
    def get(self, request, *args, **kwargs):
        return render(request, 'login/cadastro.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if username and email and password:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            Usuario.objects.create(user=user)
            return HttpResponseRedirect(reverse('plataform:login'))
        else:
            erro = 'Informe corretamente os parâmetros necessários!'
            # inserir condição de error no template
            return render(request, 'login/cadastro.html', {'erro': erro})



        
        



