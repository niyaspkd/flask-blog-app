from app import app
from flask import render_template,request
import sqlite3
from time import *
@app.route('/')
def home():
	return render_template('home.html')
@app.route('/post')
def post():
	return render_template('post.html')
@app.route('/post',methods=['POST'])
def post_store():
	conn=psycopg2.connect('/home/nidhin/Documents/Networking/flask/microblog/database.db',user='nidhin')
	c=conn.cursor()
	c.execute("INSERT INTO blogspot (author,post,day,time) VALUES (%s,%s,%s,%s)",[request.form['name'],request.form['blogpost'],strftime("%d %b %Y ", gmtime()),strftime("%H:%M:%S ", gmtime())])
	conn.commit()
	conn.close()
	return render_template('post.html')
@app.route('/main')
def main():
#	conn=sqlite3.connect('/home/nidhin/Documents/Networking/flask/microblog/database.db')
#	c=conn.cursor()
#	c.execute("SELECT * FROM blogspot ORDER BY id desc")
#	posts=[dict(id=i[0],author=i[1],post=i[2],day=i[3],time=i[4],comment=i[5]) for i in c.fetchall()]	
#	conn.commit()
#	conn.close()
#	if not posts:
#		return render_template('main.html')
#	else:
#		return render_template('main.html',posts=posts)
	return render_template('main.html')
		
@app.route('/main',methods=['POST'])
def comment_store():
	p=int(request.form['postid'])
	print p
	conn=sqlite3.connect('/home/nidhin/Documents/Networking/flask/microblog/database.db')
	c=conn.cursor()
	c.execute("SELECT comment FROM blogspot WHERE id=(?)",[p])
	comments=[c.fetchall()]	
#	conn.commit()
#	conn.close()
#	print comments[0][0][0]
#	conn=sqlite3.connect('/home/nidhin/Documents/Networking/flask/microblog/database.db')
#	c=conn.cursor()
	if comments[0][0][0]==None:
		c.execute("UPDATE blogspot SET comment=(?) WHERE id=(?)",['\n@'+request.form['guest']+ '  says: \n'+request.form['comments']+'\n',p])
	else:
		c.execute("UPDATE blogspot SET comment=(?) WHERE id=(?)",['\n@'+request.form['guest']+ '  says: \n'+request.form['comments']+'\n'+comments[0][0][0]+'\n',p])
#	conn.commit()
#	conn.close()
#	conn=sqlite3.connect('/home/nidhin/Documents/Networking/flask/microblog/database.db')
#	c=conn.cursor()
	c.execute("SELECT * FROM blogspot ORDER BY id desc")
	posts=[dict(id=i[0],author=i[1],post=i[2],day=i[3],time=i[4],comment=i[5]) for i in c.fetchall()]	
	conn.commit()
	conn.close()
	if not posts:
		return render_template('main.html')
	else:
		return render_template('main.html',posts=posts)
 	
