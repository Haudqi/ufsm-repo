from django.urls import path
from facerec import views

from .views import LimparPresencasView


urlpatterns = [
    path("",views.home, name="home"),
    path("sobre/",views.sobre, name="sobre"),
    path("contato/",views.contato, name="contato"),
    path("estudantes/", views.EstudanteLista.as_view(template_name="facerec/estudante_lista.html"), name="estudante_lista"),
    path("estudantes/add", views.EstudanteNovo.as_view(template_name="facerec/estudante_form.html"), name="estudante_novo"),
    path("estudantes/edit/<int:pk>", views.EstudanteEditar.as_view(template_name="facerec/estudante_form.html"), name="estudante_editar"),
    path("estudantes/delete/<int:pk>", views.EstudanteDeletar.as_view(), name="estudante_deletar"),
    #path("estudantes/",views.estudantes, name="estudantes"),
    path("presenca/",views.presenca, name="presenca"),
    path("presencas/",views.PresencaLista.as_view(template_name="facerec/presenca_lista.html"), name="presenca_lista"),
    path('limpar_presencas/', LimparPresencasView.as_view(), name='limpar_presencas'),
    path("treinamento/",views.treinamento, name="treinamento"),
    path("estudantes/upload/<int:pk>", views.EstudanteFotoEditar.as_view(template_name="facerec/estudante_upload_imagem.html"), name="upload_imagem"),
    path("config/",views.config, name="config"),
    path("config/add",views.AppConfigNovo.as_view(template_name="facerec/appconfig_form.html"), name="config_novo"),
    path("config/edit/<int:pk>",views.AppConfigEditar.as_view(template_name="facerec/appconfig_form.html"), name="config_editar"),
    path("api/registrar",views.registrar_presenca, name="registrar_presenca")
]