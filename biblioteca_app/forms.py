from django import forms
from django.core.exceptions import ValidationError
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


class LibroForm(forms.ModelForm):
    # Se declara aparte para admitir guiones en la entrada (978-84-376-0494-7 = 17 chars).
    # El modelo sigue en 13: clean_isbn quita los guiones antes de guardar.
    isbn = forms.CharField(
        max_length=17,
        label='ISBN',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '13 dígitos, con o sin guiones'}),
    )

    class Meta:
        model = Libro
        fields = [                           # orden = orden en que se pintan en el modal
            'isbn', 'titulo', 'autor',
            'editorial', 'genero',           # FK -> ModelChoiceField -> <select> con el __str__ del modelo
            'precio', 'stock', 'anio_publicacion',
            'descripcion',
        ]
        widgets = {
            'titulo':          forms.TextInput(attrs={'class': 'form-control'}),
            'autor':            forms.TextInput(attrs={'class': 'form-control'}),
            'editorial':        forms.Select(attrs={'class': 'form-select'}),
            'genero':           forms.Select(attrs={'class': 'form-select'}),
            'precio':           forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock':            forms.NumberInput(attrs={'class': 'form-control'}),
            'anio_publicacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion':      forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_isbn(self):
        """Validación propia: Django la llama dentro de is_valid() por el nombre
        clean_<campo>. Lo que devuelve es lo que queda en cleaned_data y se guarda."""
        isbn = self.cleaned_data['isbn'].replace('-', '').replace(' ', '')
        if not isbn.isdigit() or len(isbn) != 13:
            raise ValidationError('El ISBN debe tener exactamente 13 dígitos.')
        return isbn
