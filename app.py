from flask import Flask, render_template,request, redirect, url_for, g
import sqlite3

app = Flask(__name__)



def get_message_db():
    # write some helpful comments here
    try:
            return g.message_db
    except:
            g.message_db = sqlite3.connect("messages_db.sqlite")
            cursor = g.message_db.cursor()
            cmd = """
            CREATE TABLE IF NOT EXISTS messages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                handle TEXT NOT NULL,
                message TEXT NOT NULL
            );
            """
            cursor.execute(cmd)
            g.message_db.commit()
            return g.message_db
    
def insert_message(request):
    """
    Function handles inserting user mesasges to the 
    database of messages
    """
    # Create and connect to the message_db database
    # using our newly defined get_message_db() function
    db = get_message_db()
    # Extract message and handle from the request
    message = request.form['msg']
    handle = request.form['name']
    cmd = 'INSERT INTO messages (handle, message) VALUES (?, ?)'
    db.execute(cmd,(handle, message))
    db.commit()
    db.close()


def random_messages(n):
     db = get_message_db()
     cursor = g.message_db.cursor()
     cmd = 'SELECT handle, message FROM messages ORDER BY RANDOM() LIMIT ?'
     msgs = cursor.execute(cmd,(n,)).fetchall()
     db.close()
     return msgs

@app.route("/",  methods=['GET']) 
def index():
    return redirect(url_for('home'))

@app.route("/home/",  methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route("/submit/", methods=['POST', 'GET'])
def submit():
    if request.method == "GET":
        return render_template("submit.html")
    else: 
        insert_message(request)
        return render_template("submit.html", 
                               name=request.form['name'])

@app.route("/view/",  methods=['GET', 'POST'])
def view():
    if request.method == "GET":
        return render_template('view.html', 
                               messages = random_messages(1))
    else: 
        return render_template('view.html', 
                               messages = random_messages(int(request.form['n'])))

    
if __name__ == "__main__":
    app.run(port=8000, debug=True)