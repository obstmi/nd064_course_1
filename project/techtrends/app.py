import sqlite3, logging, sys

from datetime import datetime
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Variable to count the number of connections to the database
db_connection_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global db_connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    db_connection_count += 1
    return connection

# Function to get the amount of posts in the database
def get_post_count():
    connection = get_db_connection()
    post_count = connection.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    connection.close()
    return post_count

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Function to get the current timestamp with format: DD/Mon/YYYY HH:MM:SS
def get_timestamp():
    return datetime.now().strftime('%d/%b/%Y %H:%M:%S')

# Function to log a message at given level with a timestamp, default level is INFO
def log_message(level, message):
    log_level = getattr(logging, level.upper(), logging.INFO)
    app.logger.log(log_level, f' - - [{get_timestamp()}] {message}')

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Set Logging to stdout and loglevel to DEBUG
logging.basicConfig(
    handlers=[logging.StreamHandler(sys.stdout)],
    level=logging.DEBUG
)

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        log_message('INFO', f'Non existing article accessed! 404 page returned.')
        return render_template('404.html'), 404
    else:
        log_message('INFO', f'Article "{post["title"]}" retrieved!')
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    log_message('INFO', f'About Us page retrieved!')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            log_message('INFO', f'New Article with title: "{title}" created!')

            return redirect(url_for('index'))

    return render_template('create.html')

# Define the healthcheck endpoint
@app.route('/healthz')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    return response

# Define the metrics endpoint, which returns:
# the amount of connections to the database
# the amount of posts in the database
@app.route('/metrics')
def metrics():
    response = app.response_class(
            response=json.dumps({
                "db_connection_count": db_connection_count,
                "post_count": get_post_count()
            }),
            status=200,
            mimetype='application/json'
    )
    return response

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
