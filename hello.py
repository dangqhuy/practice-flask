from gevent.pywsgi import WSGIServer
from gevent import monkey
from flask import Flask, render_template, make_response, request, flash, redirect, url_for
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
from forms import RegistrationForm, LoginForm, PostForm
from flask_bcrypt import Bcrypt
import psycopg2, itertools
import json, datetime


try:
    conn = psycopg2.connect("dbname='my_db' user='postgres' host='localhost' password='!dangqhuy!'")
except:
    print "I am ubable to connect to the database"
    exit()


app = Flask(__name__)
app.config['SECRET_KEY'] = '95cd8af52647b2a8e726d3badf339c'
bcrypt = Bcrypt()

listen = ['default']
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn_redis = redis.from_url(redis_url)

monkey.patch_all()


@app.route('/')
def home():
    user = None
    keys = ('email', 'author', 'title', 'content', 'date_posted')
    posts = []
    dict_posts = []
    with conn.cursor() as cur:
        cur.execute('''SELECT 
                        my_user.email,
                        my_user.username,
                        post.title,
                        post.content,
                        post.created
                        FROM my_user
                        INNER JOIN post ON my_user.id = post.user_id
                        ORDER BY post.created DESC
                    ''')
        posts = cur.fetchall()
    for post in posts:
        dict_posts.append(dict(itertools.izip(keys, post)))

    if request.cookies.get('user'):
        user = json.loads(request.cookies.get('user'))
    return render_template('home.html', user=user, posts=dict_posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO my_user (email, username, password) VALUES (%s, %s, %s)",
                (form.email.data, form.username.data, bcrypt.generate_password_hash(form.password.data).decode('utf-8')))
                conn.commit()
        except:
            flash('Sign Up Unsuccesful', 'danger')
            return redirect(url_for('register'))
        flash('Account created for {username}!'.format(username=form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    users = None
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM my_user")
        users = cur.fetchall()
        print(users)
    keys = ('id', 'email', 'username', 'password')
    dict_users = []
    
    for user in users:
        dict_users.append(dict(itertools.izip(keys, user)))

    print(dict_users)
    
    if form.validate_on_submit():
        for user in dict_users:
            if form.email.data == user.get('email') and bcrypt.check_password_hash(user.get('password'), form.password.data):
                flash('You have been logged in!', 'success')
                resp = app.make_response(redirect(url_for('home')))
                resp.set_cookie('user', json.dumps(user))
                return resp
        else:
            flash('Login Unsuccessful. Please check username and password', 'warning')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('user', expires=0)
    return resp


@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    user = json.loads(request.cookies.get('user'))

    if form.validate_on_submit():
        try:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO post (title, content, user_id, created) VALUES (%s, %s, %s, %s)',
                (form.title.data, form.content.data, user.get('id'), datetime.datetime.now()))
                conn.commit()
        except:
            flash('Post Unsuccessful', 'danger')
        flash('Post Successful', 'success')
        return redirect(url_for('home'))
    return render_template('post.html', title='Post', form=form, user=user)

@run_with_reloader
def run_server():
    http_server = WSGIServer(('', 5000),  DebuggedApplication(app))
    http_server.serve_forever()




if __name__ == "__main__":

    app.run(debug=True, use_reloader=False)
    run_server()
