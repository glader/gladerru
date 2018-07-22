# coding: utf-8

from django.db import models, migrations

from core.utils.common import count_text_len


def count_post_len(apps, schema_editor, with_create_permissions=True):
    Post = apps.get_model('core', 'Post')
    for post in Post.objects.all():
        post.content = post.content.replace('<cut>', '').replace('</cut>', '')
        post.text_len = count_text_len(post.content or '')
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_post_text_len'),
    ]

    operations = [
        migrations.RunPython(count_post_len),
    ]
