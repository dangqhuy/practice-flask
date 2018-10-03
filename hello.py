from gevent.pywsgi import WSGIServer
from gevent import monkey
from flask import Flask, render_template, make_response, request, flash, redirect, url_for
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
POSTGRES = {
    'user': 'postgres',
    'pw': '!dangqhuy!',
    'db': 'my_db',
    'host': 'localhost',
    'port': '5432',
}
posts = [
    {
        'title': 'POST 1',
        'author': 'Quoc Huy',
        'content': 'con cho can con meo',
        'date_posted': 'Oct 4, 2018'
        
    },
    {
        'title': 'POST 2',
        'author': 'Huy',
        'content': 'con meo can con cho',
        'date_posted': 'Oct 5, 2018'
        
    }
]
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
    %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db = SQLAlchemy(app)
monkey.patch_all()


@app.route('/')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {username}!'.format(username=form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


@run_with_reloader
def run_server():
    http_server = WSGIServer(('', 5000),  DebuggedApplication(app))
    http_server.serve_forever()




if __name__ == "__main__":
  
    app.run(debug=True, use_reloader=False)
    run_server()
