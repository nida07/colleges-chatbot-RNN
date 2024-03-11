
from public import *
from database import *
# from faqengine import *
import random

student=Blueprint('student',__name__)


# faqslist = ["D:\\Projects\\Chatbot\\static\\data\\Greetings.csv"]
# faqmodel = FaqEngine(faqslist)

def get_response(user_message):
    msg="%"+user_message+"%"
    q="select answer from basic where question like '%s'" %(msg)
    res=select(q)
    print(res)
    return res[0]['answer']

@student.route('/studenthome',methods=['get','post'])
def studenthome():
    data={}
    lid=session['lid']
    data['lid']=lid
    try:
        if 'send' in request.form:
            message = request.form['msg']
            response_text = get_response(message)
            print(response_text)
            q="insert into chat values(null,'%s','0','%s',curdate())" %(lid,message)
            insert(q)
            q="insert into chat values(null,'0','%s','%s',curdate())" %(lid,response_text)
            insert(q)
    # return jsonify({"status":"success","response":response_text})
    except Exception as e:
        print(e)
    print(lid)
    q="""(SELECT *,'link' AS link FROM chat WHERE (sender_id='%s' AND message LIKE 'http' ) OR (receiver_id='%s'  AND message LIKE 'http' )) UNION
(SELECT *,'noink' AS link FROM chat WHERE (sender_id='%s' AND message NOT LIKE 'http' ) OR (receiver_id='%s'  AND message NOT LIKE 'http' ))ORDER BY chat_id  
""" %(lid,lid,lid,lid)
    res=select(q)
    if res:
        data['msgs']=res

   
    return render_template("studenthome.html",data=data)

@student.route('/chatsession/',methods=['get','post'])
def chatsession():
    data={}
    lid=session['lid']
    data['lid']=lid
    try:
        
        message = request.form['message']
        response_text = get_response(message)
        print(response_text)
        q="insert into chat values(null,'%s','0','%s',curdate())" %(lid,message)
        insert(q)
        q="insert into chat values(null,'0','%s','%s',curdate())" %(lid,response_text)
        insert(q)
        # return jsonify({"status":"success","response":response_text})
    except Exception as e:
        print(e)
    q="select * from chat where (sender_id='%s' and receiver_id='0') or (sender_id='0' and receiver_id='%s') order by chat_id " %(lid,lid)
    res=select(q)
   
    ress=[]
    for i in res:
        try:
            print(i,"=============================")
            ress.append(str(i['sender_id']))
            ress.append(str(i['receiver_id']))
            ress.append(str(i['message']))
        except:
            pass
    ress=','.join(ress)
    resp = make_response(json.dumps(ress))

    # else:
    #     resp = make_response(jsonify(['naveen','nikhil']))
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@student.route('student_view_profile',methods=['post','get'])
def student_view_profile():
    data={}
    stid=session['student_id']
    q="select * from student inner join course using(course_id) where student_id='%s'"%(stid)
    res=select(q)
    data['up']=res
    print(res)

    if "submit" in request.form:
        first_name=request.form['firstname']
        last_name=request.form['lastname']
        place=request.form['place']
        course=request.form['course']
        sem=request.form['semester']
        email=request.form['email']
        q="update staff set first_name='%s',last_name='%s',place='%s',semester='%s',email='%s' where staff_id='%s'"%(first_name,last_name,place,sem,email,stid)
        update(q)
        return redirect(url_for("student.student_view_profile"))

    return render_template("student_view_profile.html",data=data)


@student.route('student_view_timetable',methods=['get','post'])
def student_view_timetable():
    data={}
   
    cid=request.args['cid']
    q="select * from timetable inner join course using(course_id) where course_id='%s'"%(cid)
    data['view']=select(q)
    

    return render_template("student_view_timetable.html",data=data)


@student.route('student_view_noti')
def student_view_noti():
    data={}
    q="select * from notification"
    res=select(q)
    data['noti']=res
    return render_template("student_view_noti.html",data=data)


@student.route('/student_chat',methods=['get','post'])
def student_chat():
    data={}
    lid=session['lid']
    data['lid']=lid
    try:
        if 'send' in request.form:
            message = request.form['msg']
            response_text = get_response(message)
            print(response_text)
            q="insert into chat values(null,'%s','0','%s',curdate())" %(lid,message)
            insert(q)
            q="insert into chat values(null,'0','%s','%s',curdate())" %(lid,response_text)
            insert(q)
            return jsonify({"status":"success","response":response_text})
    except Exception as e:
        print(e)
    print(lid)
    q="""(SELECT *,'link' AS link FROM chat WHERE (sender_id='%s' AND message LIKE 'http' ) OR (receiver_id='%s'  AND message LIKE 'http' )) UNION
(SELECT *,'noink' AS link FROM chat WHERE (sender_id='%s' AND message NOT LIKE 'http' ) OR (receiver_id='%s'  AND message NOT LIKE 'http' ))ORDER BY chat_id  
""" %(lid,lid,lid,lid)
    res=select(q)
    if res:
        data['msgs']=res

   
    return render_template("student_chat.html",data=data)

@student.route('student_send_complaint',methods=['get','post'])
def parent_send_complaints():
    data={}
    q="select * from complaint where student_id='%s'"%(session['student_id'])
    res=select(q)
    data['view']=res
    if 'submit' in request.form:
        com=request.form['com']
        q="insert into complaint values(null,0,'%s','%s','pending',curdate())"%(session['student_id'],com)
        insert(q)
    return render_template("student_send_complaint.html",data=data)

@student.route('student_view_course',methods=['get','post'])
def student_view_course():
    data={}
    q="select * from course"
    res=select(q)
    data['course']=res
    return render_template("student_view_course.html",data=data)

@student.route('student_view_attendance')
def student_view_attendance():
    data={}
    q="select * from attendance inner join student using(student_id) where student_id='%s'"%(session['student_id'])
    print(q)
    res=select(q)
    data['complaint']=res
    return render_template("student_view_attendance.html",data=data)