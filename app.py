from flask import render_template,request,session,flash,redirect,url_for
import sqlite3
from time import *
from functools import wraps
import os
from flask import Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/login', methods=['GET','POST'])
def login():
   error = None
   if request.method == 'POST':
    if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
    else:
            session['logged_in']=True 
            return redirect(url_for('home'))
	    flash('!You were just logged in!!')
   return render_template('login.html', error=error)
@app.route('/log')
def log():
   return render_template('login.html')

@app.route('/')
def home():
	return render_template('home.html')
@app.route('/post')
@login_required
def post():
	return render_template('post.html')

@app.route('/post',methods=['POST'])
@login_required
def post_store():
	conn=sqlite3.connect('database.db')
	c=conn.cursor()
	c.execute("INSERT INTO blogspot (author,post,day,time) VALUES (?,?,?,?)",[request.form['name'],request.form['blogpost'],strftime("%d %b %Y ", gmtime()),strftime("%H:%M:%S ", gmtime())])
	conn.commit()
	conn.close()
	return render_template('post.html')
@app.route('/main')
def main():
	conn=sqlite3.connect('database.db')
	c=conn.cursor()
	c.execute("SELECT * FROM blogspot ORDER BY id desc")
	posts=[dict(id=i[0],author=i[1],post=i[2],day=i[3],time=i[4],comment=i[5]) for i in c.fetchall()]	
	conn.commit()
	conn.close()
	if not posts:
		return render_template('main.html')
	else:
		return render_template('main.html',posts=posts)
		
@app.route('/main',methods=['POST'])
def comment_store():
	p=int(request.form['postid'])
	print p
	conn=sqlite3.connect('database.db')
	c=conn.cursor()
	c.execute("SELECT comment FROM blogspot WHERE id=(?)",[p])
	comments=[c.fetchall()]	

	if comments[0][0][0]==None:
		c.execute("UPDATE blogspot SET comment=(?) WHERE id=(?)",['\n'+request.form['guest']+ '  : \n'+request.form['comments']+'\n',p])
	else:
		c.execute("UPDATE blogspot SET comment=(?) WHERE id=(?)",['\n'+request.form['guest']+ '  : \n'+request.form['comments']+'\n'+comments[0][0][0]+'\n',p])

	c.execute("SELECT * FROM blogspot ORDER BY id desc")
	posts=[dict(id=i[0],author=i[1],post=i[2],day=i[3],time=i[4],comment=i[5]) for i in c.fetchall()]	
	conn.commit()
	conn.close()
	if not posts:
		return render_template('main.html')
	else:
		return render_template('main.html',posts=posts)
@app.route('/logout')
def logout():
 session.pop('logged_in',None)
 flash('!!You were just logged out')
 return redirect(url_for('home'))
 	

if __name__ == '__main__':
 app.run(debug=True)