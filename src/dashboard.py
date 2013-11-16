# -*- coding: utf-8 -*-
from datetime import date, timedelta

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.db import connection

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard


class UGCStat(modules.DashboardModule):
    def __init__(self, **kwargs):
        super(UGCStat, self).__init__(**kwargs)
        self.title = kwargs.get('title', 'Статистика')
        self.template = kwargs.get('template', '3/admin/dashboard/stat.html')
        self.interval = timedelta(days=kwargs.get('days', 7))
        self.blocks = []
        cursor = connection.cursor()
        cursor.execute("""SELECT d.date, COUNT(p.id)
                            from d
                            left join core_profile p ON d.date=cast(p.date_created as date)
                            WHERE d.date <= '%s' and d.date >= '%s'
                            group by d.date""" % (date.today(), date.today() - self.interval))
        registrations = cursor.fetchall()
        if registrations:
            self.blocks.append({'title': u'Регистрации',
                            'max': max(row[1] for row in registrations),
                            'data': ','.join(str(row[1]) for row in registrations),
                            'days': '|%s|' % '|'.join(str(row[0].day) for row in registrations)
                            })

        cursor.execute("""SELECT d.date, COUNT(p.id)
                            from d
                            left join core_comment p ON d.date=cast(p.date_created as date)
                            WHERE d.date <= '%s' and d.date >= '%s'
                            group by d.date""" % (date.today(), date.today() - self.interval))
        comments = cursor.fetchall()
        if comments:
            self.blocks.append({'title': u'Комментарии',
                            'max': max(row[1] for row in comments),
                            'data': ','.join(str(row[1]) for row in comments),
                            'days': '|%s|' % '|'.join(str(row[0].day) for row in registrations)
                            })

    def is_empty(self):
        return False


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for glader.
    """
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        # append an app list module for "Applications"
        self.children.append(modules.Group(
            title=u"Приложения",
            display="tabs",
            children=[
                      modules.ModelList(
                            title='Best',
                            include_list=('core.models.mountain',
                                          'core.models.man',
                                          'core.models.profile',
                                          'core.models.tag',
                                          'core.models.movie',
                                          ),
                            exclude_list=('core.models.tag2skill',)
                        ),
                      modules.ModelList(
                            title='Other',
                            exclude_list=('core.models.mountain',
                                          'core.models.movie',
                                          'core.models.man',
                                          'core.models.tag',
                                          'core.models.profile',
                                          'django'
                                          )
                        ),
            ]
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            title=_('Administration'),
            include_list=('django.contrib',),
        ))

        self.children.append(modules.Group(
            title=u"Ссылки",
            display="tabs",
            children=[
                modules.LinkList(
                    title="Заработок",
                    children=[
                        {
                            'title': u'Посещаемость',
                            'url': 'http://metrika.yandex.ru/stat/?counter_id=41561',
                            'external': True,
                        },
                        {
                            'title': u'Sape',
                            'url': 'http://sape.ru',
                            'external': True,
                        },
                        {
                            'title': u'ЯДирект',
                            'url': 'http://mixmarket.biz/direct/reportgraph/all/',
                            'external': True,
                        },
                        {
                            'title': u'Amazon store',
                            'url': 'https://aws-portal.amazon.com/gp/aws/developer/account/index.html',
                            'external': True,
                        },
                        {
                            'title': u"Баланс",
                            'url': 'http://spreadsheets.google.com/ccc?key=0Ap-oSRhw9x3adF83UjItVDVxWmVNajlnRmtUbVZ6UkE&hl=ru',
                            'external': True,
                        },
                    ]
                ),
                modules.LinkList(
                    title=u"Социальщина",
                    children=[
                        {
                            'title': u'Вконтакте',
                            'url': 'http://vkontakte.ru/club10510322',
                            'external': True,
                        },
                        {
                            'title': _('Twitter'),
                            'url': 'http://twitter.com/glader_ru',
                            'external': True,
                        },
                        {
                            'title': _('LiveJournal'),
                            'url': 'http://syndicated.livejournal.com/gladerru_news/',
                            'external': True,
                        },
                    ]
                ),
            ]
        ))

        self.children.append(modules.Group(
            title=u"Статистика",
            display="tabs",
            children=[
                UGCStat(
                    title=u"Месяц",
                    days=30
                ),
            ]
        ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass

# to activate your app index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'glader.dashboard.CustomAppIndexDashboard'


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for glader.
    """
    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # we disable title because its redundant with the model list module
        self.title = ''

        # append a model list module
        self.children.append(modules.ModelList(
            title=self.app_title,
            include_list=self.models,
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            include_list=self.get_app_content_types(),
        ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass
