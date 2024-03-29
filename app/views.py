from flask import Flask, render_template, request, redirect, url_for,jsonify,session
from flask_pymongo import PyMongo
from bson import ObjectId  
import datetime , bcrypt
# logined = False
# currentuser  = None
app = Flask(__name__)
app.secret_key = 'BLOGAPP'
# database = open('database.txt','r').read()
# Configuration for MongoDB
app.config["MONGO_URI"] = 'mongodb://localhost:27017/blogs'
mongo = PyMongo(app)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

@app.route("/", methods=['GET', 'POST'])
def index():
    # print(currentuser,'///')
    # if 'username' not in session:
    #     return redirect('/login')
    if 'username' in session:
        userid = session["username"]
        blogs = mongo.db.blogs.find({ 'userid': userid })
 
        return render_template("index.html",userName=userid,blogs=blogs)
    return redirect('/login')

@app.route("/create", methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect('/login')
        
    if request.method == 'POST':
        # Handle form submission
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        date = datetime.date.today() 
        userid =session["username"]
        # Insert blog post data into MongoDB
        collection = mongo.db.blogs
        collection.insert_one({'title': title, 'content': content, 'author': author,'date':date.strftime("%Y-%m-%d"), 'userid': userid})
        
        # Redirect to the blogs page
        return redirect(url_for('all_blogs'))
    
    return render_template("create.html",userName=session["username"])

@app.route("/blogs")
def all_blogs():
    if 'username' not in session:
        return redirect('/login')
        
    # Retrieve all blog posts from MongoDB
    blogs = mongo.db.blogs.find()
    return render_template("blogs.html", blogs=blogs,userName=session["username"] )

@app.route("/login", methods=['GET', 'POST'])
def login():
    global  currentuser
    msg = ''
    collection = mongo.db.Users
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password'].encode('utf-8')
        # password = hash_password(request.form['password'])
        user = collection.find_one({'userName': userName}, {'_id': 0})

        if user:
            stored_pass_hash = user.get('password')
            # print(f"{stored_pass_hash}\n\n\n{password}")
            if stored_pass_hash and bcrypt.checkpw(password, stored_pass_hash):
                # if password == stored_pass:
                    # print('logined')
                    session['username'] = request.form['username']
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
    msg = ''
    collection = mongo.db.Users       
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']
        password1 = request.form['password1']
        user = collection.find_one({'userName':userName})
        print(user)
        if user:

            print('user already exist')
            msg = 'User Name already taken'
            return render_template("register.html",message = msg)
        elif password == password1:
            hashed_password = hash_password(password)
            collection.insert_one({'userName':userName,'password':hashed_password})
            return redirect('/login')

        else:
            msg += 'password does not match'
    return render_template("register.html",message = msg)

@app.route('/logout')
def logout():
    # logined = False
    # currentuser = None
    session.pop('username', None)
    return redirect('/login')

@app.route("/Search",methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect('/login')
        
    if request.method == 'POST' :
        query = request.form['query']
        blogs = mongo.db.blogs.find({ '$text': { '$search': query } })
        blogs1 = mongo.db.blogs.find({ 'author': { '$regex': query, '$options': 'i' } })
        msg = f'Search reasult for :{query}'
        return render_template("blogs.html", blogs=list(blogs)+list(blogs1),userName=session["username"] ,msg=msg)
    return render_template("blogs.html", blogs='blogs')

@app.route('/read_more',methods=['GET','POST'])
def read_more():
    if 'username' not in session:
        
        return redirect('/login')
    if request.method == 'POST':
        blog_id = request.form.get('blog_id')
        if request.form.get('action') == 'comment':
            print('comment added')
            comment = request.form['comment_data']
            if comment is not None and comment!='':
                mongo.db.comments.insert_one({'userName':session["username"],'comment':comment,'blog_id':ObjectId(blog_id) })
        blog = mongo.db.blogs.find_one({'_id': ObjectId(blog_id)})
        comments = mongo.db.comments.find({'blog_id':ObjectId(blog_id)})
        if blog:
            return render_template("read_more.html", blog=blog,comments=comments, userName=session["username"])
        else:
            return "Blog post not found."
    else:
        return redirect('/blogs')
@app.route('/delete',methods=['GET','POST'])
def delete():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        # Assuming you're passing the blog ID as a form parameter named 'blog_id'
        blog_id = request.form.get('blog_id')
        if blog_id:
            mongo.db.blogs.delete_one({'_id': ObjectId(blog_id)})
    
    return redirect('/')

@app.route('/creator',methods=['GET','POST'])
def creator():
    # if 'username' not in session:
    if 'username' not in session:
        return redirect('/login')
    users = mongo.db.Users.find({},{'password':0,'_id':0})
    return render_template('creator.html',users =users,userName=session["username"] )

@app.route('/viewWork/<username>')
def viewWork(username):
    if 'username' not in session:
        return redirect('/login')
    user = mongo.db.Users.find_one({'userName': username}, {'_id': 0})
    if user:
        blogs = mongo.db.blogs.find({ 'userid': username })
        return render_template('viewWork.html',userName=session["username"],user = username,blogs = blogs)
    else:
        return render_template('404.html')
    
@app.route('/update',methods=['GET','POST'])
def update():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['action'] == 'toupdate':
            blog_id = request.form['blog_id']
            blog = mongo.db.blogs.find_one({'_id': ObjectId(blog_id)})
            if blog:
                return render_template('update.html',blog=blog,userName=session["username"],)
            else:
                return 'no blog like this'
        if request.form['action'] == 'update':
            title = request.form['title']
            content = request.form['content']
            author = request.form['author']
            blog_id = request.form['blog_id']
            mongo.db.blogs.update_one({'_id': ObjectId(blog_id)}, {'$set': {'title': title, 'content': content, 'author': author}})
   
    return redirect('/')

@app.route('/ChangePassword',methods=['GET','POST'])
def ChangePassword():
    if 'username' not in session:
        return redirect('/login')
    msg = ''
    user  = mongo.db.Users.find_one({'userName': session['username']}, {'_id': 0})
    stored_pass_hash = user.get('password')
    userName = user.get('userName')
    if request.method == 'POST':
        OldPass = request.form['oldpassword']
        NewPass = request.form['newpassword']
        if not bcrypt.checkpw( OldPass.encode('utf-8'), stored_pass_hash):
            msg = "Old password doesn't match; please retry"
            return render_template('ChangePassword.html',user = userName,message= msg)
        elif NewPass.encode('utf-8') ==  OldPass.encode('utf-8'):
            msg = "New password cannot be the same as the old one"
            return render_template('ChangePassword.html',user = userName,message= msg)
        else:
            NewPass = hash_password(NewPass)
            mongo.db.Users.update_one({'userName': userName}, {'$set': {'password':NewPass }})
            return redirect('/')


    return render_template('ChangePassword.html',user = userName,message= msg)

if __name__ == '__main__':
    app.run(debug=True)

