# coding: utf-8
import json

from django.db import models


class JSONField(models.TextField):
    """ Поле для хранения данных, сериализованных в json. """

    editable = False
    serialize = False

    class JSONDict(dict):
        def __str__(self):
            return json.dumps(self, sort_keys=True)

    class JSONList(list):
        def __str__(self):
            return json.dumps(self, sort_keys=True)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return json.loads(value)

    def get_prep_value(self, value):
        if value is not None:
            return json.dumps(value, sort_keys=True)

    def to_python(self, value):
        if value is None:
            return value
        elif not isinstance(value, str):
            return value
        if value:
            try:
                value = json.loads(value)
                if isinstance(value, list):
                    value = self.JSONList(value)
                elif isinstance(value, dict):
                    value = self.JSONDict(value)
                return value
            except ValueError:
                # If value can't be decoded, output it as string
                return value
        return None
