from fabric.api import local, cd, task, run
import os

REPO = "git@github.com:dangqhuy/practice-flask.git"
@task
def prepare_deloy():
        if os.path.isdir('/home/huydang/practice-flask'):
            run("cd practice-flask/ ; git pull origin master")
        else:
            run("git clone {}".format(REPO))
            run("cd practice-flask/")

        run("pip install pipenv")
        run("pipenv install")
        run("pipenv shell export FLASK_APP=hello.py")
        run("pipenv shell pipenv run flask run")
