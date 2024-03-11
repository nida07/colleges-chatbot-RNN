from flask import *
from database import *
import demjson
# from faqengine import *
import random

api=Blueprint('api',__name__)

# faqslist = ["D:\\New Chat\\Chatbot\\static\\data\\Greetings.csv"]
# faqmodel = FaqEngine(faqslist)

# def get_response(user_message):
#     return faqmodel.query(user_message)
def get_response(user_message):
    msg="%"+user_message+"%"
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",msg)
    q="select answer from basic where question like '%s'" %(msg)
    print(q)
    res=select(q)
    print(res,"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
    return res[0]['answer']

@api.route('/login')
def login():
	data={}
	username=request.args['username']
	password=request.args['password']
	q="SELECT * FROM `login` WHERE `username`='%s' AND `password`='%s'" %(username,password)
	print(q)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	return demjson.encode(data)

@api.route('/studentviewprofile')
def studentviewprofile():
	data={}
	lid=request.args['lid']
	q="select * from student inner join course using(course_id) where student_id=(select student_id from student where login_id='%s')" %(lid)
	print(q,"llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll")
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	return demjson.encode(data)

@api.route('/studentviewtimetable')
def studentviewtimetable():
	data={}
	logid=request.args['lid']
	q="SELECT * FROM timetable INNER JOIN course USING(course_id) WHERE course_id=(SELECT course_id FROM student WHERE login_id='%s')"%(logid)
	res=select(q)
	print("gggggggggggggg",res)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="studentviewtimetable"
	return demjson.encode(data)

@api.route('/student_view_notification')
def student_view_notification():
	data={}

	q="select * from notification"
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	return demjson.encode(data)



@api.route('/usermanagecomplaints')
def usermanagecomplaints():
	data={}
	complaint=request.args['complaint']
	lid=request.args['lid']
	q="insert into complaint values(null,'0',(select student_id from student where login_id='%s'),'%s','pending',curdate())" %(lid,complaint)
	insert(q)
	data['status']="success"
	data['method']="usermanagecomplaints"
	return demjson.encode(data)


@api.route('/userviewcomplaints')
def userviewcomplaints():
	data={}
	lid=request.args['lid']
	q="select * from complaint where student_id=(select student_id from student where login_id='%s')" %(lid)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="userviewcomplaints"
	return demjson.encode(data)


@api.route('/View_attendance')
def View_attendance():
	data={}
	lid=request.args['lid']
	q="select * from attendance where student_id=(select student_id from student where login_id='%s')" %(lid)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="View_attendance"
	return demjson.encode(data)



@api.route('/chat')
def chat():
	data={}
	response_text=""
	lid=request.args['sender_id']
	try:
		message = request.args['details']
		response_text = get_response(message)
		print("fffffffffffffffffffffffffffffffffffffffffffffffffff",response_text)
        # return jsonify({"status":"success","response":response_text})
	except Exception as e:
		print(e)
	q="insert into chat values(null,'%s','0','%s',curdate())" %(lid,message)
	insert(q)
	if response_text:
		q="insert into chat values(null,'0','%s','%s',curdate())" %(lid,response_text)
		insert(q)
		data['status']="success"
		data['data']=response_text
	else:
		h="insert into qusetion_request values(null,(select student_id from student where login_id='%s'),'%s','pending')"%(lid,message)
		insert(h)
		q="insert into chat values(null,'0','%s','%s',curdate())" %(lid,response_text)
		insert(q)
		data['status']="success"
		data['data']=response_text
	data['method']="chat"
	return demjson.encode(data)


@api.route('/chatdetail')
def chatdetail():
	data={}																																																																																																																																	
	lid=request.args['sender_id']
	q="select * from chat where (sender_id='%s' and receiver_id='0') or (sender_id='0' and receiver_id='%s')" %(lid,lid)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="chatdetail"
	return demjson.encode(data)