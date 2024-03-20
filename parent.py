
# module on working


from public import *
from database import *
# from faqengine import *
import random

parent=Blueprint('parent',__name__)


# faqslist = ["C:\\Users\\noel\\Desktop\\New folder\\Chatbot\\static\\data\\Greetings.csv"]
# faqmodel = FaqEngine(faqslist)

def get_response(user_message):
    msg="%"+user_message+"%"
    q="select answer from basic where question like '%s'" %(msg)
    res=select(q)
    print(res)
    return res[0]['answer']

@parent.route('/parenthome',methods=['get','post'])
def parenthome():
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

   
    return render_template("parent_home.html",data=data)


@parent.route('/chatsession/',methods=['get','post'])
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
@parent.route('parent_view_student_profile',methods=['post','get'])
def parent_view_student_profile():
    data={}
    
    q="select * from student inner join parent using(student_id) where parent_id='%s'"%(session['parent_id'])
    res=select(q)
    data['up']=res
    return render_template("parent_view_student_profile.html",data=data)

@parent.route('parent_send_complaints',methods=['get','post'])
def parent_send_complaints():
    data={}
    q="select * from complaint where parent_id='%s'"%(session['parent_id'])
    res=select(q)
    data['view']=res
    if 'submit' in request.form:
        com=request.form['com']
        q="insert into complaint values(null,'%s',(select student_id from parent where parent_id='%s'),'%s','pending',curdate())"%(session['parent_id'],session['parent_id'],com)
        insert(q)
    return render_template("parent_send_complaints.html",data=data)

@parent.route('parent_view_notification')
def parent_view_notification():
    data={}
    q="select * from notification"
    res=select(q)
    data['noti']=res
    return render_template("parent_view_notification.html",data=data)


@parent.route('parent_view_attendance')
def parent_view_attendance():
    data={}
    q="select * from attendance inner join student using(student_id) inner join parent using(student_id) where parent_id='%s'"%(session['parent_id'])
    res=select(q)
    data['complaint']=res
    return render_template("parent_view_attendance.html",data=data)

@parent.route('/parent_chat',methods=['get','post'])
def parent_chat():
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

   
    return render_template("parent_chat.html",data=data)