from django.forms import ModelForm, TextInput
from .models import City
from django.core.validators import ValidationError

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Название города'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if name[0].islower():
            raise ValidationError('Название не должно начинаться с маленькой буквы')
        return name