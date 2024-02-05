from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Estudante, AppConfig, Presenca
from .services import MaquinaAprendizado, ReconhecimentoFace
from .forms import AppConfigForm
# import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone, dateformat
import pytz

# Create your views here.

def home(request):
    print(request.build_absolute_uri()) #optional
    return render(
        request,
        'facerec/home.html'
    )

def sobre(request):
    return HttpResponse("sobre")

def contato(request):
    return HttpResponse("contato")

def treinamento(request):
    ma = MaquinaAprendizado()
    rec = ReconhecimentoFace(ma)
    rec.treinar(Estudante.objects.all())
    estado = 'Sim' if ma.esta_treinada() else 'Não'
    quantidade = str(ma.quantidade_treinada())
    contexto = {}
    contexto['estado'] = estado
    contexto['quantidade'] = quantidade
    print (contexto)
    return render(request, "facerec/presenca.html", contexto)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
def registrar_presenca(request):
    presenca = Presenca()
    try:
        if (request.method == 'POST'):
            presenca.registro = request.POST['individuo'].partition(':')[0]
            presenca.nome_completo = request.POST['individuo'].partition(':')[2]
            presenca.similaridade = request.POST['similaridade']
            presenca.data_hora = dateformat.format(timezone.localtime(timezone.now()), "Y-m-d H:i:s")
            presenca.ip = get_client_ip(request)
            presenca.save()
            status = 'OK'
            mensagem = 'Presença registrada'
        else:
            status = 'NOK'
            mensagem = 'Método requisitado não é um POST. Use uma chamada POST para registrar a presença!'
    except Exception as error:
        status = 'NOK' 
        mensagem = error   

    if status == 'OK':
        data = {
            'status': status,
            'registro': presenca.registro,
            'nome_completo': presenca.nome_completo,
            'similaridade': presenca.similaridade,
            'IP:': presenca.ip,
            'data_hora': str(presenca.data_hora),
            'mensagem':mensagem
        } 
    else:
         data = {
          'status': status, 
          'mensagem': mensagem 
         }   
        
    return JsonResponse(data, status=200)        

def presenca(request):
    ma = MaquinaAprendizado()    
    estado = 'Sim' if ma.esta_treinada() else 'Não'
    quantidade = str(ma.quantidade_treinada())
    contexto = {}
    contexto['estado'] = estado
    contexto['quantidade'] = quantidade
    print (contexto)
    return render(request, "facerec/presenca.html", contexto)

def config(request):
    #template_name = "facerec/configuracoes.html"
    return render(request, "facerec/configuracoes.html")

class AppConfigNovo(CreateView):
    model = AppConfig
    # fields = ["domain", "port", "api_key"]
    form_class = AppConfigForm
    success_url = reverse_lazy("config")

    def form_valid(self, form):        
        form.save()
        return super(AppConfigNovo, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors) 
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        if self.model.objects.first():
            return redirect("config_editar", pk=1)
        else:    
            return super(AppConfigNovo, self).get(request, *args, **kwargs)

class AppConfigEditar(UpdateView):
    model = AppConfig    
    form_class = AppConfigForm
    success_url = reverse_lazy("config")    

class EstudanteLista(ListView):
    model = Estudante    

class EstudanteNovo(CreateView):
    model = Estudante
    fields = ["registro", "nome", "sobrenome", "curso", "semestre_atual"]
    success_url = reverse_lazy("estudante_lista")

class EstudanteEditar(UpdateView):
    model = Estudante
    fields = ["registro", "nome", "sobrenome", "curso", "semestre_atual"]
    success_url = reverse_lazy("estudante_lista")

class EstudanteDeletar(DeleteView):
    model = Estudante
    success_url = reverse_lazy("estudante_lista")    
    
class EstudanteFotoEditar(UpdateView):
    model = Estudante
    fields = ["foto"]
    success_url = reverse_lazy("estudante_lista")

class PresencaLista(ListView):
    model = Presenca
