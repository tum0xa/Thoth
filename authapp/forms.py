from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms.widgets import TextInput
from authapp.models import SystemUser
import random
import hashlib


class ModularTextInput(TextInput):
    template_name = 'authapp/widgets/modular_text_input.html'


class LoginForm(AuthenticationForm):
    class Meta:
        model = SystemUser
        fields = ('username', 'password')

    username = forms.CharField(widget=ModularTextInput)

    # def __init__(self, *args, **kwargs):
    #     super(LoginForm, self).__init__(*args, **kwargs)
        # for field_name, field in self.fields.items():
        #     if field_name == 'username':
        #         field.widget.attrs['class'] = 'form-control underlined'
        #         field.widget.attrs['placeholder'] = ''



class RegisterForm(UserCreationForm):
    class Meta:
        model = SystemUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'avatar')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'col-md-12 col-12'
            field.help_text = ''

    # def clean_age(self):
    #     data = self.cleaned_data['age']
    #     if data < 18:
    #         raise forms.ValidationError("Вы слишком молоды!")

        # return data

    def save(self):
        user = super(RegisterForm, self).save()

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class EditForm(UserChangeForm):
    class Meta:
        model = SystemUser
        # fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password')
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")
        return data
