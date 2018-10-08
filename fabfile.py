from fabric.api import local, cd, task, run, env, sudo
import os

REPO = "https://github.com/dangqhuy/practice-flask.git"

env.hosts = ['18.222.128.254']
env.user = 'ubuntu'

def deloy():
    run("git clone {}".format(REPO))
    run("cd practice-flask/")
    run("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
    sudo("python2 get-pip.py")
    sudo("apt-get install python-flask")
    sudo("python2 -m pip install psycopg2")
    sudo("python2 -m pip install flask-bcrypt")
    sudo("python2 -m pip install gevent")
    sudo("python2 -m pip install flask-wtf")
    run("cd practice-flask/ ; export FLASK_APP=hello.py ; python -m flask run")
