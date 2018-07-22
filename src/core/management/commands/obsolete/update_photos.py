# coding: utf-8
from django.conf import settings
from django.core.management.base import NoArgsCommand

from core.models import Photo
from urllib2 import Request, urlopen
import httplib
import re


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        ids = ()
        for photo in Photo.objects.filter(yandex_fotki_image_id__isnull=False, id__in=ids).order_by('pk'):
            print "PHOTO", photo.id

            fotki_id = photo.yandex_fotki_image_id.split(':')[-1]
            url = "/api/users/gladerru/photo/%s/" % fotki_id

            print url

            try:
                headers = {'Authorization': 'OAuth %s' % settings.YAPHOTO_TOKEN}
                request = Request("http://" + settings.YAPHOTO_HOST + url, headers=headers)

                result = urlopen(request)

                entry = result.read()
                # print entry

                if photo.rider:
                    title = photo.rider.title
                    if photo.photographer:
                        title += u" (%s)" % photo.photographer.title
                elif photo.post:
                    title = photo.post.title
                else:
                    title = u"Картинка с сайта glader.ru"

                try:
                    print title.encode('cp866')
                except:
                    print "title"
                entry = re.sub('<title>.+</title>', '<title>%s</title>' % title.encode('utf8'), entry)
                photo_descr = "Адрес фотографии: http://glader.ru%s" % str(photo.get_absolute_url())
                if '<summary>' in entry:
                    entry = re.sub('<summary>.+</summary>', '<summary>%s</summary>' % photo_descr, entry)
                else:
                    entry = entry.replace('</title>', '</title><summary>%s</summary>' % photo_descr)

                h = httplib.HTTPConnection(settings.YAPHOTO_HOST, 80)
                all_headers = {
                    'Content-Type': 'application/atom+xml; type=entry',
                    'Authorization': 'OAuth %s' % settings.YAPHOTO_TOKEN
                }
                h.request('PUT', url, entry, all_headers)
                res = h.getresponse()
                print res.status, res.reason
                print
            except Exception, e:
                print e
                log = open('errors', 'a')
                log.write("%s, " % photo.id)
                log.close()
