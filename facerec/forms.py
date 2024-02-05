from django import forms
from .models import AppConfig

# class EstudanteImagemForm(forms.ModelForm):

#     class Meta:
#         model = Estudante
#         fields = ["foto"]

class AppConfigForm(forms.ModelForm):
    class Meta:
        model = AppConfig
        fields = ["domain", "port", "api_key"]