from __future__ import print_function, unicode_literals, with_statement
from future.builtins import input, open

import os
import re
import sys
from functools import wraps
from getpass import getpass, getuser
from glob import glob
from contextlib import contextmanager
from posixpath import join

from os.path import basename, dirname

from fabric.api import env, cd, prefix, sudo as _sudo, run as _run, hide, task
#from fabric.api import settings
from fabric.api import puts
from fabric.contrib.files import exists, upload_template
from fabric.colors import yellow, green, blue, red
from fabric.utils import warn

import pdb
###############
# Fab Command #
###############

#fab command
#fab install

################
# Config setup #
################

conf = {}
if sys.argv[0].split(os.sep)[-1] in ("fab", "fab-script.py"):
    # Ensure we import settings from the current dir
    try:
        #conf = __import__("settings", globals(), locals(), [], 0).FABRIC
        #conf = __import__("project.settings", globals(), locals(), [], 0).FABRIC
        from project import settings
        conf = settings.FABRIC
        try:
            conf["HOSTS"][0]
        except (KeyError, ValueError):
            raise ImportError
    except (ImportError, AttributeError):
        print("Aborting, no hosts defined.")
        exit()

env.db_pass = conf.get("DB_PASS", None)
env.db_root_pass = env.db_pass
#env.admin_pass = conf.get("ADMIN_PASS", None)
env.user = conf.get("SSH_USER", getuser())
env.password = conf.get("SSH_PASS", None)
env.key_filename = conf.get("SSH_KEY_PATH", None)
env.hosts = conf.get("HOSTS", [""])

env.proj_name = conf.get("PROJECT_NAME", os.getcwd().split(os.sep)[-1])
env.venv_home = conf.get("VIRTUALENV_HOME", "/home/%s" % env.user)
env.venv_path = "%s/%s" % (env.venv_home, env.proj_name)
env.proj_dirname = "project"
env.proj_path = "%s/%s" % (env.venv_path, env.proj_dirname)
env.manage = "%s/bin/python %s/project/manage.py" % ((env.venv_path,) * 2)
env.domains = conf.get("DOMAINS", [conf.get("LIVE_HOSTNAME", env.hosts[0])])
env.domains_nginx = " ".join(env.domains)
env.domains_python = ", ".join(["'%s'" % s for s in env.domains])
env.ssl_disabled = "#" if len(env.domains) > 1 else ""
env.repo_url = conf.get("REPO_URL", "")
env.git = env.repo_url.startswith("git") or env.repo_url.endswith(".git")
env.reqs_path = conf.get("REQUIREMENTS_PATH", None)
env.locale = conf.get("LOCALE", "en_US.UTF-8")

env.secret_key = conf.get("SECRET_KEY", "")
env.nevercache_key = conf.get("NEVERCACHE_KEY", "")

env.django_user = conf.get("DJANGO_USER", "duser")
env.django_user_group = env.django_user

env.django_project_settings = "settings"

env.gunicorn_workers = 2
env.gunicorn_logfile = '%(venv_path)s/logs/projects/%(proj_name)s_gunicorn.log' % env
#env.rungunicorn_script = '%(venv_path)s/scripts/rungunicorn_%(proj_name)s.sh' % env
env.rungunicorn_script = '%(venv_path)s/bin/gunicorn_start' % env
env.gunicorn_worker_class = "eventlet"
env.gunicorn_loglevel = "info"
env.gunicorn_port = conf.get("GUNICORN_PORT", 8000)


env.supervisor_program_name = env.proj_name
env.supervisorctl = '/usr/bin/supervisorctl'
env.supervisor_autostart = 'true'
env.supervisor_autorestart = 'true'
env.supervisor_redirect_stderr = 'true'
env.supervisor_stdout_logfile = '%(venv_path)s/logs/projects/supervisord_%(proj_name)s.log' % env
#env.supervisord_conf_file = '%(venv_path)s/configs/supervisord/%(proj_name)s.conf' % env
env.supervisord_conf_file = '/etc/supervisor/conf.d/%(proj_name)s.conf' % env

##################
# Template setup #
##################

# Each template gets uploaded at deploy time, only if their
# contents has changed, in which case, the reload command is
# also run.

templates = {
    "nginx": {
        "local_path": "deploy/nginx.conf",
        "remote_path": "/etc/nginx/sites-enabled/%(proj_name)s.conf",
    },
    "supervisor": {
        "local_path": "deploy/supervisord.conf",
        "remote_path": env.supervisord_conf_file,
    },
    "cron": {
        "local_path": "deploy/crontab",
        "remote_path": "/etc/cron.d/%(proj_name)s",
        "owner": "root",
        "mode": "600",
    },
    "gunicorn": {
        "local_path": "deploy/gunicorn_start",
        "remote_path": "%(venv_path)s/bin/gunicorn_start",
    },
    "settings": {
        "local_path": "deploy/local_settings",
        "remote_path": "%(proj_path)s/project/local_settings.py",
    },
    "mysql": {
        "local_path": "deploy/mysql.cnf",
        "remote_path": "/etc/mysql/my.cnf",
    }
}

######################################
# Context for virtualenv and project #
######################################

@contextmanager
def virtualenv():
    """
    Runs commands within the project's virtualenv.
    """
    with cd(env.venv_path):
        with prefix("source %s/bin/activate" % env.venv_path):
            yield


@contextmanager
def project():
    """
    Runs commands within the project's directory.
    """
    with virtualenv():
        with cd(env.proj_dirname):
            yield


@contextmanager
def update_changed_requirements():
    """
    Checks for changes in the requirements file across an update,
    and gets new requirements if changes have occurred.
    """
    reqs_path = join(env.proj_path, env.reqs_path)
    get_reqs = lambda: run("cat %s" % reqs_path, show=False)
    old_reqs = get_reqs() if env.reqs_path else ""
    yield
    if old_reqs:
        new_reqs = get_reqs()
        if old_reqs == new_reqs:
            # Unpinned requirements should always be checked.
            for req in new_reqs.split("\n"):
                if req.startswith("-e"):
                    if "@" not in req:
                        # Editable requirement without pinned commit.
                        break
                elif req.strip() and not req.startswith("#"):
                    if not set(">=<") & set(req):
                        # PyPI requirement without version.
                        break
            else:
                # All requirements are pinned.
                return
        pip("-r %s/%s" % (env.proj_path, env.reqs_path))


###########################################
# Utils and wrappers for various commands #
###########################################

def _print(output):
    print()
    print(output)
    print()


def print_command(command):
    _print(blue("$ ", bold=True) +
           yellow(command, bold=True) +
           red(" ->", bold=True))


@task
def run(command, show=True):
    """
    Runs a shell comand on the remote server.
    """
    if show:
        print_command(command)
    with hide("running"):
        return _run(command)


@task
def sudo(command, show=True):
    """
    Runs a command as sudo.
    """
    if show:
        print_command(command)
    with hide("running"):
        return _sudo(command)


def log_call(func):
    @wraps(func)
    def logged(*args, **kawrgs):
        header = "-" * len(func.__name__)
        _print(green("\n".join([header, func.__name__, header]), bold=True))
        return func(*args, **kawrgs)
    return logged


def get_templates():
    """
    Returns each of the templates with env vars injected.
    """
    injected = {}
    for name, data in templates.items():
        injected[name] = dict([(k, v % env) for k, v in data.items()])
    return injected


def upload_template_and_reload(name):
    """
    Uploads a template only if it has changed, and if so, reload a
    related service.
    """
    template = get_templates()[name]
    local_path = template["local_path"]
    if not os.path.exists(local_path):
        project_root = os.path.dirname(os.path.abspath(__file__))
        local_path = os.path.join(project_root, local_path)
    remote_path = template["remote_path"]
    reload_command = template.get("reload_command")
    owner = template.get("owner")
    mode = template.get("mode")
    remote_data = ""
    if exists(remote_path):
        with hide("stdout"):
            remote_data = sudo("cat %s" % remote_path, show=False)
    with open(local_path, "r") as f:
        local_data = f.read()
        # Escape all non-string-formatting-placeholder occurrences of '%':
        local_data = re.sub(r"%(?!\(\w+\)s)", "%%", local_data)
        if "%(db_pass)s" in local_data:
            env.db_pass = db_pass()
        local_data %= env
    clean = lambda s: s.replace("\n", "").replace("\r", "").strip()
    if clean(remote_data) == clean(local_data):
        return
    upload_template(local_path, remote_path, env, use_sudo=True, backup=False)
    if owner:
        sudo("chown %s %s" % (owner, remote_path))
    if mode:
        sudo("chmod %s %s" % (mode, remote_path))
    if reload_command:
        sudo(reload_command)


def db_pass():
    """
    Prompts for the database password if unknown.
    """
    if not env.db_pass:
        env.db_pass = getpass("Enter the database password: ")
    return env.db_pass


@task
def apt(packages):
    """
    Installs one or more system packages via apt.
    """
    return sudo("apt-get install -y -q " + packages)


@task
def pip(packages):
    """
    Installs one or more Python packages within the virtual environment.
    """
    with virtualenv():
        return sudo("pip install %s" % packages)


def postgres(command):
    """
    Runs the given command as the postgres user.
    """
    show = not command.startswith("psql")
    return run("sudo -u root sudo -u postgres %s" % command, show=show)


@task
def psql(sql, show=True):
    """
    Runs SQL against the project's database.
    """
    out = postgres('psql -c "%s"' % sql)
    if show:
        print_command(sql)
    return out


@task
def backup(filename):
    """
    Backs up the database.
    """
    return postgres("pg_dump -Fc %s > %s" % (env.proj_name, filename))


@task
def restore(filename):
    """
    Restores the database.
    """
    return postgres("pg_restore -c -d %s %s" % (env.proj_name, filename))


@task
def python(code, show=True):
    """
    Runs Python code in the project's virtual environment, with Django loaded.
    """
    #pdb.set_trace()
    setup = "import os; os.environ[\'DJANGO_SETTINGS_MODULE\']=\'settings\';"
    full_code = 'python -c "%s%s"' % (setup, code.replace("`", "\\\`"))
    with project():
        result = run(full_code, show=False)
        if show:
            print_command(code)
    return result


def static():
    """
    Returns the live STATIC_ROOT directory.
    """
    return python("from django.conf import settings;"
                  "print settings.STATIC_ROOT", show=False).split("\n")[-1]


@task
def manage(command):
    """
    Runs a Django management command.
    """
    return run("%s %s" % (env.manage, command))


#########################
# Install and configure #
#########################
@task
@log_call
def all():
    """
    Installs everything required on a new system and deploy.
    From the base software, up to the deployed project.
    """
    install()
    create_virtualenv()
    create_SSH()
    create_git()
    #create_DB()
    set_SSL()
    
    create_django_user()
    set_password_django_user()
    upload_rungunicorn_script()
    upload_supervisord_conf()
    create_nginx()
    
    set_project()


@task
@log_call
def install():
    """
    Installs the base system and Python requirements for the entire server.
    """
    #locale = "LC_ALL=%s" % env.locale
    #with hide("stdout"):
    #    if locale not in sudo("cat /etc/default/locale"):
    #        sudo("update-locale %s" % locale)
    #        run("exit")
    sudo("apt-get update -y -q")
    apt("nginx libjpeg-dev python-dev python-setuptools git-core "
        "libpq-dev memcached supervisor")
    #apt("mysql-server mysql-client")
    apt("openssh-server libev-dev python-all-dev build-essential")
    apt("debconf-utils")

    sudo("easy_install pip")
    #sudo("pip install virtualenv mercurial")
    apt("python-virtualenv virtualenvwrapper")
    #sudo("apt-get install -y python-virtualenv virtualenvwrapper")
    
@task
@log_call
def create_virtualenv():
    """
    Create a new virtual environment & git.
    """
    #pdb.set_trace()
    if not exists(env.venv_home):
        run("mkdir %s" % env.venv_home)
    
    with cd(env.venv_home):
        if exists(env.proj_name):
            prompt = input("\nVirtualenv exists: %s"
                           "\nWould you like to replace it? (yes/no) "
                           % env.proj_name)
            if prompt.lower() != "yes":
                print("\nAborting!")
                return False
            remove()
        
        run("export WORKON_HOME=$HOME/.virtualenvs")
        run("export PIP_VIRTUALENV_BASE=$WORKON_HOME")
        run("source /usr/share/virtualenvwrapper/virtualenvwrapper.sh && mkvirtualenv %s"% env.proj_name)

@task
@log_call
def create_SSH():
    """
    Create a new ssh key.
    """
    #pdb.set_trace()
    ssh_path = "/home/%s/.ssh" % env.user
    if not exists(ssh_path):
        run("mkdir %s" % env.ssh_path)

    pub_path = ssh_path+"/id_rsa.pub"
    with cd(ssh_path):
        if not exists(pub_path):
            run('ssh-keygen -t rsa')
        run("cat %s"% pub_path)
        input("\nSet SSH & Press Enter!")

@task
@log_call
def create_git():
    """
    Create a new git.
    """
    if not exists(env.venv_path):
        print("\nVirtual env path isn't exists!")
        return False
    
    run("git clone %s %s" % (env.repo_url, env.proj_path))

def mysql_execute(sql, user, password):
    """ Executes passed sql command using mysql shell. """
    #user = user or env.conf.DB_USER
    from fabric.api import prompt
    sql = sql.replace('"', r'\"')
    #if password == None:
    #    password = prompt('Please enter MySQL root password:')
    return run('echo "%s" | mysql --user="%s" --password="%s"' % (sql, user , password))

@task
@log_call
def create_DB():
    """
    Create DB and DB user.
    """
    from fabric.api import settings, prompt
    
    with settings(hide('warnings', 'stderr'), warn_only=True):
        result = sudo('dpkg-query --show mysql-server')
    if result.failed is False:
        warn('MySQL is already installed')
    else:
        #sudo('echo "mysql-server-5.0 mysql-server/root_password password %s" | debconf-set-selections' % env.db_root_pass)
        #sudo('echo "mysql-server-5.0 mysql-server/root_password_again password %s" | debconf-set-selections' % env.db_root_pass)
        run('echo "mysql-server-5.0 mysql-server/root_password password %s" | sudo debconf-set-selections' % env.db_root_pass)
        run('echo "mysql-server-5.0 mysql-server/root_password_again password %s" | sudo debconf-set-selections' % env.db_root_pass)
        apt('mysql-server mysql-client')
    
    upload_template_and_reload("mysql")
    
    sql = 'CREATE DATABASE %(proj_name)s DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci' % env
    mysql_execute(sql, 'root', env.db_root_pass)
    
    sql = """CREATE USER '%(proj_name)s'@'%%' IDENTIFIED BY '%(db_pass)s';""" % env
    #sql = """CREATE USER '%(proj_name)s'@'localhost' IDENTIFIED BY '%(db_pass)s';""" % env
    mysql_execute(sql, 'root', env.db_root_pass)
    
    sql = """GRANT ALL ON %(proj_name)s.* TO '%(proj_name)s'@'%%'; FLUSH PRIVILEGES;""" % env
    #sql = """GRANT ALL ON %(proj_name)s.* TO '%(proj_name)s'@'localhost'; FLUSH PRIVILEGES;""" % env
    mysql_execute(sql, 'root', env.db_root_pass)
    
    sudo('service mysql restart')
    
@task
@log_call
def remove_DB():
    """
    Remove DB and DB user.
    """
    
    sql = 'DROP DATABASE %(proj_name)s' % env
    mysql_execute(sql, 'root', env.db_root_pass)
    sql = """DROP USER '%(proj_name)s';""" % env
    mysql_execute(sql, 'root', env.db_root_pass)
    
    sudo("service mysql stop")
    
    sudo("apt-get remove -y --purge mysql-server mysql-client")
    #sudo("netstat -tap | grep mysql")
    sudo("apt-get remove -y --purge mysql-server*")
    sudo("apt-get remove -y --purge mysql-client*")
    
@task
@log_call
def set_SSL():
    """
    # Set up SSL certificate.
    """
    if not env.ssl_disabled:
        conf_path = "/etc/nginx/conf"
        if not exists(conf_path):
            sudo("mkdir %s" % conf_path)
        with cd(conf_path):
            crt_file = env.proj_name + ".crt"
            key_file = env.proj_name + ".key"
            if not exists(crt_file) and not exists(key_file):
                try:
                    crt_local, = glob(join("deploy", "*.crt"))
                    key_local, = glob(join("deploy", "*.key"))
                except ValueError:
                    parts = (crt_file, key_file, env.domains[0])
                    sudo("openssl req -new -x509 -nodes -out %s -keyout %s "
                         "-subj '/CN=%s' -days 3650" % parts)
                else:
                    upload_template(crt_local, crt_file, use_sudo=True)
                    upload_template(key_local, key_file, use_sudo=True)

@task
@log_call
def migrate():
    """
    migrate.
    """
    manage('migrate')

@task
@log_call
def set_project():
    """
    Set up project.
    """
    upload_template_and_reload("settings")
    
    with project():
        if env.reqs_path:
            pip("-r %s/%s" % (env.proj_path, env.reqs_path))
        
        apt('libmysqlclient-dev')
        pip("fabric django python-social-auth "
            "gunicorn django-hosts mysql-python django-crontab pytz")
    manage('migrate')
    
    manage('createsuperuser')

@task
@log_call           
def create_django_user():
    """
    create django user
    """
    sudo('groupadd --system %(django_user)s' % env)
    sudo('useradd --system --gid %(django_user)s --home %(venv_path)s %(django_user)s' % env)
    
    sudo('chown -R %(django_user)s:%(django_user)s %(venv_path)s' % env)
    sudo('chmod -R g+w %(venv_path)s' % env)
    
    sudo('usermod -a -G %(django_user)s %(user)s' % env)
    
@task
@log_call
def set_password_django_user():
    """
    set password django user
    """
    sudo('passwd %(django_user)s' % env)

@task
@log_call
def upload_rungunicorn_script():
    """
    upload rungunicorn conf
    """
    sudo('mkdir -p %s' % dirname(env.gunicorn_logfile))
    sudo('chown %s %s' % (env.django_user, dirname(env.gunicorn_logfile)))
    sudo('chmod -R 775 %s' % dirname(env.gunicorn_logfile))
    sudo('touch %s' % env.gunicorn_logfile)
    sudo('chown %s %s' % (env.django_user, env.gunicorn_logfile))
    sudo('mkdir -p %s' % dirname(env.rungunicorn_script))
    
    upload_template_and_reload("gunicorn")
    sudo('chmod u+x %s' % env.rungunicorn_script)
    sudo('chown -R %(django_user)s:%(django_user)s %(rungunicorn_script)s' % env)

@task
@log_call
def upload_supervisord_conf():
    ''' upload supervisor conf '''
    
    sudo('mkdir -p %s' % dirname(env.supervisor_stdout_logfile))
    sudo('chown %s %s' % (env.django_user, dirname(env.supervisor_stdout_logfile)))
    sudo('chmod -R 775 %s' % dirname(env.supervisor_stdout_logfile))
    sudo('touch %s' % env.supervisor_stdout_logfile)
    sudo('chown %s %s' % (env.django_user, env.supervisor_stdout_logfile))
    
    sudo('mkdir -p %s' % dirname(env.supervisord_conf_file))
    
    upload_template_and_reload("supervisor")
    
    sudo('%(supervisorctl)s reread' % env)
    sudo('%(supervisorctl)s update' % env)

@task
@log_call
def create_nginx():
    '''
    create nginx
    '''
    upload_template_and_reload("nginx")
    
    sudo('unlink /etc/nginx/sites-enabled/default')
    sudo("service nginx restart")
    

@task
@log_call
def restart():
    """
    Restart gunicorn worker processes for the project.
    """
    pid_path = "%s/gunicorn.pid" % env.proj_path
    if exists(pid_path):
        #sudo("kill -HUP `cat %s`" % pid_path)
        #$sudo("kill -HUP $(cat %s)" % pid_path)
        run("cat %s" % pid_path)
        prompt = input("\npid number(upper number) : ")
        sudo("kill -HUP %s" % prompt)
    else:
        start_args = (env.proj_name, env.proj_name)
        sudo("supervisorctl start %s:gunicorn_%s" % start_args)


##########
# Deploy #
##########
@task
@log_call
def pull_git():
    """
    run  git pull
    """
    with cd(env.proj_path):
        run("git pull")


@task
@log_call
def collectstatic():
    """
    collect static for mangae django
    """
    manage('collectstatic')

@task
@log_call
def restart_supervisor():
    """
    restart supervisor
    """
    sudo("supervisorctl restart %(proj_name)s" % env)

@task
@log_call
def upload_local_settings():
    """
    upload_local_settings
    """
    upload_template_and_reload("settings")

@task
@log_call
def upload_nginx():
    '''
    create nginx
    '''
    upload_template_and_reload("nginx")
    sudo("service nginx restart")
    
@task
@log_call
def deploy():
    """
    Deploy latest version of the project.
    Check out the latest version of the project from version
    control, install new requirements, sync and migrate the database,
    collect any new static assets, and restart gunicorn's work
    processes for the project.
    """
    for name in get_templates():
        upload_template_and_reload(name)
    with project():
        #backup("last.db")
        
        #static_dir = static()
        #if exists(static_dir):
        #    run("tar -cf last.tar %s" % static_dir)
        
        git = env.git
        last_commit = "git rev-parse HEAD"
        run("%s > last.commit" % last_commit)
        with update_changed_requirements():
            run("git pull origin master -f")
        
        #manage("collectstatic -v 0 --noinput")
        #manage("syncdb --noinput")
        #manage("migrate --noinput")
    restart()
    return True

@task
@log_call
def remove():
    """
    Blow away the current project.
    """
    if exists(env.venv_path):
        sudo("rm -rf %s" % env.venv_path)
    #for template in get_templates().values():
    #    remote_path = template["remote_path"]
    #    if exists(remote_path):
    #        sudo("rm %s" % remote_path)
    #psql("DROP DATABASE IF EXISTS %s;" % env.proj_name)
    #psql("DROP USER IF EXISTS %s;" % env.proj_name)
