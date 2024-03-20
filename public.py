from flask import *
from database import *

public=Blueprint('public',__name__)

@public.route('/')
def home():
	return render_template('home.html')

@public.route('/login',methods=['get','post'])
def login():
	if 'login' in request.form:
		username=request.form['username']
		password=request.form['password']
		q="select * from login where username='%s' and password='%s'" %(username,password)
		res=select(q)
		print(q)
		print(res)
		if res:
			session['lid']=res[0]['login_id']
			logid=session['lid']
			usertype=res[0]['usertype']
			if usertype=="admin":
				flash("Login Succesfull!!")
				return redirect(url_for('admin.adminhome'))
			elif usertype=="staff":
				flash("Login Succesfull!!")
				q="select * from staff where login_id='%s'"%(logid)
				res=select(q)
				session['sid']=res[0]['staff_id']
				stid=session['sid']
				
				return redirect(url_for('staff.staffhome'))
			# elif usertype=="student":
				
			# 	q="select * from student where login_id='%s'"%(logid)
			# 	res=select(q)
			# 	if res:
					
			# 		session['student_id']=res[0]['student_id']
			# 		student_id=session['student_id']
			# 		flash("Login Succesfull!!")
			# 		return redirect(url_for('student.studenthome'))
			# elif usertype=="parent":
				
			# 	q="select * from parent where login_id='%s'"%(logid)
			# 	res=select(q)
			# 	print(q)
			# 	print(res)
			# 	if res:
					
			# 		session['parent_id']=res[0]['parent_id']
			# 		parent_id=session['parent_id']
			# 		flash("Login Succesfull!!")
			# 		return redirect(url_for('parent.parenthome'))
		else:
			flash("invalid username and password..!")

	return render_template('login.html')	


# @public.route('/parentreg',methods=['get','post'])
# def parentreg():
# 	data={}
# 	q="select * from student"
# 	res=select(q)
# 	data['student']=res 
# 	if 'register' in request.form:
# 		stud=request.form['stud']
# 		fname=request.form['firstname']
# 		lname=request.form['lastname']
# 		place=request.form['place']
# 		phone=request.form['phone']
# 		email=request.form['email']
# 		uname=request.form['uname']
# 		passw=request.form['passw']
# 		q="select * from login where username='%s'  "%(uname)
# 		res=select(q)
# 		if res:
# 			flash("Username  already exist!!")

# 			q="select * from student where student_id='%s'"%(stud)
# 			res=select(q)
# 			if res:
# 				flash("Already Added..!")
# 			else:
# 				q="insert into login values(null,'%s','%s','parent')"%(uname,passw)
# 				id=insert(q)
# 				print(q)
# 				q="insert into parent values(null,'%s','%s','%s','%s','%s','%s','%s')"%(id,stud,fname,lname,place,phone,email)
# 				insert(q)
# 				print(q)
# 				flash("registration successfull")
# 				return redirect(url_for('public.login'))

# 		else:
# 			return redirect(url_for('public.login'))
# 	return render_template('parent_register.html',data=data)