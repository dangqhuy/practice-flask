from fabric.api import local, cd, task, run, env, sudo
import os

REPO = "https://github.com/dangqhuy/practice-flask.git"

env.hosts = ['18.224.95.78']
env.user = 'ubuntu'
def prepare_deloy():

    if os.path.isdir('/home/huydang/practice-flask'):
        run("cd practice-flask/ ; git pull origin master")
    else:
        sudo("apt install python-minimal")
        run("git clone {}".format(REPO))
        run("cd practice-flask/")
        run("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
        sudo("python2 get-pip.py")
        sudo("pip install pipenv")
        run("pipenv install")
        run("pipenv shell export FLASK_APP=hello.py")
        run("pipenv shell pipenv run flask run")
