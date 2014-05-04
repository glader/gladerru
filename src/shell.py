from django.core.management import setup_environ
import settings
from urllib2 import urlopen
from StringIO import StringIO
setup_environ(settings)
from core.models import *
import re

"""
for post in Post.objects.filter(name__isnull=False):
    match = re.search("src=.([^\"\']+)", post.content or "")
    if match:
        print post.id, match.groups()

        #for url in match.groups():

            #if 'thumbnail' in url:
             #   continue

            #if '/media/data' in url:
            #    print post.id, post.name, url.encode('utf8')

            #print post.id, post.name, url.encode('utf8')
"""

av_log = open('av_log').read().split('\n')


class F(StringIO):
    pass

for p in Profile.objects.filter(avatar=True):
    if str(p.user_id) in av_log:
        continue

    try:
        avatars = {}
        for size in (128, 64, 32, 16):
            url = "http://glader.ru/media/%s%s/avatar%s.jpg" % (settings.USERPIC_URL, p.user.username, size)

            print p.user_id, url,
            content = urlopen(url).read()

            print "read"

            avatars[size] = F(content)
            avatars[size].name = '%s_avatar_%s' % (p.user.username, size)
            avatars[size].size = 1
            avatars[size].file = content

        avatar = Avatar()
        avatar.user = p.user
        avatar.avatar128.save('avatar_128', avatars[128])
        avatar.avatar64.save('avatar_64', avatars[64])
        avatar.avatar32.save('avatar_32', avatars[32])
        avatar.avatar16.save('avatar_16', avatars[16])

        avatar.save()

        open('av_log', 'a').write("%s\n" % p.user_id)

    except Exception, e:
        print e
