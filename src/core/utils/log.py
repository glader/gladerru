# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

from django.conf import settings


def get_logger(name):
    filename = os.path.join(settings.LOG_PATH, name.replace('.', '/') + '.log')

    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
                  filename, maxBytes=10000000, backupCount=6)
    LOG_FORMAT = u'%(levelname)s %(asctime)s: %(message)s'
    LOG_TIME_FORMAT = u'%Y-%m-%d %H:%M:%S'
    handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_TIME_FORMAT))
    log.addHandler(handler)

    return log
