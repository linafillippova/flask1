import random
from functools import lru_cache
from flask import Flask, render_template
from faker import Faker

from flask import request, make_response, redirect, url_for
from .forms import PhoneForm

fake = Faker()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qWpoirec23@geG0r00'

application = app

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

def generate_comments(replies=True):
    comments = []
    for _ in range(random.randint(1, 3)):
        comment = {
            'author': fake.name(),
            'text': fake.text(),
            'date': fake.date_time_between(start_date='-2y', end_date='now')
        }
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments

def generate_post(i):
    return {
        'id': i,
        'title': 'Заголовок поста',
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i]}.jpg',
        'comments': generate_comments()
    }

@lru_cache
def posts_list():
    return sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list())

@app.route('/posts/<int:post_id>')
def post(post_id):
    p = None
    for post in posts_list():
        if post['id'] == post_id:
            p = post
            break
    if not p:
        return "Post not found", 404

    return render_template('post.html', title=p['title'], post=p)

@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')

@app.route('/url_params')
def url_params():
    return render_template('url_params.html', params=request.args)

@app.route('/headers')
def headers():
    return render_template('headers.html', headers=request.headers)

@app.route('/cookies')
def cookies():
    value = request.cookies.get('my_cookie')
    response = make_response(render_template('cookies.html', my_cookie=value))

    if value:
        response.delete_cookie('my_cookie')
    else:
        response.set_cookie('my_cookie', 'My Cookie Value')

    return response

@app.route('/form', methods=['GET', 'POST'])
def phone_form():
    form = PhoneForm()
    formatted_number = None

    if form.validate_on_submit():
        try:
            formatted_number = form.validate_phone_number(form.phone_number)
        except ValidationError as e:
            form.phone_number.errors.append(str(e))

    return render_template('form.html', form=form, formatted_number=formatted_number)