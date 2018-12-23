from flask import Flask, render_template, url_for, flash, request, redirect, session, abort
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from forms import *
from datetime import timedelta, datetime
from functools import wraps
from datamanager import *
from s3bucket import s3_upload, s3_delete_file, s3_generate_url
from random import choice


app = Flask(__name__)
app.secret_key = 'VerySecretKey'
app.config.from_pyfile('config.cfg')
mail = Mail(app)
s = URLSafeTimedSerializer('VerySecretKey')



def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not verify_session(session.get('user_id')):
            abort(404)
        return function(*args, **kwargs)
    return decorated_function



def redirect_if_user_in_session(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if  verify_session(session.get('user_id')):
            return redirect(url_for('home'))
        return function(*args, **kwargs)
    return decorated_function



def set_permanent_session(remember_me,days):
    if remember_me:
        session.permanent = True
        app.permanent_session_lifetime = timedelta(days=days)



def add_user_to_session(user):
    session['user_id'] = user['id']
    session['user_name'] = user['user_name']



def send_verification_token(user_data):
    email = user_data.get('email')
    user_name = user_data.get('user_name')
    token = s.dumps(email, salt='email-confirm')
    message = Message('Confirm Email', sender="forropcs@gmail.com", recipients=[email])
    link = url_for('confirm_email',user_name=user_name, token=token, _external=True)
    message.body = f"Your activation link is: {link}"
    mail.send(message)



@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404



@app.route('/',methods=['GET','POST'])
@redirect_if_user_in_session
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_email(form.email.data)
        if user and verify_password(form.password.data,user['password']):
            if not user.get('confirmed'):
                flash('Your account has not been confirmed yet!')
                return redirect(url_for('login'))
            set_permanent_session(form.remember_me.data,days=10)
            add_user_to_session(user)
            flash(f'You have been successfully logged in as: {session["user_name"]}')
            return redirect('home')
        flash("Wrong E-mail or Password!")
        return redirect(request.referrer)
    return render_template("login.html",form=form)



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



@app.route('/register',methods=['GET','POST'])
@redirect_if_user_in_session
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        add_user_to_db(form.data)
        send_verification_token(form.data)
        flash("Please verify your account through the link sent in your inbox!")
        return redirect(url_for('login'))
    return render_template("register.html",form=form)



@app.route('/confirm_email/')
def confirm_email():
    try:
        token = request.args.get('token')
        user_name = request.args.get('user_name')
        s.loads(token,salt='email-confirm',max_age=3600)
        confirm_account(user_name)
        flash('Your Account has been successfully confirmed!')
        return redirect(url_for('login'))
    except SignatureExpired:
        abort(404)



@app.route('/home')
@login_required
def home():
    posts = get_posts()
    for post in posts:
        files = get_post_files(post['id'])
        post['sample_img'] = s3_generate_url(choice(files)['filename'])
    return render_template('home.html',posts=posts)



@app.route('/new_story',methods=['GET','POST'])
@login_required
def new_story():
    form = PostForm()
    if form.validate_on_submit():
        data = form.data
        data['submission_time'] = datetime.now()
        data['user_id'] = session['user_id']
        data['post_id'] = add_post_to_db(data)
        for picture in data['pictures']:
            data['filename'] = picture.filename = create_random_filename(picture.filename)
            add_file_to_db(data)
            s3_upload(picture)
        return redirect(url_for('home'))
    return render_template("post.html",form=form)



@app.route('/delete_file/<filename>')
@login_required
def delete_file(filename):
    remove_file_from_db(filename)
    s3_delete_file(filename)
    return redirect(url_for('home'))




@app.route('/story/<int:post_id>')
@login_required
def story(post_id):
    post = get_post(post_id)
    files = get_post_files(post_id)
    for file in files:
        file['url'] = s3_generate_url(file['filename'])
    print(files)
    return render_template('story.html',post=post,files=files)



@app.route('/delete_posts')
@login_required
def delete_posts():
    files = get_files()
    for file in files:
        s3_delete_file(file['filename'])
    delete_records('posts')
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run()
