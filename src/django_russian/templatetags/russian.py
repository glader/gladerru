# encoding: utf-8
from django import template
from datetime import datetime

register = template.Library()


@register.filter
def human_month(monthNumber):
    months = (u'январь', u'февраль', u'март', u'апрель', u'май', u'июнь', u'июль', u'август',
              u'сентябрь', u'октябрь', u'ноябрь', u'декабрь')
    return months[monthNumber - 1]


@register.filter
def human_weekday(date):
    days = (u'пн', u'вт', u'ср', u'чт', u'пт', u'сб', u'вс')
    return days[date.weekday()]


@register.filter
def human_date(date, mode=""):
    if not date:
        return ""
    months = (u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня', u'июля', u'августа',
              u'сентября', u'октября', u'ноября', u'декабря')
    date_str = u"%d %s" % (date.day, months[date.month - 1])
    if date.year != datetime.now().year or 'year' in mode:
        date_str += u" %d" % date.year
    return date_str


@register.filter
def human_time(time):
    if not time:
        return ""
    return u"%02d:%02d" % (time.hour, time.minute)


@register.filter
def human_gender(gender):
    if gender == 'm':
        return u"Мальчик"
    if gender == 'f':
        return u"Девочка"
    return u"Не определилось"


@register.filter
def human_number(quantity, word):
    """ Преобразует слово в зависимости от числа
        1 комментарий
        2 комментария
        5 комментариев
    """
    if not quantity:
        quantity = 0

    terminations = {u'ий': [u'ий', u'ия', u'иев'],
                    u'ие': [u'ие', u'ия', u'ий'],
                    u'ый': [u'ый', u'ых', u'ых'],
                    u'т': [u'т', u'та', u'тов'],
                    u'с': [u'с', u'са', u'сов'],
                    }

    def get_term_number(quantity):
        """ Возвращает номер окончания в зависимости от числа
            0: 1 (комментарий)
            1-4: 2 (комментария)
            5...: 3 (комментариев)
        """
        q = quantity % 100
        if q in xrange(11, 15):
            return 3
        q = q % 10
        if q == 1:
            return 1
        if 2 <= q <= 4:
            return 2
        return 3

    term_number = get_term_number(quantity)
    for t in terminations.keys():
        if word[-len(t):] == t:
            return word[:-len(t)] + terminations[t][term_number - 1]
    return word
