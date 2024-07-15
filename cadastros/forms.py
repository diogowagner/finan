import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='invalid'
        )

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        required=True,
        label = 'Senha',
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'placeholder': 'Digite sua senha.'
        }),
        help_text=(
            'A senha deve conter no mínimo 8 caracteres '
            'uma palavra maíuscula e um número. '
        ),
        validators=[strong_password]
    )

    password2 = forms.CharField(
        required=True,
        label = 'Repita a senha',
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'placeholder': 'Repita sua senha'
        })
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "form-control"}),
            'last_name': forms.TextInput(attrs={'class': "form-control"}),
            'username': forms.TextInput(attrs={'class': "form-control"}),
            'email': forms.EmailInput(attrs={'class': "form-control"}),
            'password': forms.PasswordInput(attrs={
                'class': "form-control",
                'placeholder': "Digite sua senha",
                }),
        }

        def clean(self):
            cleaned_data = super().clean()

            password = cleaned_data.get('password')
            password2 = cleaned_data.get('password2')

            if password != password2:
                password_confirmation_error = ValidationError(
                    'A senha e a senha2 não são iguais.',
                    code='invalid'
                )
                raise ValidationError({
                    'password': password_confirmation_error,
                    'password2': [
                        password_confirmation_error,
                    ],
                })