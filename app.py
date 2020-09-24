from flask import Flask, render_template, request, redirect,session,flash
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'register'

mysql= MySQL(app)
@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    msg=''
    if request.method == "POST" and 'username' in request.form and 'emailid' and 'password' in request.form:
        details = request.form
        username = details['username']
        emailid = details['emailid']
        password = details['password']
        conpassword = details['conpassword']
        cur = mysql.connection.cursor()
        b=cur.execute("SELECT * FROM sign WHERE username LIKE %s", (username,))
        c = cur.execute("SELECT * FROM sign WHERE emailid LIKE %s", (emailid,))
        if int(b)> 0 and int(c)<=0:
            msg='Username already exists!'
        elif int(c)>0 and int(b)<=0:
            msg='Email id already exists!'
        elif int(b)>0 and int(c)>0:
            msg="Both username and email id already exists!"
        else:
            cur.execute("INSERT INTO sign(username,emailid,password,conpassword) VALUES(%s, %s,%s,%s)", (username,emailid,password,conpassword))
            mysql.connection.commit()
            cur.close()
            msg='Signed up sucessfully..!!'
    return render_template('signup.html',msg=msg)
@app.route('/')
def star():
    return redirect('/login.html')


@app.route('/login.html', methods=['GET','POST'])
def login():
    error=None
    if request.method == 'POST' and 'name' in request.form and 'pass' in request.form:
        details=request.form
        username=details['name']
        password=details['pass']
        cursor = mysql.connection.cursor()
        a=cursor.execute('SELECT * FROM sign WHERE username = %s AND password = %s', (username, password))
        if int (a)>0:
            session['logged_in'] = True
            session['username'] = username
            session['password']=password
            return redirect('/home.html')
        else:
            error='Incorrect username/password!'
    return render_template('login.html', error=error)
@app.route('/home.html', methods=['POST','GET'])
def img():
    cur = mysql.connection.cursor()
    cur.execute("select * from blog")
    result = cur.fetchall()
    if request.method == "POST":
        details = request.form
        comments= details['cmnt']
        comment_date=details['date']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO comment(comments,comment_date) VALUES(%s,%s)",(comments,comment_date))
        cur.execute("select * from blog")
        res = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    return render_template('home.html', var=result)

@app.route('/profile.html', methods=['POST','GET'])
def profile():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM sign WHERE username = %s', (session['username'],))
    res=cur.fetchone()
    cur.execute('SELECT * FROM blog WHERE username = %s', (session['username'],))
    result = cur.fetchall()
    return render_template('profile.html',res=res,result=result)

@app.route('/logout.html')
def log():
    session.pop('logged_in',None)
    return redirect('/login.html')

@app.route('/blog.html',methods=['GET','POST'])
def blog():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM sign WHERE username = %s AND password=%s', (session['username'], session['password'],))
    result = cur.fetchone()
    if request.method == "POST":
        details = request.form
        title = details['title']
        image = details['image']
        content = details['content']
        username=details['username']
        date=details['date']
        emailid=details['emailid']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO blog(title,image,date,content,username,emailid) VALUES(%s, %s,%s,%s,%s,%s)",(title,image,date,content,username,emailid))
        mysql.connection.commit()
        cur.close()
    return render_template('blog.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
