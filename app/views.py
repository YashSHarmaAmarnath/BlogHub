from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

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
        return render_template("index.html",userName=currentuser.get('userName'))
    return redirect('/login')

@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Handle form submission
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        image = request.files['image']
        
        # Save the image to the filesystem
        try:
            image.save(image.filename)
        except:
            pass
        
        # Insert blog post data into MongoDB
        collection = mongo.db.blogs
        collection.insert_one({'title': title, 'content': content, 'author': author, 'image': image.filename})
        
        # Redirect to the blogs page
        return redirect(url_for('all_blogs'))
    
    return render_template("create.html",userName=currentuser.get('userName'))

@app.route("/blogs")
def all_blogs():
    # Retrieve all blog posts from MongoDB
    blogs = mongo.db.blogs.find()
    return render_template("blogs.html", blogs=blogs,userName=currentuser.get('userName') )

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
def regis():
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

if __name__ == '__main__':
    app.run(debug=True)
