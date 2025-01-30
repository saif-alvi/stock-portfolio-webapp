from flask import Flask, render_template
from markupsafe import escape
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    # return render_template('about.html', company_name="TestDriven.io")
    return render_template('about.html')
@app.route('/stocks/')
def stocks():
    return '<h2>Stock List...</h2>'
@app.route('/hello/<message>')
def hello_message(message):
    return f'<h1>Welcome {escape(message)}!</h1>'
@app.route('/blogposts/<int:post_id>')
def display_blog_post(post_id):
    return f'<h1>Blog Post #{post_id}...</h1>'