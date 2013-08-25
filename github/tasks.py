from celery import task
import os
from subprocess import call
from django.conf import settings
from github.models import Repository, User


@task()
def fetch_repo(pk, ssh_key=None):
    repository = Repository.objects.get(pk=pk)
    location = os.path.join(settings.GITHUB_ROOT,
                            'repositories',
                            repository.owner.login,
                            repository.name)

    if not os.path.exists(location):
        cmd = 'git clone %s %s' % (repository.ssh_url, location)
    else:
        os.chdir(location)
        cmd = "git pull --rebase"

    if ssh_key:
        call(['ssh-agent', 'bash', '-c', 'ssh-add %s; %s' % (ssh_key, cmd)])
    else:
        call(['bash', '-c', cmd])

    return location

@task()
def setup_private_key(pk):
    user = User.objects.get(pk=pk)
    location = os.path.join(settings.SSH_KEY_DIR,
                            'id_rsa.%s' % user.login)

    if not os.path.exists(location):
        call(['ssh-keygen', '-f %s' % location, "-N ''"])

    with open(location + ".pub") as key:
        user.add_key(user.application.name, key.read())