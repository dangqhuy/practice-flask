from gevent.pywsgi import WSGIServer
from gevent import monkey
from flask import Flask, render_template, make_response, request, flash, redirect, url_for
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '95cd8af52647b2a8e726d3badf339c'
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
monkey.patch_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(120), nullable=True)
    password = db.Conlumn(db.String(60), nullable=False)

    def __repr__(self):
        return "User('{username}', '{email}', '{image_file}')"
        .format(username=self.username, email=self.email, image_file=self.image_file)



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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'dangqhuy@gmail.com' and form.password.data == '123qweasd':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'warning')
    return render_template('login.html', title='Login', form=form)


@run_with_reloader
def run_server():
    http_server = WSGIServer(('', 5000),  DebuggedApplication(app))
    http_server.serve_forever()




if __name__ == "__main__":
  
    app.run(debug=True, use_reloader=False)
    run_server()
