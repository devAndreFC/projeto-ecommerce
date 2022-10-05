from django import forms
from django.contrib.auth.models import User
from . import models


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação da senha',
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password', 'password2', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_erros_msgs = {}

        usuario_data = cleaned.get('username')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        email_data = cleaned.get('email')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'email já existe'
        error_msg_password_match = 'Senhas não conferem'
        error_msg_password_short = 'Senha menor que 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatorio'

        if self.usuario:
            if usuario_data != usuario_db.username:
                if usuario_db:
                    validation_erros_msgs['username'] = error_msg_user_exists

            if email_data != email_db.email:
                if email_db:
                    validation_erros_msgs['email'] = error_msg_email_exists

            if password_data:
                if len(password_data) < 6:
                    validation_erros_msgs['password'] = error_msg_password_short

                if password_data != password2_data:
                    validation_erros_msgs['password'] = error_msg_password_match
                    validation_erros_msgs['password2'] = error_msg_password_match
        else:
            if usuario_db:
                validation_erros_msgs['username'] = error_msg_user_exists

            if not password_data:
                validation_erros_msgs['password'] = error_msg_required_field

            if not password2_data:
                validation_erros_msgs['password2'] = error_msg_required_field

            if email_db:
                validation_erros_msgs['email'] = error_msg_email_exists

            if len(password_data) < 6:
                validation_erros_msgs['password'] = error_msg_password_short

            if password_data != password2_data:
                validation_erros_msgs['password'] = error_msg_password_match
                validation_erros_msgs['password2'] = error_msg_password_match

        if validation_erros_msgs:
            raise (forms.ValidationError(
                validation_erros_msgs
            ))
