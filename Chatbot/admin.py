from flask import *
from database import*

admin=Blueprint('admin',__name__)

@admin.route('/adminhome')
def adminhome():
	return render_template('adminhome.html')

@admin.route('/admin_manage_course',methods=['get','post'])
def admin_manage_course():
	if 'submit' in request.form:
		course_name=request.form['course_name']
		q="insert into course values(null,'%s')"%(course_name)
		insert(q)
	data={}
	q="select * from course"
	res=select(q)
	data['course']=res
	if 'action' in request.args:
		action=request.args['action']
		cid=request.args['cid']
	else:
		action=None
	if action=="update":
		q="select * from course where course_id='%s'"%(cid)
		res=select(q)
		data['update_course']=res
	if 'update' in request.form:
		course=request.form['course']
		q="update course set course='%s' where course_id='%s'"%(course,cid)
		update(q)
		return redirect(url_for('admin.admin_manage_course'))	
	if action=="delete":
		cid=request.args['cid']
		q="delete from course where course_id='%s'"%(cid)
		delete(q)
		return redirect(url_for('admin.admin_manage_course'))
	return render_template('admin_manage_course.html',data=data)	

@admin.route('/admin_manage_staff',methods=['get','post'])
def admin_manage_staff():
	if 'submit' in request.form:
		first_name=request.form['firstname']
		last_name=request.form['lastname']
		place=request.form['place']
		phone=request.form['phone']
		email=request.form['email']
		username=request.form['uname']
		password=request.form['password']
		q="insert into login values(null,'%s','%s','staff')" %(username,password)
		id=insert(q)
		q="insert into staff values(null,'%s','%s','%s','%s','%s','%s')" %(id,first_name,last_name,place,phone,email)
		insert(q)

	data={}
	q="select * from staff"
	res=select(q)
	data['staff']=res
	print(res)

	if 'action' in request.args:
		action=request.args['action']
		sid=request.args['sid']
	else:
		action=None
	if action=="update":
		q="select * from staff where staff_id='%s'"%(sid)
		print(q)
		res=select(q)
		data['Edit']=res
	
	if action=="delete":
		sid=request.args['sid']
		q="delete from staff where staff_id='%s'"%(sid)
		delete(q)
		return redirect(url_for('admin.admin_manage_staff'))

	if 'update' in request.form:
		firstname=request.form['firstname']
		lastname=request.form['lastname']
		place=request.form['place']
		phone=request.form['phone']
		email=request.form['email']
		q1="update staff set first_name='%s',last_name='%s',place='%s',phone='%s',email='%s' where staff_id='%s'"%(firstname,lastname,place,phone,email,sid)
		update(q1)
		return redirect(url_for('admin.admin_manage_staff'))
	return render_template('admin_manage_staff.html',data=data)

@admin.route('admin_sent_notification',methods=['get','post'])
def admin_sent_notification():
	if 'submit' in request.form:
		notification=request.form['notification']
		q="insert into notification values(null,'%s',now())"%(notification)
		insert(q)

	return render_template("admin_sent_notification.html")

@admin.route('adminviewcomplaint',methods=['get','post'])
def adminviewcomplaint():
	
	data={}
	q="select * from complaint"
	res=select(q)
	data['complaint']=res
	print(res)

	
	return render_template("adminviewcomplaint.html",data=data)

@admin.route('adminreply',methods=['get','post'])
def adminreply():
	cid=request.args['cid']
	if 'submit' in request.form:
		reply=request.form['reply']
		q="update complaint set reply='%s' where complaint_id='%s'"%(reply,cid)
		update(q)
		return redirect(url_for('admin.adminviewcomplaint',cid=cid))
	return render_template("adminreply.html")

@admin.route('adminchat',methods=['get','post'])
def adminchat():
	
	
	return render_template("adminchat.html")


@admin.route('/admin_view_chat')
def admin_view_chat():
	data={}
	ddf="SELECT * FROM `student`INNER JOIN `course`USING(`course_id`)"
	data['view']=select(ddf)
	if 'action' in request.args:
		action=request.args['action']
		lid=request.args['lid']
	else:
		action=None
	if action=='chat':
		dd="SELECT * FROM `chat`WHERE `sender_id`='%s' AND `receiver_id`='0'  OR (`sender_id`='0' AND `receiver_id`='%s' )"%(lid,lid)
		data['c_view']=select(dd)
	return render_template('admin_view_chat.html',data=data)


@admin.route('/admin_view_request_question')
def admin_view_request_question():
	data={}
	h="select * from qusetion_request"
	data['view']=select(h)
	return render_template('admin_view_request_question.html',data=data)

@admin.route('/admin_add_ans',methods=['get','post'])
def admin_add_ans():
	qus=request.args['qus']
	req=request.args['req']
	if 'add' in request.form:
		ans=request.form['ans']
		gg="insert into basic values(null,'%s','%s')"%(qus,ans)
		insert(gg)
		n="update qusetion_request set status='sended' where question_request_id='%s'"%(req)
		update(n)
		return redirect(url_for('admin.admin_view_request_question'))
	return render_template('admin_add_ans.html')