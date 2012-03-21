# encoding: utf-8

from django import template
from core.models import Movie, Post

register = template.Library()

@register.inclusion_tag("admin/core/movie/announces.html")
def movie_announces(movie_id):
    announces = {'object_id': movie_id}

    try:
        Post.objects.get(type='teaser', item_id=movie_id, item_type=37)
        announces['teaser'] = False
    except Post.DoesNotExist:
        announces['teaser'] = True

    try:
        Post.objects.get(type='full_movie', item_id=movie_id, item_type=37)
        announces['full'] = False
        announces['teaser'] = False
    except Post.DoesNotExist:
        announces['full'] = True

    try:
        Post.objects.get(type='soundtrack', item_id=movie_id, item_type=37)
        announces['soundtrack'] = False
    except Post.DoesNotExist:
        announces['soundtrack'] = True

    return announces