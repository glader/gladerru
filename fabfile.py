# -*- coding: utf-8 -*-

from datetime import date

from fabric.api import *
from fabric.contrib.files import exists, append, upload_template, sed

from fab_settings import *

env.directory = '/home/%s/projects/gladerru' % SSH_USER
env.manage_dir = env.directory + '/src'
env.user = SSH_USER
env.activate = 'source %s/ENV/bin/activate' % env.directory
env.www_ssh_key = 'ssh-dss AAAAB3NzaC1kc3MAAACAbN+8KDO1jkRluNqiqO2KjkaSn4Qs66zBcV+JaUFrnoVt5tBaEMGW56ihtd1zmPqSufpDKTMXKneZWLAx8evFobvU5S32OKtFpR6oylZwIWg0SQNtjBE7lFHC5VnN4BtjpLp6DBzUOt6mTXYyCjaYhorMWmyw5641KXOsW0V7et0AAAAVALlYgGve+sIVrw7MTQFD4Hvb1utVAAAAgAGktSDpYw1sEC9tA593z3Ymk9r4J939DsKiL3d+RK/RXfY9KgoFtMHmCzL8goYpyWdaE2XQzCrIfp3EFW41NUWUfxsaDzXSEg4Q/CYAfJm7nNDpwv1eAq3c0Mw7RMGEw3pxsAnQrq0snHI7cVhdZ12Z6wO147+ybAbOXW7XF04sAAAAgGzFeuezmdfyS0N4VE42/kgC4SusMTxYOj5nrb8VRvzQ08Msa5FChXIWv0Fj5hMpOVX/gc4uEkbt7knpjqouo+K+8jadQ4I+sRidqG13U6b2UGJy844THSqL3HIhuPmhvWPOFjJbsNFxcoakSqLxn3ewkDzco7CH/aYo9u9VrLwk dsa-key-20080514'
env.forward_agent = True

if not env.hosts:
    env.hosts = ['82.196.9.202']


def virtualenv(command):
    with cd(env.directory):
        run(env.activate + ' && ' + command)


def init():
    with settings(user='root'):
        append('/etc/apt/sources.list', 'deb-src http://archive.ubuntu.com/ubuntu precise main', use_sudo=True)
        append('/etc/apt/sources.list', 'deb-src http://archive.ubuntu.com/ubuntu precise-updates main', use_sudo=True)

        sudo('apt-get update')
        sudo('apt-get upgrade -y')
        sudo('apt-get install -y mc nginx mysql-client python-setuptools python-dev rrdtool sendmail memcached fail2ban')
        sudo('apt-get build-dep -y python-mysqldb')
        run('apt-get install libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev')  # Pillow dependencies

        if not exists('/home/%s' % SSH_USER):
            sudo('yes | adduser --disabled-password %s' % SSH_USER)
            sudo('mkdir /home/%s/.ssh' % SSH_USER)
            sudo('echo "%s" >> /home/%s/.ssh/authorized_keys' % (env.www_ssh_key, SSH_USER))

        if not exists('/var/cache/gladerru/thumbnails'):
            sudo('mkdir -p /var/cache/gladerru/thumbnails')
            sudo('touch /var/cache/gladerru/glader_ru.links.db')
            sudo('chown -R www:www /var/cache/gladerru')

        if not exists('/var/log/projects/gladerru'):
            sudo('mkdir -p /var/log/projects/gladerru')
            sudo('chmod 777 /var/log/projects/gladerru')

        if exists('/etc/nginx/sites-enabled/default'):
            sudo('rm /etc/nginx/sites-enabled/default')

        if not exists('/etc/nginx/listen'):
            put('tools/nginx/listen', '/etc/nginx/listen', use_sudo=True)

        if not exists('/etc/nginx/sites-available/90-gladerru.conf'):
            sudo('touch /etc/nginx/sites-available/90-gladerru.conf')
            sudo('chown %s /etc/nginx/sites-available/90-gladerru.conf' % SSH_USER)
        if not exists('/etc/nginx/sites-enabled/90-gladerru.conf'):
            sudo('ln -s /etc/nginx/sites-available/90-gladerru.conf /etc/nginx/sites-enabled/90-gladerru.conf', shell=False)

        if not exists('/etc/init/gladerru.conf'):
            run('touch /etc/init/gladerru.conf')
            run('chown %s /etc/init/gladerru.conf' % SSH_USER)

        if not exists('/etc/init/gladerru_celery.conf'):
            run('touch /etc/init/gladerru_celery.conf')
            run('chown %s /etc/init/gladerru_celery.conf' % SSH_USER)

        append('/etc/sudoers', '%s ALL=(ALL) NOPASSWD:/sbin/restart gladerru,/sbin/restart gladerru_celery' % SSH_USER)

        if not exists('/etc/cron.d/gladerru'):
            sudo('touch /etc/cron.d/gladerru')

        sudo('mkdir -p /home/%s/projects/gladerru' % SSH_USER)
        sudo('chown -R %(user)s:%(user)s /home/%(user)s' % {'user': SSH_USER})


def init_mysql():
    with settings(host_string='82.196.15.15', user='root'):
        run('apt-get update')
        run('apt-get upgrade -y')
        run('apt-get install -y fail2ban mc')
        run('DEBIAN_FRONTEND=noninteractive apt-get -q -y install mysql-server')
        run('mysqladmin -u root password mysecretpasswordgoeshere111')

        sed('/etc/mysql/my.cnf', 'bind-address.+$', 'bind-address = ::')
        run('/etc/init.d/mysql restart')


def production(mode=""):
    upload()
    static()
    environment()
    local_settings()
    nginx()
    upstart()
    cron()
    if mode != 'no_dump':
        dump()
        migrate()
    collect_static()
    restart()


def update():
    production(mode='no_dump')


def upload():
    with settings(user=SSH_USER):
        local('git archive HEAD | gzip > archive.tar.gz')
        put('archive.tar.gz', env.directory + '/archive.tar.gz')
        with cd(env.directory):
            run('tar -zxf archive.tar.gz')
            run('rm archive.tar.gz')
        local('del archive.tar.gz')


def static():
    with settings(user=SSH_USER):
        with cd(env.directory + '/src/media/design/3/css'):
            run('python merge.py')


def environment():
    with settings(user=SSH_USER):
        with cd(env.directory):
            with settings(warn_only=True):
                run('python virtualenv.py ENV')
            virtualenv('pip install -r requirements.txt')


def local_settings():
    with settings(user=SSH_USER):
        with cd(env.manage_dir):
            upload_template(
                'src/local_settings.py.sample',
                'local_settings.py',
                globals(),
                backup=False
            )


def nginx():
    run('cp %(directory)s/tools/nginx/90-gladerru.conf /etc/nginx/sites-available/90-gladerru.conf' % env, shell=False)
    #sudo('/etc/init.d/nginx reload', shell=False)


def upstart():
    run('cp %(directory)s/tools/upstart/gladerru.conf /etc/init/gladerru.conf' % env, shell=False)


def cron():
    with settings(user='root'):
        sudo('cp %(directory)s/tools/cron/gladerru /etc/cron.d/gladerru' % env)
        sudo('/etc/init.d/cron restart')


def dump():
    with cd(env.directory):
        tmp_filename = run("date +/tmp/gladerru_backup_%Y%m%d_%H%M.sql.gz")
        month_dir = date.today().strftime("%Y_%m")
        backup_dir = "Backup/db/%s" % month_dir
        webdav_command =\
        "import easywebdav;"\
        "webdav = easywebdav.connect('webdav.yandex.ru', username='%s', password='%s', protocol='https');"\
        "webdav.mkdirs('%s');"\
        "webdav.upload('%s', '%s/%s');" % (DUMP_ACCOUNT_NAME, DUMP_PASSWORD, backup_dir, tmp_filename, backup_dir, tmp_filename.split('/')[-1])

        run("mysqldump -u %(DATABASE_USER)s -p%(DATABASE_PASSWORD)s -h %(DATABASE_HOST)s %(DATABASE_DB)s | gzip > " % globals() + tmp_filename)
        virtualenv('python -c "%s"' % webdav_command)
        run("rm %s" % tmp_filename)


def manage_py(command):
    virtualenv('cd %s && python manage.py %s' % (env.manage_dir, command))


def migrate():
    with settings(user=SSH_USER):
        manage_py('migrate')


def collect_static():
    with settings(user=SSH_USER):
        run('mkdir -p /home/www/projects/gladerru/static')
        manage_py('collectstatic -c --noinput')


def restart():
    run('sudo restart gladerru')


# -----------------------------------------------------------------------
# https://yandextank.readthedocs.org/en/latest/install.html

def tank_init():
    with settings(user='root', host='146.185.136.227'):
        run('apt-get install python-software-properties')
        run('add-apt-repository ppa:yandex-load/main')
        run('sudo apt-get update && sudo apt-get install yandex-load-tank-base')


def tank_start():
    with settings(user='root', host='146.185.136.227'):
        run('yandex-tank ammo.txt')


# -----------------------------------------------------------------------

def run_local():
    local('cd src && ..\\ENV\\Scripts\\python manage.py runserver 0.0.0.0:8000')


def local_env():
    with settings(warn_only=True):
        local('c:\\python\\python virtualenv.py ENV --system-site-packages')
    local('ENV\\Scripts\\pip install -r requirements.txt ')


def local_migrate():
    with settings(warn_only=True):
        local('cd src && ..\\ENV\\Scripts\\python manage.py schemamigration core --auto')
    local('cd src && ..\\ENV\\Scripts\\python manage.py migrate')


def update_local_db():
    run("mysqldump -u %(DATABASE_USER)s -p%(DATABASE_PASSWORD)s -h %(DATABASE_HOST)s %(DATABASE_DB)s > gladerru.sql" % globals())
    get("gladerru.sql", "gladerru.sql")
    run("rm gladerru.sql")
    local("mysql -uroot %(DATABASE_DB)s < gladerru.sql" % globals())
    local("del gladerru.sql")


def local_celery():
    local('cd src && ..\\ENV\\scripts\\python manage.py celeryd --settings=settings')


def local_static():
    local('cd src && ..\\ENV\\scripts\\python manage.py collectstatic -c --noinput --verbosity=0')


def make_backup():
    today = date.today().replace(day=1)
    run("mysqldump -u %(DATABASE_USER)s -p%(DATABASE_PASSWORD)s -h %(DATABASE_HOST)s %(DATABASE_DB)s | gzip > gladerru.sql.gz" % globals())
    get("gladerru.sql.gz", "gladerru.sql.%s.gz" % today.strftime('%Y%m%d'))
