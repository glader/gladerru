# -*- coding: utf-8 -*-

import re
from datetime import datetime
import MySQLdb
from MySQLdb.cursors import DictCursor, SSDictCursor

conn = MySQLdb.connect(host='localhost', user='root', \
                       passwd='', db='gladerru')

conn2 = MySQLdb.connect(host='localhost', user='root', \
                       passwd='', db='u70497_glader')

cursor = conn.cursor(DictCursor)
cursor.execute("SET NAMES 'cp1251'")
#cursor.execute("SET CHARACTER SET 'utf8'")
#cursor.execute("SET character_set_client=utf8;")
#cursor.execute("SET character_set_connection=utf8;")

source = conn2.cursor()
source.execute("SET NAMES 'cp1251'")
#cursor2.execute("SET CHARACTER SET 'utf8'")
#cursor2.execute("SET character_set_client=utf8;")
#cursor2.execute("SET character_set_connection=utf8;")

"""
import sys,settings
from django.core.management import setup_environ
setup_environ(settings)
from YourApp.models import MyModel

try:
    print MyModel.objects.get(id=sys.argv[1])
except Exception:
    print "error"
"""


print "itemtypes ..",
cursor.execute("TRUNCATE TABLE core_itemtype")
source.execute("SELECT * FROM cms_spr_types")
types = {}
i = 1
for t in source.fetchall():
    types[t[1]] = i
    i += 1
    cursor.execute("INSERT INTO core_itemtype (name, description, template) VALUES (%s, %s, %s)", (t[1], t[2], t[0]))
print "done"

cursor.execute("INSERT INTO core_itemtype (name, description, template) VALUES ('USER', 'Профиль', '')")
types['USER'] = i

print "users ..",
cursor.execute("TRUNCATE TABLE auth_user")
cursor.execute("TRUNCATE TABLE core_item")
source.execute("SELECT * FROM cms_users")
users = {}
items = {}

i = 1
for u in source.fetchall():
    users['user_' + str(u[2])] = i
    email = u[9] or "no@no.com"
    last_login = u[5] or datetime.now()
    date_joined = u[6] or datetime.now()
    cursor.execute("""INSERT INTO auth_user (username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined)
        VALUES (%s, %s, '', %s, CONCAT('md5$$', %s), 0, 1, 0, %s, %s)""", (u[2], u[1], email, u[3], last_login, date_joined))

    if u[10]:
        icq = re.sub('\-', '', str(u[10]))
    else:
        icq = None
    if u[35] < 0:
        picCount = 0
    else:
        picCount = u[35]

    name = 'user_' + u[2]
    items[name] = i

    cursor.execute("""INSERT INTO core_item (user_id, name, title, type_id, item_type, date_created, date_changed, filename, icq, url, interests, board, bindings,
                    boots, riding_style, mountains, clothes, equip, country, city, content, gender,
                    draftPostCount, pubPostCount, commentCount, picCount, clipCount)
        VALUES (%s, %s, %s, %s, 'USER', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                       (i, name, u[1], types['USER'], date_joined, date_joined, u[8], icq, u[11], u[14], u[15], u[16],
                        u[17], u[18], u[19], u[20], u[21], u[22], u[23], u[24], u[28],
                        u[32], u[33], u[34], picCount, u[36]))

    i += 1

cursor.execute("UPDATE auth_user SET is_staff=1, is_superuser=1 WHERE username='glader'")
cursor.execute("COMMIT")
print "done"

print "items ..",
source.execute("SELECT * FROM cms_items")
for item in source.fetchall():
    items[item[0]] = i
    cursor.execute("INSERT INTO core_item (name, type_id, item_type, template, date_created, date_changed)  VALUES (%s, %s, %s, %s, %s, %s)",
                   (item[0], types[item[1]], item[1], item[2], item[3], item[4]))
    i += 1

print "done"


print "attrs ..",
source.execute("select id_item, `name`, `value` FROM cms_attrs JOIN cms_spr_attrs ON id_attr_type =cms_spr_attrs.id")
i = 0
for attr in source.fetchall():
    value = attr[2]
    if attr[1] == 'date' and value[4] != '-':
        value = "%s-%s-%s" % (value[6:], value[3:5], value[:2])

    try:
        cursor.execute("UPDATE core_item SET `%s`=%s WHERE name=%s" % (attr[1], "%s", "%s"), (value, attr[0]))
    except (MySQLdb.OperationalError, MySQLdb.DataError), e:
        print "=" * 60
        #print attr, value
        print e

    i += 1
    if i % 1000 == 0:
        print i,
print "done"

print "relationtypes ..",
cursor.execute("TRUNCATE TABLE core_relationtype")
source.execute("SELECT * FROM cms_spr_relations")
rels = {}
i = 1
for t in source.fetchall():
    rels[t[0]] = i
    i += 1
    cursor.execute("INSERT INTO core_relationtype (name, description) VALUES (%s, %s)", (t[0], t[1]))
print "done"


print "relations ..",
cursor.execute("TRUNCATE TABLE core_relation")
source.execute("UPDATE cms_relations SET DBegin='2004-10-09' WHERE DBegin IS NULL OR DBegin='0000-00-00'")
source.execute("DELETE FROM cms_relations WHERE id_relation='default'")
source.execute("SELECT * FROM cms_relations")
i = 0
for item in source.fetchall():
    try:
        a = items[item[1]]
    except KeyError:
        print item

    try:
        b = items[item[2]]
    except KeyError:
        print item

    try:
        cursor.execute("INSERT INTO core_relation (item_a_id, item_b_id, rel_type_id, date_created)  VALUES (%s, %s, %s, %s)",
                       (a, b, rels[item[3]], item[4]))
    except (MySQLdb.OperationalError, MySQLdb.DataError), e:
        print "=" * 60
        print item[4]
        #print attr, value
        print e

    i += 1
    if i % 1000 == 0:
        print i,

print "done"

# Оценки
print "votes ..",
cursor.execute("TRUNCATE TABLE core_itemvote")
source.execute("SELECT * FROM cms_items_votes order by recid")
for v in source.fetchall():
    if not (items.has_key(v[2]) and items.has_key(v[3])):
        continue
    cursor.execute("INSERT INTO core_itemvote (item_id, profile_id, vote, date_created)  VALUES (%s, %s, %s, %s)",
                       (items[v[2]], items[v[3]], v[4], v[1]))

print "done"


print "updates .."
cursor.execute("INSERT INTO core_item SET name='articles_menu', type_id=28, title='Articles menu', date_created=NOW(), date_changed=NOW()")
cursor.execute("SELECT id FROM core_item WHERE name='articles_menu'")
menu = cursor.fetchone()['id']

cursor.execute("SELECT id FROM core_item WHERE name IN ('freeride_articles', 'freestyle_articles', 'jibbing_articles', 'school', 'mat', 'creatives', 'snowstyles', 'howtobuy', 'usefull', 'humour')")
for rec in cursor.fetchall():
    cursor.execute("INSERT INTO core_relation VALUES (Null, %s, %s, 1, NOW())", (menu, rec['id']))

cursor.execute("update core_item set menu_type='articles_menu' WHERE name in ('freeride_articles', 'freestyle_articles', 'jibbing_articles', 'articles', 'school', 'mat', 'creatives', 'snowstyles', 'howtobuy', 'usefull', 'humour')")


cursor.execute("INSERT INTO core_item SET name='world_menu', type_id=28, title='World menu', date_created=NOW(), date_changed=NOW()")
cursor.execute("SELECT id FROM core_item WHERE name='world_menu'")
menu = cursor.fetchone()['id']

cursor.execute("""SELECT id FROM core_item WHERE name IN ('riders', 'photographers', 'men_other', 'companies', 'teams', 'moviemakers', 'countries',
                  'mountains', 'contests', 'reports', 'magazines', 'links', 'shops')""")
for rec in cursor.fetchall():
    cursor.execute("INSERT INTO core_relation VALUES (Null, %s, %s, 1, NOW())", (menu, rec['id']))

cursor.execute("update core_item set menu_type='world_menu' WHERE name in ('snowboard', 'riders', 'photographers', 'men_other', 'companies', 'teams', 'moviemakers', 'countries', 'mountains', 'contests', 'reports', 'magazines', 'links')")


cursor.execute("INSERT INTO core_item SET name='movie_menu', type_id=28, title='Movie menu', date_created=NOW(), date_changed=NOW()")
cursor.execute("SELECT id FROM core_item WHERE name='movie_menu'")
menu = cursor.fetchone()['id']

cursor.execute("""SELECT id FROM core_item WHERE name IN ('snow_films', 'ski_films', 'kite', 'wake')""")
for rec in cursor.fetchall():
    cursor.execute("INSERT INTO core_relation VALUES (Null, %s, %s, 1, NOW())", (menu, rec['id']))

cursor.execute("update core_item set menu_type='movie_menu' WHERE name in ('films_list', 'snow_films', 'ski_films', 'kite', 'wake')")


cursor.execute("update core_item set template=NULL where `name`='articles'")
cursor.execute("update core_item set template=NULL where `name`='snowboard'")
cursor.execute("UPDATE core_item SET template='riders.html' WHERE name='riders'")
cursor.execute("update core_item set template='moviemakers.html' where `name`='moviemakers'")
cursor.execute("update core_item set template='companies.html' where `name`='companies'")
cursor.execute("update core_item set template='photographers.html' where `name`='photographers'")
cursor.execute("update core_item set template='men_other.html' where `name`='men_other'")
cursor.execute("update core_item set template='links.html' where `name`='links'")
cursor.execute("update core_item set template='teams.html' where `name`='teams'")
cursor.execute("update core_item set template='countries.html' where `name`='countries'")
cursor.execute("update core_item set template='mountains.html' where `name`='mountains'")
cursor.execute("update core_item set template='magazines.html' where `name`='magazines'")
cursor.execute("update core_item set template='contests.html' where `name`='contests'")
cursor.execute("update core_item set template='reports.html' where `name`='reports'")
cursor.execute("update core_item set template='rubric_icon.html' where template='rubric_icon_t'")
cursor.execute("update core_item set template='deep_rubric.html' where template='deep_rubric_t'")
cursor.execute("UPDATE core_item SET template='news.html' WHERE name='news'")
cursor.execute("UPDATE core_item SET template='films.html' WHERE name='films_list'")

print "done"
#
