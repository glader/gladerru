# coding: utf-8
from datetime import date

from fabric.api import *
from fabric.contrib.files import exists, append, upload_template, sed

from fab_settings import *

env.directory = '/home/%s/projects/gladerru' % SSH_USER
env.manage_dir = env.directory + '/src'
env.user = SSH_USER
env.activate = 'source %s/ENV/bin/activate' % env.directory
env.www_ssh_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAIEAlgcYVZYvzu1GX4Td+RLt9BIqUr33gkTz6MW2MHvWS/+9eKueA6+N7Bei2NqTBNg2HLUY0uOyG1NBmzoWZglht70iChcGLMVkvciQ1/QQfr5bvIbfgpPHuZMwn4ElFiiabhnZe9wALp+jjg0TnolWxbAfwJUmv2UDXXSiYDrfBes= glader hosting rsa-key-20150528'
env.forward_agent = True

if not env.hosts:
    env.hosts = ['188.246.227.206']


def virtualenv(command):
    with cd(env.directory):
        run(env.activate + ' && ' + command)


def init():
    with settings(user='root'):
        run('apt-get update -q', warn_only=True)
        #run('apt-get upgrade -y')
        #run('apt-get install -y mc nginx mysql-client libmysqlclient-dev python-setuptools python-dev python-pip rrdtool sendmail memcached fail2ban git')
        #run('apt-get build-dep -y python-mysqldb')
        #run('pip install --upgrade virtualenv')

        if not exists('/home/%s' % SSH_USER):
            run('yes | adduser --disabled-password %s' % SSH_USER)
            run('mkdir /home/%s/.ssh' % SSH_USER)
            run('echo "%s" >> /home/%s/.ssh/authorized_keys' % (env.www_ssh_key, SSH_USER))

        if not exists('/var/cache/gladerru/thumbnails'):
            run('mkdir -p /var/cache/gladerru/thumbnails')
            run('touch /var/cache/gladerru/glader_ru.links.db')
            run('chown -R www:www /var/cache/gladerru')

        if not exists('/var/log/projects/gladerru'):
            run('mkdir -p /var/log/projects/gladerru')
            run('chmod 777 /var/log/projects/gladerru')

        if exists('/etc/nginx/sites-enabled/default'):
            run('rm /etc/nginx/sites-enabled/default')

        if not exists('/etc/nginx/sites-available/90-gladerru.conf'):
            run('touch /etc/nginx/sites-available/90-gladerru.conf')
            run('chown %s /etc/nginx/sites-available/90-gladerru.conf' % SSH_USER)
        if not exists('/etc/nginx/sites-enabled/90-gladerru.conf'):
            run('ln -s /etc/nginx/sites-available/90-gladerru.conf /etc/nginx/sites-enabled/90-gladerru.conf', shell=False)

        if not exists('/etc/init/gladerru.conf'):
            run('touch /etc/init/gladerru.conf')
            run('chown %s /etc/init/gladerru.conf' % SSH_USER)

        if not exists('/etc/init/gladerru_celery.conf'):
            run('touch /etc/init/gladerru_celery.conf')
            run('chown %s /etc/init/gladerru_celery.conf' % SSH_USER)

        append('/etc/sudoers', '%s ALL=(ALL) NOPASSWD:/sbin/restart gladerru,/sbin/restart gladerru_celery' % SSH_USER)

        if not exists('/etc/cron.d/gladerru'):
            run('touch /etc/cron.d/gladerru')

        run('mkdir -p /home/%s/projects/gladerru' % SSH_USER)
        run('chown -R %(user)s:%(user)s /home/%(user)s' % {'user': SSH_USER})


def init_mysql():
    with settings(user='root'):
        run('apt-get update -q', warn_only=True)
        #run('apt-get upgrade -y')
        #run('apt-get install -y fail2ban mc')
        run('DEBIAN_FRONTEND=noninteractive apt-get -q -y install mysql-server')
        run('mysqladmin -u root password mysecretpasswordgoeshere111')

        #sed('/etc/mysql/my.cnf', 'bind-address.+$', 'bind-address = ::')
        run('/etc/init.d/mysql restart')


def production(mode=''):
    upload()
    static()
    environment()
    local_settings()
    nginx()
    systemd()
    cron()
    logrotate()
    if mode != 'no_dump':
        # dump()
        migrate()
    collect_static()
    put_release_file()
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
    with cd(env.directory):
        with settings(warn_only=True):
            run('virtualenv ENV')
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

            upload_template(
                'tools/dump/dump.sh',
                '../tools/dump/dump.sh',
                globals(),
                backup=False
            )


def nginx():
    run('cp %(directory)s/tools/nginx/90-gladerru.conf /etc/nginx/sites-available/90-gladerru.conf' % env, shell=False)


def systemd():
    with settings(user='root'):
        run('cp %(directory)s/tools/systemd/gladerru.service /lib/systemd/system/gladerru.service' % env, shell=False)


def cron():
    with settings(user='root'):
        run('cp %(directory)s/tools/cron/gladerru /etc/cron.d/gladerru' % env)
        run('systemctl restart cron')


def logrotate():
    with settings(user='root'):
        run('cp %(directory)s/tools/logrotate/gladerru /etc/logrotate.d/gladerru' % env)


def dump():
    run('/home/www/projects/gladerru/tools/dump/dump.sh')


def manage_py(command):
    virtualenv('cd %s && python manage.py %s' % (env.manage_dir, command))


def migrate():
    with settings(user=SSH_USER):
        manage_py('migrate')


def collect_static():
    with settings(user=SSH_USER):
        run('mkdir -p /home/www/projects/gladerru/static')
        manage_py('collectstatic -c --noinput')


def put_release_file():
    local('git log -n 1 --format=oneline > release')

    put('release', env.directory + '/release')
    local('rm release')


def restart():
    with settings(user='root'):
        run('systemctl restart gladerru')


def remote(args=''):
    manage_py(args)


# -----------------------------------------------------------------------
# https://yandextank.readthedocs.org/en/latest/install.html

def tank_init():
    with settings(user='root', host='146.185.136.227'):
        run('apt-get install python-software-properties')
        run('add-apt-repository ppa:yandex-load/main')
        run('run apt-get update && sudo apt-get install yandex-load-tank-base')


def tank_start():
    with settings(user='root', host='146.185.136.227'):
        run('yandex-tank ammo.txt')


# -----------------------------------------------------------------------

def run_local():
    local('cd src && ..\\ENV\\Scripts\\python manage.py runserver 0.0.0.0:8000')


def local_env():
    with settings(warn_only=True):
        local('virtualenv.exe ENV --system-site-packages')
    local('ENV\\Scripts\\pip install -r requirements_test.txt ')


def enter(args=''):
    local('cd src && ..\\ENV\\Scripts\\python manage.py %s' % args)


def local_migrate():
    with settings(warn_only=True):
        local('cd src && ..\\ENV\\Scripts\\python manage.py makemigrations')
    local('cd src && ..\\ENV\\Scripts\\python manage.py migrate')


def update_local_db():
    run('mysqldump -u %(DATABASE_USER)s -p%(DATABASE_PASSWORD)s -h %(DATABASE_HOST)s %(DATABASE_DB)s |gzip > gladerru.sql.gz' % globals())
    get('gladerru.sql.gz', 'gladerru.sql.gz')
    run('rm gladerru.sql.gz')
    local('gzip -d gladerru.sql.gz')
    local('mysql -uroot %(DATABASE_DB)s < gladerru.sql' % globals())
    local('del gladerru.sql')


def local_celery():
    local('cd src && ..\\ENV\\scripts\\python manage.py celeryd --settings=settings')


def local_static():
    local('cd src && ..\\ENV\\scripts\\python manage.py collectstatic -c --noinput --verbosity=0')


def make_backup():
    today = date.today().replace(day=1)
    run('mysqldump -u %(DATABASE_USER)s -p%(DATABASE_PASSWORD)s -h %(DATABASE_HOST)s %(DATABASE_DB)s | gzip > gladerru.sql.gz' % globals())
    get('gladerru.sql.gz', 'gladerru.sql.%s.gz' % today.strftime('%Y%m%d'))
    run('rm gladerru.sql.gz')
