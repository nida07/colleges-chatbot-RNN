from public import *
from database import *

staff=Blueprint('staff',__name__)

@staff.route('/staffhome')
def staffhome():
	return render_template("staffhome.html")

@staff.route('staffviewprofile',methods=['post','get'])
def staffviewprofile():
	data={}
	stid=session['sid']
	q="select * from staff where staff_id='%s'"%(stid)
	res=select(q)
	data['up']=res
	print(res)

	if "submit" in request.form:
		first_name=request.form['firstname']
		last_name=request.form['lastname']
		place=request.form['place']
		phone=request.form['phone']
		email=request.form['email']
		q="update staff set first_name='%s',last_name='%s',place='%s',phone='%s',email='%s' where staff_id='%s'"%(first_name,last_name,place,phone,email,session['sid'])
		update(q)
		return redirect(url_for("staff.staffviewprofile"))

	return render_template("staffviewprofile.html",data=data)

@staff.route('staffviewnotification')
def staffviewnotification():
	data={}
	q="select * from notification"
	res=select(q)
	data['noti']=res
	return render_template("staffviewnotification.html",data=data)

@staff.route('staffmanagestudent',methods=['get','post'])
def staffmanagestudent():
	data={}
	q="select * from course"
	res=select(q)
	data['crs']=res
	if 'submit' in request.form:
		course=request.form['course']
		semester=request.form['semester']
		firstname=request.form['firstname']
		lastname=request.form['lastname']
		place=request.form['place']
		email=request.form['email']
		username=request.form['username']
		password=request.form['password']
		q="insert into login values(null,'%s','%s','student')"%(username,password)
		id=insert(q)
		s="insert into student values(null,'%s','%s','%s','%s','%s','%s','%s')"%(id,course,semester,firstname,lastname,place,email)
		insert(s)	
	if 'action' in request.args:
		action=request.args['action']
		sid=request.args['sid']
		id=request.args['id']
	else:
		action=None

	if action=="delete":
		q="delete from login where login_id='%s'"%(id)
		delete(q)
		q="delete from student where login_id='%s'"%(id)
		delete(q)
		return redirect(url_for('staff.staffmanagestudent'))

	if action=="update":
		q="select * from student where student_id='%s'"%(sid)
		print(q)
		res=select(q)
		data['Edit']=res
	
	if 'update' in request.form:
		course=request.form['course']
		semester=request.form['semester']
		firstname=request.form['firstname']
		lastname=request.form['lastname']
		place=request.form['place']
		email=request.form['email']
		q="update student set course_id='%s',semester='%s',first_name='%s',last_name='%s',place='%s',email='%s' where student_id='%s'"%(course,semester,firstname,lastname,place,email,sid)
		update(q)
		print(q)
		return redirect(url_for('staff.staffmanagestudent'))

	q="select * from student inner join course using(course_id)"
	res=select(q)
	data['student']=res

	return render_template("staffmanagestudent.html",data=data)


@staff.route('staffaddattendance',methods=['get','post'])
def staffaddattendance():
	sid=request.args['sid']
	if 'submit' in request.form:
		status=request.form['status']
		q="insert into attendance values(null,'%s',now(),'%s')"%(sid,status)
		insert(q)
		return redirect(url_for('staff.staffmanagestudent'))
	return render_template("staffaddattendance.html")


@staff.route('staffaddtimetable',methods=['get','post'])
def staffaddtimetable():
	data={}
	# q="select * from course"
	# res=select(q)
	# data['course']=res
	
	cid=request.args['cid']
	if 'submit' in request.form:
		
		semester=request.form['semester']
		
		s="insert into timetable values(null,'%s','%s',curdate(),curtime())"%(cid,semester)
		insert(s)

	q="select * from timetable inner join course using(course_id) where course_id='%s'"%(cid)
	data['view']=select(q)
	return render_template("staffaddtimetable.html",data=data)
@staff.route('staff_view_course',methods=['get','post'])
def staff_view_course():
	data={}
	q="select * from course"
	res=select(q)
	data['course']=res
	return render_template("staff_view_course.html",data=data)
