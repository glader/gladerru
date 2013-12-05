# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup, element
import urllib
import random
from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import *
from django.db.models import Q

from core.models import Profile, Post, Tag, Photo, Movie, Discount, Comment, Mountain, Avatar, NewsCategory
from core.utils.common import notice_admin, process_template, send_html_mail


def sanitizeHTML(value, mode='none'):
    """ Удаляет из value html-теги.
        Если mode==none - все теги
        Если mode==strict - все теги кроме разрешенных
    """
    if mode == 'strict':
        valid_tags = 'p i strong b u a h1 h2 h3 h4 pre br div span img blockquote glader cut object param embed'.split()
    else:
        valid_tags = []

    valid_attrs = 'href src pic user page class text title alt'.split()
    # параметры видеороликов
    valid_attrs += 'width height classid codebase id name value flashvars allowfullscreen allowscriptaccess quality src type bgcolor base seamlesstabbing swLiveConnect pluginspage data frameborder'.split()

    soup = BeautifulSoup(value.encode('utf8'), from_encoding='utf8')
    for tag in soup.recursiveChildGenerator():
        if isinstance(tag, element.Tag):
            if tag.name in valid_tags:
                tag.attrs = dict((attr, val) for attr, val in tag.attrs.items()
                             if attr in valid_attrs)
            else:
                tag.hidden = True

        elif isinstance(tag, element.Comment):
            tag.extract()

    result = soup.renderContents().decode('utf8')
    return re.sub('</(glader|cut)>', '', result)


class CommonForm(Form):
    def errors_list(self):
        return [unicode(message) for k, l in self.errors.items() for message in l]

    def str_errors(self, divider=u". "):
        return divider.join(self.errors_list())


class RegistrationForm(CommonForm):
    email = EmailField(max_length=100, error_messages={'required': u'Укажите свой email'})
    name = CharField(label=u'Имя пользователя', required=False)
    login = CharField(label=u'Логин', required=False, help_text=u'Поле для отсечения автоматических регистраторов',
                      widget=TextInput(attrs={'class': 'g-hidden'}))
    password1 = CharField(max_length=100, required=False, widget=PasswordInput)
    password2 = CharField(max_length=100, required=False, widget=PasswordInput)
    retpath = CharField(max_length=2000, required=False, widget=HiddenInput)

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
                raise ValidationError(u'Это имя уже занято :(')

    def clean_email(self):
        if self.free_credentials(self.cleaned_data['email']):
            return self.cleaned_data['email']
        else:
            raise ValidationError(u'В базе уже есть пользователь с введенным email')

    def clean_login(self):
        if len(self.cleaned_data['login']) > 0:
            raise ValidationError(u'Извините, роботов не регистрируем')

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
                raise ValidationError(u'Введенные пароли не одинаковые')
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

        subject, content = process_template('email/registration.html', {
                                                        'user': new_user,
                                                        'form': self
                                                    })
        send_html_mail(subject, content, [self.cleaned_data['email']])


class LoginForm(CommonForm):
    login = CharField(label=u'Логин', max_length=100)
    passwd = CharField(label=u'Пароль', max_length=100, widget=PasswordInput)
    retpath = CharField(max_length=2000, required=False, widget=HiddenInput)

    def get_user(self, s):
        u""" Проверяет строку на емейл, логин или имя пользователя """
        return User.objects.get(Q(username=s) | Q(email=s) | Q(first_name=s))

    def clean(self):
        login = self.cleaned_data.get('login', '')
        passwd = self.cleaned_data.get('passwd', '')

        try:
            user = self.get_user(login)
        except User.DoesNotExist:
            raise ValidationError(u'Логин или пароль не верен')

        auth_user = authenticate(username=user.username, password=passwd)
        if auth_user:
            self.user = auth_user
            return self.cleaned_data
        else:
            raise ValidationError(u'Логин или пароль не верен')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('board', 'bindings', 'boots', 'riding_style', 'mountains', 'clothes',
                  'equip', 'gender', 'content', 'country', 'city', 'icq')

    def clean(self):
        for f in self._meta.fields:
            if f in self.cleaned_data and self.cleaned_data[f]:
                self.cleaned_data[f] = sanitizeHTML(self.cleaned_data[f])
        return self.cleaned_data


class AvatarForm(CommonForm):
    avatar = ImageField(error_messages={'required': u'Укажите файл с аватаром',
                                        'invalid': u'Файл поврежден или не является картинкой'})

    def save(self, user):
        Avatar.add(user, self.cleaned_data['avatar'])


class OpenMultipleChoiceField(MultipleChoiceField):
    def validate(self, *args, **kwargs):
        pass


class PostForm(CommonForm):
    post = IntegerField(label=u'Пост', required=False, widget=HiddenInput, help_text=u'Пост')
    title = CharField(label=u'Заголовок', error_messages={'required': u'Введите заголовок поста'},
                      widget=TextInput(attrs={'class': 'input'}))
    category = IntegerField(label=u'Категория', widget=Select, help_text=u'Категория')
    content = CharField(label=u'Сообщение', error_messages={'required': u'Введите текст поста'},
                        widget=Textarea(attrs={'class': 'content'}))
    geography = BooleanField(label=u'Относится к моему городу', required=False)
    #tags = CharField(label=u'Теги', required=False,
    #                  widget=TextInput(attrs={'class':'tags'}))
    tags = OpenMultipleChoiceField(choices=[], required=False, initial=[])

    #Картинка
    picture = ImageField(label=u'Картинка', required=False,
                         widget=FileInput(attrs={'class': 'picture'}))

    deferred_date = DateField(label=u"Дата публикации", required=False, initial=datetime.now().date)
    deferred_time = TimeField(label=u"Время публикации", required=False, initial=datetime.now().time)

    event_date_start = DateField(label=u"Дата события", required=False, widget=DateInput(attrs={'class': 'vDateField'}))
    event_date_finish = DateField(label=u"Дата окончания события", required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.post = kwargs.pop('post')

        super(PostForm, self).__init__(*args, **kwargs)

        self.fields['category'].widget.choices = [(c.id, c.title) for c in NewsCategory.objects.all()]

        if 'initial' in kwargs:
            self.fields['tags'].choices = [(t, t) for t in kwargs['initial']['tags']]

    def clean_post(self):
        if not self.cleaned_data['post']:
            return None
        try:
            post = Post.all.get(id=self.cleaned_data['post'])
            author = post.author
            if author == self.user or self.user.get_profile().is_moderator:
                return post
            raise ValidationError(u'Вы не можете редактировать чужие сообщения.')

        except Post.DoesNotExist:
            raise ValidationError(u'Редактирование неизвестного поста.')
        except IndexError:
            raise ValidationError(u'Ошибка в посте, сообщите администрации.')

    def clean_title(self):
        return sanitizeHTML(self.cleaned_data['title'])

    def clean_category(self):
        try:
            return NewsCategory.objects.get(pk=self.cleaned_data['category'])
        except NewsCategory.DoesNotExist:
            raise ValidationError(u"Неизвестная категория")

    def clean_content(self):
        if self.user.get_profile().is_moderator:
            return self.cleaned_data['content']
        else:
            return sanitizeHTML(self.cleaned_data['content'], mode='strict')

    def clean_tags(self):
        tags_str = u",".join(self.cleaned_data['tags'])
        return Tag.process_tags(sanitizeHTML(tags_str))

    def clean(self):
        self.cleaned_data['deferred_datetime'] = None

        if self.cleaned_data.get('deferred_date') and \
           self.cleaned_data.get('deferred_time'):
                deferred_datetime = datetime.combine(self.cleaned_data['deferred_date'],
                                                     self.cleaned_data['deferred_time'])
                if deferred_datetime >= datetime.now():
                    self.cleaned_data['deferred_datetime'] = deferred_datetime

        return self.cleaned_data


class PictureForm(CommonForm):
    """ Форма для заливки картинок через swfupload """
    Filedata = ImageField(label=u'Картинка')


class PostCommentForm(CommonForm):
    post = CharField(label=u'Пост', error_messages={'required': u'Отсутствует код поста'})
    klass = CharField(label=u'Тип элемента', error_messages={'required': u'Отсутствует тип элемента'})
    comment = IntegerField(label=u'Родительский комментарий', required=False)
    content = CharField(label=u'Сообщение')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PostCommentForm, self).__init__(*args, **kwargs)

    def clean_content(self):
        content = urllib.unquote(self.cleaned_data['content'])
        if self.user.get_profile().is_moderator:
            return content
        else:
            return sanitizeHTML(content, mode='strict')

    def clean_comment(self):
        if not self.cleaned_data['comment']:
            return None
        try:
            return Comment.objects.get(pk=self.cleaned_data['comment'])
        except Comment.DoesNotExist:
            raise ValidationError(u'Неизвестный комментарий')

    def clean(self):
        klass = {'photo': Photo,
                 'movie': Movie,
                 'mountain': Mountain,
                 'item': Post}.get(self.cleaned_data['klass'], Post)
        try:
            post = klass.objects.get(pk=self.cleaned_data['post'])
        except klass.DoesNotExist:
            raise ValidationError(u'Неизвестное сообщение')

        self.cleaned_data['post'] = post
        return self.cleaned_data


class PostVoteForm(CommonForm):
    """ Голосование за пост """
    post = CharField(label=u'Сообщение', error_messages={'required': u'Отсутствует код поста'})
    klass = CharField(label=u'Тип элемента', error_messages={'required': u'Отсутствует тип элемента'})
    vote = IntegerField(label=u'Оценка', error_messages={'required': u'Отсутствует оценка поста'})

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PostVoteForm, self).__init__(*args, **kwargs)

    def clean_vote(self):
        vote = self.cleaned_data['vote']
        if not (self.user.get_profile().is_moderator or (vote == 1)):
            raise ValidationError(u'Неправильная оценка')

        return vote

    def clean(self):
        klass = {'post': Post, 'photo': Photo, 'mountain': Mountain, 'movie': Movie}.get(self.cleaned_data['klass'], None)
        try:
            post = klass.objects.get(pk=self.cleaned_data['post'])
        except klass.DoesNotExist:
            raise ValidationError(u'Голосование за неизвестный пост')

        if not post.can_vote(self.user):
            raise ValidationError(u'Вы не можете голосовать за этот пост')

        self.cleaned_data['post'] = post
        return self.cleaned_data


class CommentForm(CommonForm):
    comment = IntegerField(label=u'Комментарий', error_messages={'required': u'Отсутствует код комментария'})

    def clean_comment(self):
        try:
            return Comment.objects.get(pk=self.cleaned_data['comment'])
        except Comment.DoesNotExist:
            raise ValidationError(u'Неизвестный комменатрий')


class CommentVoteForm(CommentForm):
    """ Голосование за комментарий """
    vote = IntegerField(label=u'Оценка', error_messages={'required': u'Отсутствует оценка комментария'})

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CommentVoteForm, self).__init__(*args, **kwargs)

    def clean_vote(self):
        vote = self.cleaned_data['vote']
        if not (self.user.get_profile().is_moderator or (vote == 1)):
            raise ValidationError(u'Неправильная оценка')

        return vote

    def clean(self):
        if not self.cleaned_data['comment'].can_vote(self.user):
            raise ValidationError(u'Вы не можете голосовать за этот комменатрий')

        return self.cleaned_data


class FeedbackForm(CommonForm):
    name = CharField(label=u'Имя', required=False)
    email = EmailField(label=u'Email', required=False, error_messages={'invalid': u'Введенный email некорректен'})
    message = CharField(label=u'Сообщение*',
                        error_messages={'required': u'Введите текст сообщения'},
                        widget=Textarea())
    code = CharField(label="Код", required=False, widget=HiddenInput)

    def clean_message(self):
        if '[url=' in self.cleaned_data.get('message', ''):
            raise ValidationError('Spammer detected')
        else:
            return self.cleaned_data.get('message')

    def send(self):
        text = u"Сообщение со страницы обратной связи:<br>"
        if self.cleaned_data['name']:
            text += u"Имя отправителя: '%s'<br>" % self.cleaned_data['name']
        if self.cleaned_data['email']:
            text += u"Обратный адрес: '%s'<br>" % self.cleaned_data['email']
        text += self.cleaned_data['message']
        notice_admin(text, subject=u"Обратная связь")


class PhotoForm(CommonForm):
    title = CharField(label=u'Название', required=False, widget=TextInput(attrs={'size': '60'}))
    tags = CharField(label=u'Теги', required=False, widget=TextInput(attrs={'size': '70'}))

    def __init__(self, *args, **kwargs):
        self.photo = kwargs.pop('photo')
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['title'].initial = self.photo.title
        self.fields['tags'].initial = ", ".join(t.title for t in self.photo.tags.all())

    def clean_title(self):
        return sanitizeHTML(self.cleaned_data['title'])

    def clean_tags(self):
        return Tag.process_tags(sanitizeHTML(self.cleaned_data['tags']))

    def save(self):
        self.photo.title = self.cleaned_data['title']
        self.photo.tags.clear()
        self.photo.tags.add(*self.cleaned_data['tags'])
        self.photo.rebuild_tags()


class DiscountForm(ModelForm):
    class Meta:
        model = Discount
        exclude = ('user', 'date_created')

    def __init__(self, *args, **kwargs):
        super(DiscountForm, self).__init__(*args, **kwargs)
        for f in self.base_fields.values():
            f.error_messages['required'] = u"Это поле обязательно для заполнения"
