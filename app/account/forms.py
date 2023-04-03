import uuid

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.forms import SetPasswordForm

User = get_user_model()


class UserSignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2'
        )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError('Passwords should match!')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password1']
        user.is_active = False
        user.username = uuid.uuid4()
        user.set_password(password)
        user.save()

        self.send_email()

        return user

    def send_email(self):
        from django.core.mail import send_mail
        subject = 'Thank You for sign up!'
        path = reverse('account:activate', args=(self.instance.username,))
        message = f'''
            {settings.HTTP_SCHEMA}://{settings.HOST}{path}
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.instance.email],
            fail_silently=False,
        )


class UserPasswordChangeForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
