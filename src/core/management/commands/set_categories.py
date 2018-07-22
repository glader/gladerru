# coding: utf-8
from django.core.management.base import NoArgsCommand

from core.models import Post, NewsCategory


class Command(NoArgsCommand):
    def get_category(self, post):
        tags = post.tags.filter(type=30)
        categories = set([tag.category for tag in tags if tag.category])
        priority = ['Экипировка', 'Соревнования', 'Обучение', 'Фото', 'Горы', 'Видео', 'Обзоры']

        for category in categories:
            for title in priority:
                if category.title == title:
                    return category

        return None

    def handle_noargs(self, **options):
        other = NewsCategory.objects.get(title='Обзоры')

        for post in Post.objects.all():
            post.category = self.get_category(post) or other
            post.save()
