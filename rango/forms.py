from django import forms
from rango.models import Tapas, Bares
from django.contrib.auth.models import User
from rango.models import UserProfile

class TapasForm(forms.ModelForm):
    nombre_tapa = forms.CharField(max_length=128, help_text="Por favor introduce el nombre de la tapa.")
    votos = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Tapas
        fields = ('nombre_tapa',)


class BaresForm(forms.ModelForm):
    nombre_bar= forms.CharField(max_length=128, help_text="Por favor introduce el nombre del Bar.")
    direccion = forms.CharField(max_length=200, help_text="Por favor introduce la direccion.")
    n_visitas = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Bares

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('tapa',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
