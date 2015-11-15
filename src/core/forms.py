# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup, element
import random
import re

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms
from django.db.models import Q
from django.forms.models import ModelForm

from core.models import Profile, Post
from core.utils.common import notice_admin, process_template, send_html_mail


def sanitizeHTML(value, mode='none'):
    """ Удаляет из value html-теги.
        Если mode==none - все теги
        Если mode==strict - все теги кроме разрешенных
    """
    if mode == 'strict':
        valid_tags = 'p i strong b u a h1 h2 h3 h4 pre br div span img blockquote object param embed iframe ' \
                     'table thead tbody tr td'.split()
    else:
        valid_tags = []

    valid_attrs = 'href src pic user page class text title alt style colspan rowspan rel'.split()
    # параметры видеороликов
    valid_attrs += 'width height classid codebase id name value flashvars webkitallowfullscreen mozallowfullscreen ' \
                   'allowfullscreen allowscriptaccess ' \
                   'quality src type bgcolor base seamlesstabbing swLiveConnect pluginspage data frameborder'.split()

    soup = BeautifulSoup(value.encode('utf8'), from_encoding='utf8')
    for tag in soup.recursiveChildGenerator():
        if isinstance(tag, element.Tag):
            if tag.name in valid_tags:
                tag.attrs = dict((attr, val) for attr, val in tag.attrs.items() if attr in valid_attrs)
            else:
                tag.hidden = True

        elif isinstance(tag, element.Comment):
            tag.extract()

    return soup.renderContents().decode('utf8')


class CommonForm(forms.Form):
    def errors_list(self):
        return [unicode(message) for k, l in self.errors.items() for message in l]

    def str_errors(self, divider='. '):
        return divider.join(self.errors_list())


class RegistrationForm(CommonForm):
    email = forms.EmailField(max_length=100, error_messages={'required': 'Укажите свой email'})
    name = forms.CharField(label='Имя пользователя', required=False)
    login = forms.CharField(label='Логин', required=False,
                            help_text='Поле для отсечения автоматических регистраторов',
                            widget=forms.TextInput(attrs={'class': 'g-hidden'}))
    password1 = forms.CharField(max_length=100, required=False, widget=forms.TextInput)
    password2 = forms.CharField(max_length=100, required=False, widget=forms.TextInput)
    next = forms.CharField(max_length=2000, required=False, widget=forms.HiddenInput)

    def free_credentials(self, s):
        u""" Проверяет строку на емейл, логин или имя пользователя """
        return User.objects.filter(Q(username=s) | Q(email=s) | Q(first_name=s)).count() == 0

    def make_login(self, desired_login=None):
        u""" Генерация логина на основе емейла """
        if desired_login:
            login = desired_login
        elif '@' in self.cleaned_data['email']:
            login = self.cleaned_data['email'][:self.cleaned_data['email'].find('@')]
        else:
            login = self.cleaned_data['email']

        while True:
            if self.free_credentials(login):
                return login

            login += str(random.randint(1, 9))

    def check_login(self, name):
        return re.match('^[\d\w-]+$', name)

    def clean_name(self):
        if self.cleaned_data['name']:
            if self.free_credentials(self.cleaned_data['name']):
                return self.cleaned_data['name']
            else:
                raise forms.ValidationError('Это имя уже занято :(')

    def clean_email(self):
        if self.free_credentials(self.cleaned_data['email']):
            return self.cleaned_data['email']
        else:
            raise forms.ValidationError('В базе уже есть пользователь с введенным email')

    def clean_login(self):
        if len(self.cleaned_data['login']) > 0:
            raise forms.ValidationError('Извините, роботов не регистрируем')

    def generate_password(self):
        vowels = 'euioa'
        consonants = 'qwrtypsdfghjklzxcvbnm'
        digits = '123456789'
        pattern = 'cvcvcdcvcvc'
        return ''.join(random.choice({'v': vowels, 'c': consonants, 'd': digits}[c]) for c in pattern)

    def clean(self):
        if self.errors:
            return self.cleaned_data

        if not self.cleaned_data['name']:
            self.cleaned_data['name'] = self.make_login()

        if self.check_login(self.cleaned_data['name']):
            self.cleaned_data['username'] = self.cleaned_data['name']
        else:
            self.cleaned_data['username'] = self.make_login()

        if self.cleaned_data['password1']:
            p1 = self.cleaned_data['password1']
            p2 = self.cleaned_data['password2']
            if not p1 == p2:
                raise forms.ValidationError('Введенные пароли не одинаковые')
            password = p1
        else:
            password = self.generate_password()

        self.cleaned_data['password'] = password
        return self.cleaned_data

    def save(self):
        new_user = User.objects.create_user(self.cleaned_data['username'],
                                            self.cleaned_data['email'],
                                            self.cleaned_data['password'])
        new_user.is_active = True
        new_user.first_name = self.cleaned_data['name']
        new_user.save()

        Profile.objects.create(user=new_user)

        self.user = authenticate(username=new_user.username, password=self.cleaned_data['password'])

        subject, content = process_template(
            'email/registration.html',
            {
                'user': new_user,
                'form': self
            }
        )
        send_html_mail(subject, content, [self.cleaned_data['email']])


class LoginForm(CommonForm):
    login = forms.CharField(label='Логин', max_length=100)
    passwd = forms.CharField(label='Пароль', max_length=100, widget=forms.PasswordInput)
    next = forms.CharField(max_length=2000, required=False, widget=forms.HiddenInput)

    def get_user(self, s):
        """ Проверяет строку на емейл, логин или имя пользователя """
        return User.objects.get(Q(username=s) | Q(email=s) | Q(first_name=s))

    def clean(self):
        login = self.cleaned_data.get('login', '')
        passwd = self.cleaned_data.get('passwd', '')

        try:
            user = self.get_user(login)
        except User.DoesNotExist:
            raise forms.ValidationError('Логин или пароль не верен')

        auth_user = authenticate(username=user.username, password=passwd)
        if auth_user:
            self.user = auth_user
            return self.cleaned_data
        else:
            raise forms.ValidationError('Логин или пароль не верен')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('board', 'bindings', 'boots', 'riding_style', 'mountains', 'clothes',
                  'equip', 'gender', 'content', 'country', 'city', 'icq')

    def clean(self):
        for f in self._meta.fields:
            if f in self.cleaned_data and self.cleaned_data[f]:
                self.cleaned_data[f] = sanitizeHTML(self.cleaned_data[f])
        return self.cleaned_data


class PostForm(ModelForm):
    title = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'size': '100'}))
    abstract = forms.CharField(label='Анонс', widget=forms.Textarea(attrs={'cols': 100, 'rows': 5}))
    icon = forms.ImageField(label='Картинка')

    def clean_title(self):
        return sanitizeHTML(self.cleaned_data['title'])

    def clean_content(self):
        if not self.cleaned_data['content']:
            raise forms.ValidationError('Введите текст новости.')
        return sanitizeHTML(self.cleaned_data['content'], mode='strict')

    def clean(self):
        if not self.cleaned_data['category']:
            raise forms.ValidationError('Укажите желаемую категорию новости')
        return super(PostForm, self).clean()

    class Meta:
        model = Post
        fields = ('title', 'icon', 'category', 'abstract', 'content')


class FeedbackForm(CommonForm):
    name = forms.CharField(label='Имя', required=False)
    email = forms.EmailField(label='Email', required=False, error_messages={'invalid': 'Введенный email некорректен'})
    message = forms.CharField(label='Сообщение*',
                              error_messages={'required': 'Введите текст сообщения'},
                              widget=forms.Textarea())
    code = forms.CharField(label='Код', required=False, widget=forms.HiddenInput)

    def clean_message(self):
        if '[url=' in self.cleaned_data.get('message', ''):
            raise forms.ValidationError('Spammer detected')
        else:
            return self.cleaned_data.get('message')

    def send(self):
        text = 'Сообщение со страницы обратной связи:<br>'
        if self.cleaned_data['name']:
            text += 'Имя отправителя: "%s"<br>' % self.cleaned_data['name']
        if self.cleaned_data['email']:
            text += 'Обратный адрес: "%s"<br>' % self.cleaned_data['email']
        text += self.cleaned_data['message']
        notice_admin(text, subject='Обратная связь')
