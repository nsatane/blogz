from flask import Flask, request, redirect, render_template 
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:1234@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

#creating blog class
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))

# initializer or constructor for blog class
    def __init__(self, title, body):
        self.title = title
        self.body = body
    
    


@app.route('/')
def index():
    return render_template('blog.html') 

# route to main blog page
@app.route('/blog')
def blog_index():
    # args getting id dictionary element from table
    blog_id = request.args.get('id')
    #blog = Blog.query.all()

    if blog_id:
        post = Blog.query.get(blog_id)
        blog_title = post.title
        blog_body = post.body
        # Use Case 1: Click on a blog entry's title on the main page 
        # and go to a blog's individual entry page.
        return render_template('entry.html', title="Blog Entry #" 
        + blog_id, blog_title=blog_title, blog_body=blog_body)


#handler route to new posts
@app.route('/newpost')
def new_post():
    return render_template('newpost.html', title="Add New Blog Entry")

#handler route to verify new post and body
@app.route('/newpost', methods=['GET','POST'])
def verify_post():
    
    blog_title = request.form['title']
    blog_body = request.form['body']
    title_error = ''
    body_error = ''
    new_blog = Blog(blog_title, blog_body)

    #error validation massage for empty fields
    if blog_title == "":
        title_error = "Please Enter Title for your Blog."
    elif blog_body == "":
        body_error = "Fill in the Body for your Blog."
    
    #add a new blog post and commit it to new id:
    if not title_error and not body_error:
        db.session.add(new_blog)
        db.session.commit()
        blog = new_blog.id
    #User Case2: After adding a new blog post, instead of going back to the main page, 
    # we go to that blog post's individual entry page. Redirect to specific blog id page.
        return redirect('/blog?id={0}'.format(blog))
    else:
        # return user to post page with errors.
        return render_template('newpost.html', title="Add New Blog Entry", 
        blog_title = blog_title, blog_body = blog_body, 
        title_error = title_error, body_error = body_error)

    

if __name__ == '__main__':
    app.run()