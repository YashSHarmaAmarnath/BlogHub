# Blaog website using Flask
---

## Features

1. **User Registration and Login:**
   - Users can register with a username and password.
   - Secure password storage using `bcrypt`.
   - Login functionality with session management.

2. **Blog Management:**
   - Create, update, delete, and view blogs.
   - Search for blogs by title, content, or author.
   - Comment on blogs with session-based user association.

3. **User Profile:**
   - View all blogs by a specific user.
   - Change password functionality with validation.

4. **Admin and Creator Information:**
   - View all creators (registered users) and their blogs.

---

## Prerequisites

1. **Software Requirements:**
   - Python 3.x
   - MongoDB server (locally hosted or cloud-based)
   - Flask framework and required dependencies (install with `pip`)

2. **Python Libraries:**
   Install the required libraries using:
   ```bash
   pip install flask flask-pymongo bcrypt
   ```

---

## Application Structure

- **Routes:**
  - `/`: Home page displaying blogs for the logged-in user.
  - `/create`: Create a new blog post.
  - `/blogs`: View all blogs.
  - `/login`: Login page for users.
  - `/register`: Registration page for new users.
  - `/logout`: Log out the current user.
  - `/Search`: Search for blogs by text or author.
  - `/read_more`: View a blog and its comments, and add comments.
  - `/delete`: Delete a blog post.
  - `/creator`: View all creators and their blogs.
  - `/viewWork/<username>`: View a specific creator's blogs.
  - `/update`: Update an existing blog post.
  - `/ChangePassword`: Change the logged-in user's password.

- **Templates:**
  - HTML templates for pages like login, registration, blogs, create, update, and search.
  - Use of Jinja2 templating for dynamic content.

- **Database Configuration:**
  - MongoDB is used as the database, with collections for:
    - `Users`: Stores user credentials.
    - `blogs`: Stores blog data.
    - `comments`: Stores blog comments.

---

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   https://github.com/YashSHarmaAmarnath/BlogHub.git
   cd BlogHub/app
   ```

2. **Configure MongoDB:**
   - Start the MongoDB server.
   - Ensure the database name is `blogs` and is accessible at `mongodb://localhost:27017/blogs`.

3. **Run the Application:**
   ```bash
   python views.py
   ```

4. **Access the Application:**
   - Open a browser and navigate to `http://127.0.0.1:5000/`.

---

## Usage

1. **Register a New User:**
   - Navigate to `/register` to create a new user account.

2. **Log In:**
   - Use your registered credentials to log in at `/login`.

3. **Create Blogs:**
   - Go to `/create` to add new blogs.

4. **Manage Blogs:**
   - View all blogs at `/blogs`.
   - Update or delete blogs as needed.

5. **Search Blogs:**
   - Use `/Search` to look up blogs based on keywords or author names.

6. **Comment on Blogs:**
   - Navigate to a specific blog's detail page via `/read_more` to add comments.

7. **Change Password:**
   - Update your password securely at `/ChangePassword`.

---

## Security Notes

- **Password Security:** 
  - All passwords are hashed using `bcrypt` before storing in the database.

- **Session Management:** 
  - `Flask-Session` is used for user session handling.

- **Database Queries:**
  - MongoDB's `find_one`, `find`, `insert_one`, and `update_one` operations are used to interact with the database.

---
