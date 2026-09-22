from django import forms
from .models import Editorial, Genero, Libro


class EditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial                    # de qué modelo se generan los campos
        fields = ['nombre']                  # cuáles se incluyen (el id nunca va)
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }


class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
