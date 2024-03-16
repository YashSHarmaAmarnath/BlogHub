from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask_pymongo import PyMongo
from bson import ObjectId  
import datetime
logined = False
currentuser  = None
app = Flask(__name__)

# Configuration for MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/blogs"
mongo = PyMongo(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    # print(currentuser,'///')
    if logined:
        userid = currentuser.get('userName')
        blogs = mongo.db.blogs.find({ 'userid': userid })
 
        return render_template("index.html",userName=userid,logined=logined,blogs=blogs)
    return redirect('/login')

@app.route("/create", methods=['GET', 'POST'])
def create():
    if not logined:
        return redirect('/login')
        
    if request.method == 'POST':
        # Handle form submission
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        date = datetime.date.today() 
        userid = userName=currentuser.get('userName')
        # Insert blog post data into MongoDB
        collection = mongo.db.blogs
        collection.insert_one({'title': title, 'content': content, 'author': author,'date':date.strftime("%Y-%m-%d"), 'userid': userid})
        
        # Redirect to the blogs page
        return redirect(url_for('all_blogs'))
    
    return render_template("create.html",userName=currentuser.get('userName'),logined=logined)

@app.route("/blogs")
def all_blogs():
    if not logined:
        return redirect('/login')
        
    # Retrieve all blog posts from MongoDB
    blogs = mongo.db.blogs.find()
    return render_template("blogs.html", blogs=blogs,userName=currentuser.get('userName'),logined=logined )

@app.route("/login", methods=['GET', 'POST'])
def login():
    global logined, currentuser
    msg = ''
    collection = mongo.db.Users
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']
        user = collection.find_one({'userName': userName}, {'_id': 0})

        if user:
            stored_pass = user.get('password')
            if stored_pass:
                if password == stored_pass:
                    # print('logined')
                    logined = True
                    currentuser = user
                    # print(currentuser)
                    # return redirect('/')
                    return redirect('/')
                else:
                    msg = 'Incorrect password'
        else:
            msg = 'Incorrect user name or password'
    return render_template("login.html",message = msg)

@app.route("/register", methods=['GET', 'POST'])
def register():
    global logined, currentuser
    msg = ''
    collection = mongo.db.Users       
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']
        password1 = request.form['password1']
        if password == password1:
            collection.insert_one({'userName':userName,'password':password})
            return redirect('/login')
        else:
            msg = 'password does not match'
    return render_template("register.html",message = msg)

@app.route('/logout')
def logout():
    global logined,currentuser
    logined = False
    currentuser = None
    return redirect('/login')

@app.route("/Search",methods=['GET', 'POST'])
def search():
    if not logined:
        return redirect('/login')
        
    if request.method == 'POST' and logined:
        query = request.form['query']
        blogs = mongo.db.blogs.find({ '$text': { '$search': query } })
        blogs1 = mongo.db.blogs.find({ 'author': { '$regex': query, '$options': 'i' } })
        msg = f'Search reasult for :{query}'
        return render_template("blogs.html", blogs=list(blogs)+list(blogs1),userName=currentuser.get('userName'),logined=logined ,msg=msg)
    return render_template("blogs.html", blogs='blogs')

@app.route('/read_more',methods=['GET','POST'])
def read_more():
    if not logined:
        return redirect('/login')
        
    if request.method == 'POST':
        # Assuming you're passing the blog ID as a form parameter named 'blog_id'
        blog_id = request.form.get('blog_id')
        # print(blog_id)
        # Retrieve the specific blog post from MongoDB using its ID
        blog = mongo.db.blogs.find_one({'_id': ObjectId(blog_id)})
        if blog:
            # Render the read more template with the specific blog post
            return render_template("read_more.html", blog=blog, userName=currentuser.get('userName'), logined=logined)
        else:
            # If the blog post is not found, you can handle it appropriately
            return "Blog post not found."
    else:
        # If the request method is not POST, handle it accordingly
        return redirect('/blogs')
@app.route('/delete',methods=['GET','POST'])
def delete():
    if not logined:
        return redirect('/login')
    if request.method == 'POST':
        # Assuming you're passing the blog ID as a form parameter named 'blog_id'
        blog_id = request.form.get('blog_id')
        if blog_id:
            mongo.db.blogs.delete_one({'_id': ObjectId(blog_id)})
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
