from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(240))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return str(self.id)


@app.route('/blog', methods=['GET'])
def blog():
    posts = Blog.query.all()
        
    post_id = request.args.get('id')
    if post_id:
        single_post = Blog.query.get(post_id)
        return render_template('single_post.html', single_post=single_post)
    else:
        return render_template('blog.html', posts=posts)

@app.route('/', methods=['GET'])
def index():
    return redirect('/blog')
   
@app.route('/newpost', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':

        blog_title = request.form['blog-title']
        blog_body = request.form['blog-body']

        body_error = ''
        title_error = ''

        if blog_title == '':
            title_error = 'please enter a title for your blog.'  

        if blog_body == '':
            body_error = 'please enter a blog post.'  

        if not title_error and not body_error:           
            new_post = Blog(blog_title, blog_body)
            db.session.add(new_post)
            db.session.commit()            
           
            blog = Blog.query.get(new_post.id)
            return redirect('/blog?id={0}'.format(blog))

        else:
            return render_template('newpost.html', blog_title=blog_title, title="Add Blog Entry",
            blog_body=blog_body, title_error=title_error, body_error=body_error)
        
    else:
        return render_template('newpost.html')
  
   
   

if __name__ == '__main__':
    app.run()

