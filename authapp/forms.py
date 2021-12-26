import hashlib
from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django import forms

from authapp.models import ShopUser, ShopUserProfile


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False
        user.activate_key = hashlib.sha1(user.email.encode('utf8')).hexdigest()
        user.activate_key_expired = datetime.now(pytz.timezone(settings.TIME_ZONE))
        user.save()

        return user

    def clean(self):
        errors = []
        age = self.cleaned_data['age']
        username = self.cleaned_data['username']
        forbidden_words = ('admin', 'moderator', 'fluggegecheimen')

        for word in forbidden_words:
            if word in username.lower():
                errors.append(f'Нельзя использовать "{word}" в имени пользователя!')

        if age < 18:
            errors.append(f'{username}, иди делать уроки!')
        elif age > 99:
            errors.append(f'Меня терзают смутные сомнения насчёт возраста, {username}!')

        # не придумал как выводить ошибки над полями ввода (понятно, что не через список)
        # как повлиять на код html тоже не придумал :/ знаки <> в разных кодировках упорно превращаются в мнемонику
        if errors:
            errors = "\n".join(errors)
            raise forms.ValidationError(errors)


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'avatar', 'email', 'age', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean(self):
        errors = []
        age = self.cleaned_data['age']
        username = self.cleaned_data['username']
        forbidden_words = ('admin', 'moderator', 'fluggegecheimen')

        for word in forbidden_words:
            if word in username.lower():
                errors.append(f'Нельзя использовать "{word}" в имени пользователя!')

        if age < 18:
            errors.append(f'{username}, иди делать уроки!')
        elif age > 99:
            errors.append(f'Меня терзают смутные сомнения насчёт возраста, {username}!')

        # не придумал как выводить ошибки над полями ввода (понятно, что не через список)
        # как повлиять на код html тоже не придумал :/ знаки <> в разных кодировках упорно превращаются в мнемонику
        if errors:
            errors = "\n".join(errors)
            raise forms.ValidationError(errors)


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ShopUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = ShopUserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

