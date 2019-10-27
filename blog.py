from flask import Flask, render_template
import sqlite3


app = Flask(__name__)
title = "MyNotes"

def connect2db():
   db = sqlite3.connect("blog-posts.db")
   wand = db.cursor()
   return wand

def get_posts():
   wand = connect2db()
   wand.execute("SELECT * from posts")
   return wand.fetchall()

def get_post(post_id):
   wand = connect2db()
   wand.execute("SELECT * FROM posts WHERE id = '%s'" % post_id)
   post = wand.fetchone()
   return post

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return """<center><h1 style="color: red;"> The page doesn't exist.
    </h1></center>""", 404

@app.route('/posts/<post>', methods=['GET'])
def posts(post):
   post = get_post(post)
   post_title = post[0]
   post_subtitle = post[1]
   post_body = post[2]
   post_category = post[3]
   image = post[4]
   date = post[6]
   return render_template("post.html", post_title=post_title, body=post_body, category=post_category, image=image, title=title)


@app.route('/')
def home_page():
   return render_template('home.html', posts=get_posts(), title=title)

if __name__ == '__main__':
   app.run(debug=True)