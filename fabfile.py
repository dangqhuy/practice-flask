from fabric.api import local, cd, task, run


REPO = "git@github.com:dangqhuy/practice-flask.git"
def prepare_deloy():
        run("cd ~/")
        run("git clone {}".format(REPO))
        run("cd practice-flask/")
        run("pip install pipenv")
        run("pipenv install")
        run("export FLASK_APP=hello.py pipenv run flask run")