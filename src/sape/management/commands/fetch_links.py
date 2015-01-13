# -*- coding: utf-8 -*-
import xmlrpclib
from itertools import imap

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.core.mail import mail_admins

from sape.models import Link
from sape.cookietransport import CookieTransport
import logging

log = logging.getLogger('django.cron')


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        log.info('Start fetching links from sape')

        stat = {'new': 0, 'del': 0, 'unchanged': 0}

        server = xmlrpclib.Server('http://api.sape.ru/xmlrpc/', transport=CookieTransport())
        server.sape.login(settings.SAPE_LOGIN, settings.SAPE_PASSWORD)
        links = server.sape.get_site_links(38739)

        if any(imap(lambda link: link['status'] == 'ERROR', links)):
            mail_admins(u'glader.ru: битые ссылки', u'На сайте glader.ru обнаружены линки в статусе ERROR.')

        log.info('%s links fetched', len(links))

        pages = server.sape.get_site_pages(38739)
        pages_dict = {page['id']: page['uri'] for page in pages}

        site_links = {link.link_id: link for link in Link.objects.all()}

        for link in links:
            if link['status'] not in ('OK', 'ERROR'):
                continue

            if link['id'] in site_links:
                del site_links[link['id']]
                stat['unchanged'] += 1

            else:
                log.info('New link %r', link)
                Link.objects.create(
                    link_id=link['id'],
                    status=link['status'],
                    txt=link['txt'],
                    url=link['url'],
                    page=pages_dict[link['page_id']]
                )
                stat['new'] += 1

        for link in site_links.values():
            log.info('Link %s removed', link.link_id)
            stat['del'] += 1
            link.delete()

        log.info('Finish fetching links from sape, %s new, %s deleted, %s unchanged',
                 stat['new'], stat['del'], stat['unchanged'])
