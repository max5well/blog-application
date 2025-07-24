from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_PATH = os.path.join('data', 'posts.json')

def load_posts():
    with open(DATA_PATH) as f:
        return json.load(f)

def save_posts(posts):
    with open(DATA_PATH, 'w') as f:
        json.dump(posts, f, indent=2)

def fetch_post_by_id(post_id):
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        if title and author and content:
            blog_posts = load_posts()
            new_id = max((post['id'] for post in blog_posts), default=0) + 1

            new_post = {
                'id': new_id,
                'title': title,
                'author': author,
                'content': content
            }

            blog_posts.append(new_post)
            save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    blog_posts = load_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_posts(blog_posts)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_posts()
    post = next((p for p in blog_posts if p['id'] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        if title and author and content:
            post['title'] = title
            post['author'] = author
            post['content'] = content
            save_posts(blog_posts)
            return redirect(url_for('index'))

    return render_template('update.html', post=post)

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    blog_posts = load_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] = post.get('likes', 0) + 1
            break
    save_posts(blog_posts)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
