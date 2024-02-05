from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
import django.utils

# Onde armazenar as imagens
def image_full_path(instance, filename): 
    return 'user_{0}/{1}'.format(instance.registro, filename) 

# Modelo de dados do estudante

class Estudante(models.Model):
    class SemestreEnum (models.IntegerChoices):
        S1 = 1, "Semestre 1"
        S2 = 2, "Semestre 2"
        S3 = 3, "Semestre 3"
        S4 = 4, "Semestre 4"
        S5 = 5, "Semestre 5"
        S6 = 6, "Semestre 6"
        S7 = 7, "Semestre 7"
        S8 = 8, "Semestre 8"
        S9 = 9, "Semestre 9"
        S10 = 10, "Semestre 10"
        S11 = 11, "Semestre 11"
        S12 = 12, "Semestre 12"
        S13 = 13, "Semestre 13"
        S14= 14, "Semestre 14"
        S15 = 15, "Semestre 15"
        
    registro = models.IntegerField(primary_key=True, null=False)
    nome = models.CharField(max_length=200, null=False)
    sobrenome = models.CharField(max_length=200, null=False)
    curso = models.CharField(max_length=200, null=False)
    semestre_atual = models.IntegerField(default=1,choices=SemestreEnum.choices)
    foto = models.ImageField(upload_to=image_full_path, blank=True)

    def __str__(self):
        return str(self.registro).concat(" - ").concat(self.nome).concat(" - ").concat(self.sobrenome)

    def get_absolute_url(self):
        return reverse('estudante_editar', kwargs={'pk': self.pk})

class AppConfig(models.Model):
    domain = models.CharField(max_length=200,blank=True, default="") #'http://192.168.0.184'
    port = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(65535)], default=8000) #'8000'
    api_key = models.CharField(max_length=200, blank=True, default="") #'981e2935-72ee-4505-b8e4-61b01de3662d'

    # def __init__(self, domain:str, port:int, api_key:str) -> None:
    #     self.domain = domain
    #     self.port = port
    #     self.api_key = api_key

    def get_domain(self) -> str:
        return self.domain

    def get_port(self) -> int:
        return self.port

    def get_api_key(self) -> str:
        return self.api_key
    
    def __str__(self):
        return self.get_domain() + ":" + str(self.get_port())
    
    def get_absolute_url(self):
        return reverse('config_editar', kwargs={'pk': self.pk})
    
class Presenca(models.Model):
    registro = models.IntegerField(null=False)
    nome_completo = models.CharField(max_length=200, null=False)
    similaridade = models.FloatField(null=False, default=0.0)
    ip = models.GenericIPAddressField(null=False)
    data_hora = models.DateTimeField(default=django.utils.timezone.now, null=False)

    def __str__(self):
        return str(self.registro).concat(" - ").concat(self.nome).concat(" - ").concat(self.sobrenome)
