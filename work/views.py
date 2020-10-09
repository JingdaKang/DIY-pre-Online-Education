import datetime
import os
import time
import pytz
import math
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from django.contrib.auth import authenticate, login
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from backend.models import User, Course, User_Course, Work, User_Work, Simple, Multiple, Blank, Judge, Subjective, \
    Work_Question, User_Question, SharedArea, Share_File, Work_Message, GoodWork
import json
from django.db import connection

# Create your views here.

def GetIdByUsername(username):
    cursor = connection.cursor()
    cursor.execute("select id from public.user where username=%s;",
    (username,))
    Id = cursor.fetchone()[0]
    cursor.close()
    return Id

# @deprecated
def UploadAvatar(request):#上传头像
    if request.method == "POST":
        if request.GET.get("select") is not None:
            picture = request.FILES.get("file")
            baseUrl = "Avatar"
            image_name = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + picture.name
            f = open(os.path.join(baseUrl,image_name),'wb+')
            for i in picture.chunks():
                f.write(i)
            f.close()
            url = '/Avatar/'+image_name
            return JsonResponse({"url":url})
        if request.GET.get("f") is not None:
            data = json.loads(request.body)
            username = data.get("username")
            imageurl = data.get("imageurl")
            print(username)
            print(imageurl)
            User.objects.filter(username=username).update(user_avatar=imageurl)

            return JsonResponse({"msg":1})
# @deprecated
def GetMyAvatar(request):#获得我的头像
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        AvatarUrl = list(User.objects.filter(username=username).values_list("user_avatar"))
        return JsonResponse({"AvatarUrl":AvatarUrl})

def GetCourse(request):#传所有课程
    cursor = connection.cursor()
    if request.method == "GET":
        try:
            cursor.execute("select course.id,name,number,maxnum,tid,status,stime\
                        ,time,public.user.username from public.course left join \
                        public.user on course.tid=public.user.id order by course.id;")
            rs = cursor.fetchall()
            return JsonResponse({"courses": rs}) 
        except Exception as e:
            print(e)
        finally:
            cursor.close()

        return JsonResponse({"courses": None})

def GetMyCourse(request):#查询我的课程
    if request.method == "POST":
        cursor = connection.cursor()
        data = json.loads(request.body)
        username = data.get("user")
        try:
            cursor.execute("select course.id,name,number,maxnum,tid,status,stime\
                        ,time,public.user.username from ((public.user_course left join public.course on \
                            user_course.cid=course.id) left join public.user on course.tid=public.user.id) \
                                where user_course.sname=%s order by id;",(username,))
            rs = cursor.fetchall()
            return JsonResponse({"mes": rs}) 
        except Exception as e:
            print(e)
        finally:
            cursor.close()

        return JsonResponse({"mes": None})


def GetTeacherCourse(request):#教师查看课程
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("user")
        cursor = connection.cursor()
        try:
            cursor.execute("select course.id,name,number,maxnum,tid,stime\
                        ,time,status,public.user.username from public.course left join \
                        public.user on course.tid=public.user.id where \
                            public.user.username=%s order by course.id;",(username,))
            rs = cursor.fetchall()
            return JsonResponse({"mes": rs}) 
        except Exception as e:
            print(e)
        finally:
            cursor.close()

def EditWork(request):#创建作业 （未完成）
    if request.method == "POST":
        data = json.loads(request.body)
        wid = data.get("wid")
        cursor = connection.cursor()
        try:
            if request.GET.get("select") is not None:
                cursor.execute("delete from work where id=%s;",(wid,))
                cursor.execute("delete from user_work where wid=%s;",(wid,))
            if request.GET.get("change") is not None:
                deadline = data.get("deadline")
                print(deadline)
                cursor.execute("update work set deadline=%s where id=%s",(deadline,wid))
            if request.GET.get("c") is not None:
                cursor.execute("update work set release='t' where id=%s",(wid,))
            return JsonResponse({'msg' : 1})
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        return JsonResponse({"msg": 0})

def GetWorkTime(request):#获得作业信息
    if request.method == "POST":
        data = json.loads(request.body)
        courseid = data.get("courseid")
        username = data.get("username")
        cursor = connection.cursor()
        try:
            cursor.execute("select id from public.user where username=%s;",(username,))
            sid = cursor.fetchone()[0]
            cursor.execute("select wid,finish,ctime,deadline from user_work,work where \
                work.id=user_work.wid and work.cid=%s and work.release='t' and user_work.sid=%s \
                     order by wid;",(courseid,sid))
            finishlist = cursor.fetchall()
            return JsonResponse({"finishlist":finishlist})
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        return JsonResponse({"finishlist":[]})


def GetMyWork(request):#查询我的作业
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        cursor = connection.cursor()
        try:
            cursor.execute("select id from public.user where username=%s;",(username,))
            sid = cursor.fetchone()[0]
            cursor.execute("select course.name,username,ctime,chapter,update,user_work.score,\
                finish,ifscore,wid,file from course,public.user,work,user_work where sid=%s \
                    and wid=work.id and work.cid=course.id and public.user.id=course.tid;",(sid,))
            workList = cursor.fetchall()
            return JsonResponse({"worklist":workList})
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        return JsonResponse({"worklist":[]})

def GetTeacherWork(request):#教师查询作业
    if request.method == "POST":
        data = json.loads(request.body)
        courseid = data.get("courseid")
        cursor = connection.cursor()
        try:
            if request.GET.get("select") is not None:
                cursor.execute("select count(*) from work where cid=%s;",(courseid,))
                ctime = cursor.fetchone()[0] + 1
                cursor.execute("insert into work(cid,ctime,chapter,deadline,release,finishnum,qnum) \
                    values (%s,%s,%s,now(),'f',0,0);",(courseid,ctime,ctime))
                cursor.execute("select id from work where cid=%s and ctime=%s;",(courseid,ctime))
                wid = cursor.fetchone()[0]
                cursor.execute("select public.user.id from public.user, user_course \
                    where sname=username and cid=%s;",(courseid,))
                sidlist = cursor.fetchall()
                for sidt in sidlist:
                    cursor.execute("insert into user_work(wid,sid,update,score,good,finish,ifscore) \
                        values (%s,%s,now(),0,'f','f','f');",(wid,sidt[0]))
            cursor.execute("select ctime,chapter,deadline,release,finishnum,id from work where cid=%s;",
                            (courseid,))
            worklist = []
            worklist.append(cursor.fetchall())
        except Exception as e:
            print(e)
            return JsonResponse({"worklist":[]})
        finally:
            cursor.close()
        return JsonResponse({"worklist":worklist})
        

def CreateQuestion(request):#创建题目
    if request.method == "POST":
        cursor = connection.cursor()
        if request.GET.get("picture1") is not None:
            picture = request.FILES.get("file")
            print(picture)
            baseUrl = "Question"
            image_name = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + picture.name
            f = open(os.path.join(baseUrl,image_name),'wb+')
            for i in picture.chunks():
                f.write(i)
            f.close()
            #url = 'http://127.0.0.1:8000/Question/'+image_name
            url = 'Question/'+image_name
            return JsonResponse({"url":url})
        if request.GET.get("picture2") is not None:
            picture = request.FILES.get("file")
            print(picture)
            baseUrl = "Question"
            image_name = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + picture.name
            f = open(os.path.join(baseUrl,image_name),'wb+')
            for i in picture.chunks():
                f.write(i)
            f.close()
            url = 'Question/'+image_name
            return JsonResponse({"url":url})
        if request.GET.get("picture3") is not None:
            picture = request.FILES.get("file")
            print(picture)
            baseUrl = "Question"
            image_name = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + picture.name
            f = open(os.path.join(baseUrl,image_name),'wb+')
            for i in picture.chunks():
                f.write(i)
            f.close()
            url = 'Question/'+image_name
            return JsonResponse({"url":url})
        if request.GET.get("picture4") is not None:
            picture = request.FILES.get("file")
            print(picture)
            baseUrl = "Question"
            image_name = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + picture.name
            f = open(os.path.join(baseUrl,image_name),'wb+')
            for i in picture.chunks():
                f.write(i)
            f.close()
            url = 'Question/'+image_name
            return JsonResponse({"url":url})
        if request.GET.get("picture5") is not None:
            picture = request.FILES.get("file")
            print(picture)
            baseUrl = "Question"
            image_name = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + picture.name
            f = open(os.path.join(baseUrl,image_name),'wb+')
            for i in picture.chunks():
                f.write(i)
            f.close()
            url = 'Question/'+image_name
            return JsonResponse({"url":url})
        if request.GET.get("question1") is not None:
            data = json.loads(request.body)
            wid = data.get("wid")
            content = data.get("content")
            chioce1 = data.get("chioce1")
            chioce2 = data.get("chioce2")
            chioce3 = data.get("chioce3")
            chioce4 = data.get("chioce4")
            answer = data.get("answer")
            explain = data.get("explain")
            imageUrl = data.get("questionimageUrl")
            if not all([content,chioce1,chioce2,chioce3,chioce4,answer]):
                return JsonResponse({"code":0, "msg":'信息不完整！'})
            else:
                cursor.execute("insert into simple(wid,content,choice1,choice2,choice3,choice4,answer,picture,explain) values \
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s);",(wid,content,chioce1,chioce2,chioce3,chioce4,answer,imageUrl,explain))
                #Simple.objects.create(wid=wid,content=content,choice1=chioce1,choice2=chioce2,choice3=chioce3,choice4=chioce4,answer=answer,picture=imageUrl,explain=explain)
                cursor.execute("select id from simple where wid=%s and content=%s;",(wid,content))
                qid = cursor.fetchone()[0]
                #qid = "".join('%s' %id for id in list(Simple.objects.filter(wid=wid,content=content).values_list("id")))
                cursor.execute("select qnum from work where id=%s;",(wid,))
                qnum = cursor.fetchone()[0]
                # qnum = int("".join('%s' %id for id in list(Work.objects.filter(id=wid).values_list("qnum"))))
                cursor.execute("update work set qnum=qnum+1 where id=%s;",(wid,))
                #Work.objects.filter(id=wid).update(qnum=qnum+1)
                cursor.execute("insert into work_question(wid,qid,number,type) values \
                    (%s,%s,%s,'1');",(wid,qid,qnum+1))
                #Work_Question.objects.create(wid=wid,qid=qid,number=qnum+1,type='1')
                return JsonResponse({"code":1, "msg":'提交此题成功！'})
        if request.GET.get("question2") is not None:
            data = json.loads(request.body)
            wid = data.get("wid")
            content = data.get("content")
            chioce1 = data.get("chioce1")
            chioce2 = data.get("chioce2")
            chioce3 = data.get("chioce3")
            chioce4 = data.get("chioce4")
            answer = data.get("answer")
            explain = data.get("explain")
            Answer = ''.join(answer)
            imageUrl = data.get("questionimageUrl")
            if not all([content,chioce1,chioce2,chioce3,chioce4,answer]):
                return JsonResponse({"code":0, "msg":'信息不完整！'})
            else:
                cursor.execute("insert into mutiple(wid,content,choice1,choice2,choice3,choice4,answer,picture,explain) values \
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s);",(wid,content,chioce1,chioce2,chioce3,chioce4,Answer,imageUrl,explain))
                cursor.execute("select id from mutiple where wid=%s and content=%s;",(wid,content))
                qid = cursor.fetchone()[0]
                cursor.execute("select qnum from work where id=%s;",(wid,))
                qnum = cursor.fetchone()[0]
                cursor.execute("update work set qnum=qnum+1 where id=%s;",(wid,))
                cursor.execute("insert into work_question(wid,qid,number,type) values \
                    (%s,%s,%s,'2');",(wid,qid,qnum+1))
                return JsonResponse({"code":1, "msg":'提交此题成功！'})
                '''Multiple.objects.create(wid=wid,content=content,choice1=chioce1,choice2=chioce2,choice3=chioce3,choice4=chioce4,answer=Answer,picture=imageUrl,explain=explain)
                qid = "".join('%s' %id for id in list(Multiple.objects.filter(wid=wid,content=content).values_list("id")))
                qnum = int("".join('%s' %id for id in list(Work.objects.filter(id=wid).values_list("qnum"))))
                Work.objects.filter(id=wid).update(qnum=qnum+1)
                Work_Question.objects.create(wid=wid,qid=qid,number=qnum+1,type='2')
                return JsonResponse({"code":1, "msg":'提交此题成功！'})'''
        if request.GET.get("question3") is not None:
            data = json.loads(request.body)
            wid = data.get("wid")
            content = data.get("content")
            answer = data.get("answer")
            explain = data.get("explain")
            imageUrl = data.get("questionimageUrl")
            if not all([content]):
                return JsonResponse({"code":0, "msg":'信息不完整！'})
            else:
                #Blank.objects.create(wid= wid,content=content,answer=answer,picture=imageUrl,explain=explain)
                cursor.execute("insert into blank(wid,content,answer,picture,explain) \
                    values (%s,%s,%s,%s,%s);",(wid,content,answer,imageUrl,explain))
                cursor.execute("select id from blank where wid=%s and content=%s;",(wid,content))
                qid = cursor.fetchone()[0]
                cursor.execute("select qnum from work where id=%s;",(wid,))
                qnum = cursor.fetchone()[0]
                cursor.execute("update work set qnum=qnum+1 where id=%s;",(wid,))
                cursor.execute("insert into work_question(wid,qid,number,type) values \
                    (%s,%s,%s,'4');",(wid,qid,qnum+1))
                return JsonResponse({"code":1, "msg":'提交此题成功！'})
                '''qid = "".join('%s' %id for id in list(Blank.objects.filter(wid=wid,content=content).values_list("id")))
                qnum = int("".join('%s' %id for id in list(Work.objects.filter(id=wid).values_list("qnum"))))
                Work.objects.filter(id=wid).update(qnum=qnum+1)
                Work_Question.objects.create(wid=wid,qid=qid,number=qnum+1,type='4')
                return JsonResponse({"code":1, "msg":'提交此题成功！'})'''
        if request.GET.get("question4") is not None:
            data = json.loads(request.body)
            wid = data.get("wid")
            content = data.get("content")
            judge = data.get("answer")
            explain = data.get("explain")
            print(judge)
            if judge=='正确':
                answer = True
            else:
                answer = False
            imageUrl = data.get("questionimageUrl")
            if not all([content,judge]):
                return JsonResponse({"code":0, "msg":'信息不完整！'})
            else:
                cursor.execute("insert into judge(wid,content,answer,picture,explain) \
                    values (%s,%s,%s,%s,%s);",(wid,content,answer,imageUrl,explain))
                cursor.execute("select id from judge where wid=%s and content=%s;",(wid,content))
                qid = cursor.fetchone()[0]
                cursor.execute("select qnum from work where id=%s;",(wid,))
                qnum = cursor.fetchone()[0]
                cursor.execute("update work set qnum=qnum+1 where id=%s;",(wid,))
                cursor.execute("insert into work_question(wid,qid,number,type) values \
                    (%s,%s,%s,'3');",(wid,qid,qnum+1))
                return JsonResponse({"code":1, "msg":'提交此题成功！'})
                '''Judge.objects.create(wid= wid,content=content,answer=answer,picture=imageUrl,explain=explain)
                qid = "".join('%s' %id for id in list(Judge.objects.filter(wid=wid,content=content).values_list("id")))
                qnum = int("".join('%s' %id for id in list(Work.objects.filter(id=wid).values_list("qnum"))))
                Work.objects.filter(id=wid).update(qnum=qnum+1)
                Work_Question.objects.create(wid=wid,qid=qid,number=qnum+1,type='3')
                return JsonResponse({"code":1, "msg":'提交此题成功！'})'''
        if request.GET.get("question5") is not None:
            data = json.loads(request.body)
            wid = data.get("wid")
            content = data.get("content")
            answer = data.get("answer")
            explain = data.get("explain")
            imageUrl = data.get("questionimageUrl")
            if not all([content]):
                return JsonResponse({"code":0, "msg":'信息不完整！'})
            else:
                cursor.execute("insert into subjective(wid,content,answer,picture,explain) \
                    values (%s,%s,%s,%s,%s);",(wid,content,answer,imageUrl,explain))
                cursor.execute("select id from subjective where wid=%s and content=%s;",(wid,content))
                qid = cursor.fetchone()[0]
                cursor.execute("select qnum from work where id=%s;",(wid,))
                qnum = cursor.fetchone()[0]
                cursor.execute("update work set qnum=qnum+1 where id=%s;",(wid,))
                cursor.execute("insert into work_question(wid,qid,number,type) values \
                    (%s,%s,%s,'5');",(wid,qid,qnum+1))
                return JsonResponse({"code":1, "msg":'提交此题成功！'})
                '''Subjective.objects.create(wid= wid,content=content,answer=answer,picture=imageUrl,explain=explain)
                qid = "".join('%s' %id for id in list(Subjective.objects.filter(wid=wid,content=content).values_list("id")))
                qnum = int("".join('%s' %id for id in list(Work.objects.filter(id=wid).values_list("qnum"))))
                Work.objects.filter(id=wid).update(qnum=qnum+1)
                Work_Question.objects.create(wid=wid,qid=qid,number=qnum+1,type='5')
                return JsonResponse({"code":1, "msg":'提交此题成功！'})'''

def Comment(request):#查询和评分学生作业
    if request.method == "POST":
        data = json.loads(request.body)
        cursor = connection.cursor()
        try:
            if request.GET.get("select") is not None:
                wid = data.get("wid")
                cursor.execute("select public.user.id,username from public.user,user_work where wid=%s and finish='f' \
                    and sid=public.user.id;",(wid,))
                Studentlist = cursor.fetchall()
                '''studentlist = cursor.fetchall()
                sidlist = list(User_Work.objects.filter(wid=wid,finish=False).values_list("sid"))
                Studentlist = []
                for Sid in sidlist:
                    sid = "".join('%s' %id for id in Sid)
                    studentlist = list(User.objects.filter(id=sid).values_list("id","username"))
                    Studentlist.append(studentlist)'''
                return JsonResponse({"studentlist":Studentlist})

            if request.GET.get("finish") is not None:
                wid = data.get("wid")
                cursor.execute("select public.user.id,username,update,ifscore,file from public.user,user_work \
                    where wid=%s and finish='t' and sid=public.user.id;",(wid,))
                Studentlist = cursor.fetchall()
                '''sidlist = list(User_Work.objects.filter(wid=wid,finish=True).values_list("sid"))
                Studentlist = []
                for Sid in sidlist:
                    sid = "".join('%s' %id for id in Sid)
                    studentlist = list(User.objects.filter(id=sid).values_list("id","username"))
                    update = list(User_Work.objects.filter(sid=sid,wid=wid).values_list("update","ifscore"))
                    file = list(User_Work.objects.filter(sid=sid,wid=wid).values_list("file"))
                    Studentlist.append(studentlist)
                    Studentlist.append(update)
                    Studentlist.append(file)'''
                return JsonResponse({"studentlist":Studentlist})
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        return JsonResponse({"msg":1})

def GetQuestionNumber(request):#获得题目数
    if request.method == "POST":
        data = json.loads(request.body)
        wid = data.get("wid")
        #qnum = list(Work.objects.filter(id=wid).values_list("qnum"))
        cursor = connection.cursor()
        cursor.execute("select qnum from work where id=%s;",(wid,))
        qnum = cursor.fetchone()[0]
        cursor.close()
        return JsonResponse({"qnum":qnum})

def GetQuestion(request):#获得题目
    if request.method == "POST":
        data = json.loads(request.body)
        wid = data.get("wid")
        number = data.get("number")
        username = data.get("username")
        cursor = connection.cursor()
        cursor.execute("select id from public.user where username=%s;",(username,))
        sid = cursor.fetchone()[0]
        cursor.execute("select qid,type from work_question where \
            wid=%s and number=%s;",(wid,number))
        Qid, Type = cursor.fetchone()
        '''sid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
        qid = list(Work_Question.objects.filter(wid=wid,number=number).values_list("qid"))
        Qid = "".join('%s' %id for id in qid)
        type = list(Work_Question.objects.filter(wid=wid,number=number).values_list("type"))
        Type = "".join('%s' %id for id in type)'''
        print(Qid)
        print(Type)
        cursor.execute("select count(*) from user_question where \
                sid=%s and wid=%s and qid=%s and number=%s and type=%s;",
                (sid,wid,Qid,number,Type))
        if cursor.fetchone()[0] == 0:
            cursor.execute("insert into user_question(sid,wid,qid,number,type,ischeck,\
                judge,cloud,is_read) values (%s,%s,%s,%s,%s,'f','f','f','f');",
                (sid,wid,Qid,number,Type))
        if Type=='1':
            '''if len(list(User_Question.objects.filter(sid=sid,wid=wid,qid=Qid,number=number,type=Type).values_list()))==0:
                User_Question.objects.create(
                    sid=sid,
                    wid=wid,
                    qid=Qid,
                    number=number,
                    type=Type
                )'''
            cursor.execute("select content,choice1,choice2,choice3,choice4,picture from simple\
                where wid=%s and id=%s;",(wid,Qid))
            content,choice1,choice2,choice3,choice4,picture = cursor.fetchone()
            '''content = list(Simple.objects.filter(wid=wid,id=Qid).values_list("content"))
            choice1 = list(Simple.objects.filter(wid=wid,id=Qid).values_list("choice1"))
            choice2 = list(Simple.objects.filter(wid=wid,id=Qid).values_list("choice2"))
            choice3 = list(Simple.objects.filter(wid=wid,id=Qid).values_list("choice3"))
            choice4 = list(Simple.objects.filter(wid=wid,id=Qid).values_list("choice4"))
            picture = list(Simple.objects.filter(wid=wid,id=Qid).values_list("picture"))'''

            return JsonResponse({
                "type":Type,
                "content":content,
                "choice1":choice1,
                "choice2":choice2,
                "choice3":choice3,
                "choice4":choice4,
                "picture":picture
            })
        elif Type=='2':
            cursor.execute("select content,choice1,choice2,choice3,choice4,picture from mutiple\
                where wid=%s and id=%s;",(wid,Qid))
            content,choice1,choice2,choice3,choice4,picture = cursor.fetchone()
            '''content = list(Multiple.objects.filter(wid=wid,id=Qid).values_list("content"))
            choice1 = list(Multiple.objects.filter(wid=wid,id=Qid).values_list("choice1"))
            choice2 = list(Multiple.objects.filter(wid=wid,id=Qid).values_list("choice2"))
            choice3 = list(Multiple.objects.filter(wid=wid,id=Qid).values_list("choice3"))
            choice4 = list(Multiple.objects.filter(wid=wid,id=Qid).values_list("choice4"))
            picture = list(Multiple.objects.filter(wid=wid,id=Qid).values_list("picture"))
            '''
            return JsonResponse({
                "type":Type,
                "content":content,
                "choice1":choice1,
                "choice2":choice2,
                "choice3":choice3,
                "choice4":choice4,
                "picture":picture
            })
        elif Type=='3':
            cursor.execute("select content,picture from judge\
                where wid=%s and id=%s;",(wid,Qid))
            content,picture = cursor.fetchone()
            '''content = list(Judge.objects.filter(wid=wid,id=Qid).values_list("content"))
            picture = list(Judge.objects.filter(wid=wid,id=Qid).values_list("picture"))
            '''
            return JsonResponse({
                "type":Type,
                "content":content,
                "picture":picture
            })
        elif Type=='4':
            cursor.execute("select content,picture from blank\
                where wid=%s and id=%s;",(wid,Qid))
            content,picture = cursor.fetchone()            
            return JsonResponse({
                "type":Type,
                "content":content,
                "picture":picture
            })
        elif Type=='5':
            cursor.execute("select content,picture from subjective\
                where wid=%s and id=%s;",(wid,Qid))
            content,picture = cursor.fetchone()
            return JsonResponse({
                "type":Type,
                "content":content,
                "picture":picture
            })

def UpdateAnswer(request):#上传答案
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        wid = data.get("wid")
        number = data.get("number")
        answer = data.get("answer")
        answerList = "".join('%s' %id for id in data.get("answerList"))
        cursor = connection.cursor()
        cursor.execute("select id from public.user where username=%s;",(username,))
        sid = cursor.fetchone()[0]
        
        #sid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
        cursor.execute("select qid,type from work_question where \
            wid=%s and number=%s;",(wid,number))
        Qid, Type = cursor.fetchone()
        if Type=='1':
            if answer==1:
                a = 'A'
            elif answer==2:
                a = 'B'
            elif answer==3:
                a = 'C'
            elif answer==4:
                a = 'D'
            else:
                a = None
            #User_Question.objects.filter(sid=sid,wid=wid,number=number).update(answer=a)
            cursor.execute("update user_question set anser=%s where \
                sid=%s and wid=%s and number=%s;",(a,sid,wid,number))
        elif Type=='2':
            cursor.execute("update user_question set anser=%s where \
                sid=%s and wid=%s and number=%s;",(answerList,sid,wid,number))
        elif Type=='3':
            if answer=='1':
                a = True
            elif answer=='0':
                a = False
            else:
                a = None
            cursor.execute("update user_question set anser=%s where \
                sid=%s and wid=%s and number=%s;",(a,sid,wid,number))
        elif Type=='4':
            cursor.execute("update user_question set anser=%s where \
                sid=%s and wid=%s and number=%s;",(answer,sid,wid,number))
        elif Type=='5':
            cursor.execute("update user_question set anser=%s where \
                sid=%s and wid=%s and number=%s;",(answer,sid,wid,number))
        cursor.close()
        return JsonResponse({"msg":1})

def CheckAnswer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        wid = data.get("wid")
        cursor = connection.cursor()
        cursor.execute("select id from public.user where username=%s;",(username,))
        sid = cursor.fetchone()[0]
        utime = data.get("time")
        cursor.execute("update user_work set finish='t',update=%s where wid=%s and \
            sid=%s;",(utime,wid,sid))
        #User_Work.objects.filter(wid=wid,sid=sid).update(finish=True)

        
        #uTime = utime[0:10]+" "+utime[11:19]
        #t = time.strptime(uTime, "%Y-%m-%d %H:%M:%S")
        #tt = datetime.datetime.fromtimestamp(int(time.mktime(t))+28800, pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
        #User_Work.objects.filter(wid=wid,sid=sid).update(update=utime)


        #finishnum = int("".join('%s' %id for id in list(Work.objects.filter(id=wid).values_list("finishnum"))))
        #Work.objects.filter(id=wid).update(finishnum=finishnum+1)
        cursor.execute("update work set finishnum=finishnum+1 where id=%s;",(wid,))
        result = []
        cursor.execute("select number from user_question where sid=%s and wid=%s \
            and type='1';",(sid,wid))
        number1 = cursor.fetchall()
        #list(User_Question.objects.filter(sid=sid,wid=wid,type='1').values_list("number"))
        for num1 in number1:
            #n1 = "".join('%s' %id for id in num1)
            cursor.execute("select answer,qid from user_question where sid=%s and wid=%s and number=%s;",
            (sid,wid,num1))
            answer1, qid1 = cursor.fetchone()
            #answer1 = "".join('%s' %id for id in list(User_Question.objects.filter(sid=sid,wid=wid,number=n1).values_list("answer")))
            #qid1 = "".join('%s' %id for id in list(User_Question.objects.filter(sid=sid,wid=wid,number=n1).values_list("qid")))
            #Answer1 = "".join('%s' %id for id in list(Simple.objects.filter(wid=wid,id=qid1).values_list("answer")))
            cursor.execute("select answer from simple where wid=%s and id=%s;",(wid,qid1))
            Answer1 = cursor.fetchone()[0]
            cursor.execute("update user_question set ischeck='t',judge=%s where sid=%s and wid=%s \
                and number=%s;",(answer1==Answer1,sid,wid,num1))
            #User_Question.objects.filter(sid=sid,wid=wid,number=n1).update(ischeck=True,judge=answer1==Answer1)
            result.append(num1)
            result.append(answer1==Answer1)

        cursor.execute("select number from user_question where sid=%s and wid=%s \
            and type='2';",(sid,wid))
        number2 = cursor.fetchall()
        for num2 in number2:
            #n2 = "".join('%s' %id for id in num2)
            #answer2 = "".join('%s' %id for id in list(User_Question.objects.filter(sid=sid,wid=wid,number=n2).values_list("answer")))
            cursor.execute("select answer,qid from user_question where sid=%s and wid=%s and number=%s;",
            (sid,wid,num2))
            answer2, qid2 = cursor.fetchone()
            #qid2 = "".join('%s' %id for id in list(User_Question.objects.filter(sid=sid,wid=wid,number=n2).values_list("qid")))
            cursor.execute("select answer from mutiple where wid=%s and id=%s;",(wid,qid2))
            Answer2 = cursor.fetchone()[0]
            cursor.execute("update user_question set ischeck='t',judge=%s where sid=%s and wid=%s \
                and number=%s;",(answer2==Answer2,sid,wid,num2))
            #Answer2 = "".join('%s' %id for id in list(Multiple.objects.filter(wid=wid,id=qid2).values_list("answer")))
            #User_Question.objects.filter(sid=sid,wid=wid,number=n2).update(ischeck=True,judge=answer2==Answer2)
            result.append(num2)
            result.append(answer2==Answer2)

        cursor.execute("select number from user_question where sid=%s and wid=%s \
            and type='3';",(sid,wid))
        number3 = cursor.fetchall()
        for num3 in number3:
            cursor.execute("select answer,qid from user_question where sid=%s and wid=%s and number=%s;",
            (sid,wid,num3))
            answer3, qid3 = cursor.fetchone()
            #qid2 = "".join('%s' %id for id in list(User_Question.objects.filter(sid=sid,wid=wid,number=n2).values_list("qid")))
            cursor.execute("select answer from judge where wid=%s and id=%s;",(wid,qid3))
            Answer3 = cursor.fetchone()[0]
            cursor.execute("update user_question set ischeck='t',judge=%s where sid=%s and wid=%s \
                and number=%s;",(answer3==Answer3,sid,wid,num3))
            #Answer2 = "".join('%s' %id for id in list(Multiple.objects.filter(wid=wid,id=qid2).values_list("answer")))
            #User_Question.objects.filter(sid=sid,wid=wid,number=n2).update(ischeck=True,judge=answer2==Answer2)
            result.append(num3)
            result.append(answer3==Answer3)
        print(result)


        return JsonResponse({"result":result})

def GetWrongQuestion(request):#查询错误的题目
    global UQid
    if request.method == "POST":
        cursor = connection.cursor()
        data = json.loads(request.body)
        username = data.get("username")
        cid = data.get("cid")
        ctime = data.get("ctime")
        sid = GetIdByUsername(username)
        if cid == None or cid=="":
            cursor.execute("select id from user_question where sid=%s and \
                ischeck='t' and judge='f';",(sid,))
            UQid = cursor.fetchall()
            #UQid = list(User_Question.objects.filter(sid=sid,ischeck=True,judge=False).values_list("id"))
        else:
            if ctime == None or ctime=="":
                print(1)
                cursor.execute("select user_question.id from work,user_question where cid=%s \
                    and wid=work.id and sid=%s and ischeck='t' and judge='f';",(cid,sid))
                UQid = cursor.fetchall()
                #widlist = list(Work.objects.filter(cid=cid).values_list("id"))
            else:
                cursor.execute("select user_question.id from work,user_question where cid=%s \
                    and wid=work.id and sid=%s and ctime=%s and ischeck='t' and judge='f';",(cid,sid,ctime))
                #widlist = list(Work.objects.filter(cid=cid,ctime=ctime).values_list("id"))
            '''UQid = []
            for workid in widlist:
                workid = "".join('%s' %id for id in workid)
                uquid = list(User_Question.objects.filter(wid=workid,sid=sid,ischeck=True,judge=False).values_list("id"))
                for uuuid in uquid:
                    uuuid = "".join('%s' %id for id in uuuid)
                    UQid.append(uuuid)'''
        result = []
        for uqid in UQid:
            cursor.execute("select wid from user_question where id=%s;",(uqid,))
            wid = cursor.fetchone()[0]
            cursor.execute("select user_question.wid,user_question.type,ctime,chapter,course.name,\
                            username,update,user_question.number from public.user,user_question,work,\
                            course,user_work where user_question.id=%s and work.id=user_question.wid and \
                            course.id=work.cid and course.tid=public.user.id and user_work.wid=user_question.wid \
                            and user_work.sid=%s;",(uqid,sid))
            '''Uqid = "".join('%s' %id for id in uqid)
            wid = list(User_Question.objects.filter(id=Uqid).values_list("wid"))
            Wid = "".join('%s' %id for id in wid)
            type = list(User_Question.objects.filter(id=Uqid).values_list("type"))
            t = int("".join('%s' %id for id in type))
            number = list(User_Question.objects.filter(id=Uqid).values_list("number"))
            cid = "".join('%s' %id for id in list(Work.objects.filter(id=Wid).values_list("cid")))
            ctime = list(Work.objects.filter(id=Wid).values_list("ctime"))
            chapter = list(Work.objects.filter(id=Wid).values_list("chapter"))
            name = list(Course.objects.filter(id=cid).values_list("name"))
            tid = "".join('%s' %id for id in list(Course.objects.filter(id=cid).values_list("tid")))
            tname = list(User.objects.filter(id=tid).values_list("username"))
            update = list(User_Work.objects.filter(wid=Wid,sid=sid).values_list("update"))
            result.append(Wid)
            result.append(type)
            result.append(ctime)
            result.append(chapter)
            result.append(name)
            result.append(tname)
            result.append(update)
            result.append(number)'''
            rs = cursor.fetchone()
            t = int(rs[1])
            number=rs[7]
            result.append(rs)
            cursor.execute("select qid from user_question where id=%s;",(uqid,))
            qid = cursor.fetchone()[0]
            #qid = "".join('%s' %id for id in list(User_Question.objects.filter(id=uqid).values_list("qid")))
            n = int(number)
            if t==1:
                cursor.execute("select content,choice1,choice2,choice3,choice4,answer,\
                    picture,explain from simple where id=%s;",(qid,))
                content,choice1,choice2,choice3,choice4,answer,picture,explain = \
                cursor.fetchone()
                cursor.execute("select answer from user_question where sid=%s and wid=%s \
                    and number=%s;",(sid,wid,n))
                Answer = cursor.fetchone()[0]
                result.append(content)
                result.append(choice1)
                result.append(choice2)
                result.append(choice3)
                result.append(choice4)
                result.append(answer)
                result.append(Answer)
                result.append(picture)
                result.append(explain)
            elif t==2:
                cursor.execute("select content,choice1,chhoice2,choice3,choice4,answer,\
                    picture,explain from mutiple where id=%s;",(qid,))
                content,choice1,choice2,choice3,choice4,answer,picture,explain = \
                cursor.fetchone()
                cursor.execute("select answer from user_question where sid=%s and wid=%s \
                    and number=%s;",(sid,wid,n))
                Answer = cursor.fetchone()[0]
                result.append(content)
                result.append(choice1)
                result.append(choice2)
                result.append(choice3)
                result.append(choice4)
                result.append(answer)
                result.append(Answer)
                result.append(picture)
                result.append(explain)
            elif t==3:
                cursor.execute("select content,answer,picture,explain from judge where \
                    id=%s;",(qid,))
                content,answer,picture,explain = cursor.fetchone()
                cursor.execute("select answer from user_question where sid=%s and \
                    wid=%s and number=%s;",(sid,wid,n))
                Answer=cursor.fetchone()[0]
                #content = list(Judge.objects.filter(id=qid).values_list("content"))
                choice1 = 1
                choice2 = 2
                choice3 = 3
                choice4 = 4
                '''answer = list(Judge.objects.filter(id=qid).values_list("answer"))
                Answer = list(User_Question.objects.filter(sid=sid,wid=Wid,number=n).values_list("answer"))
                picture = list(Judge.objects.filter(id=qid).values_list("picture"))
                explain = list(Judge.objects.filter(id=qid).values_list("explain"))'''
                result.append(content)
                result.append(choice1)
                result.append(choice2)
                result.append(choice3)
                result.append(choice4)
                result.append(answer)
                result.append(Answer)
                result.append(picture)
                result.append(explain)
            elif t==4:
                cursor.execute("select content,answer,picture,explain from blank where \
                    id=%s;",(qid,))
                content,answer,picture,explain = cursor.fetchone()
                cursor.execute("select answer from user_question where sid=%s and \
                    wid=%s and number=%s;",(sid,wid,n))
                Answer=cursor.fetchone()[0]
                #content = list(Blank.objects.filter(id=qid).values_list("content"))
                choice1 = 1
                choice2 = 2
                choice3 = 3
                choice4 = 4
                '''answer = list(Blank.objects.filter(id=qid).values_list("answer"))
                Answer = list(User_Question.objects.filter(sid=sid,wid=Wid,number=n).values_list("answer"))
                picture = list(Blank.objects.filter(id=qid).values_list("picture"))
                explain = list(Blank.objects.filter(id=qid).values_list("explain"))'''
                result.append(content)
                result.append(choice1)
                result.append(choice2)
                result.append(choice3)
                result.append(choice4)
                result.append(answer)
                result.append(Answer)
                result.append(picture)
                result.append(explain)
            elif t==5:
                cursor.execute("select content,answer,picture,explain from subjective where \
                    id=%s;",(qid,))
                content,answer,picture,explain = cursor.fetchone()
                cursor.execute("select answer from user_question where sid=%s and \
                    wid=%s and number=%s;",(sid,wid,n))
                Answer=cursor.fetchone()[0]
                #content = list(Subjective.objects.filter(id=qid).values_list("content"))
                choice1 = 1
                choice2 = 2
                choice3 = 3
                choice4 = 4
                '''answer = list(Subjective.objects.filter(id=qid).values_list("answer"))
                Answer = list(User_Question.objects.filter(sid=sid,wid=Wid,number=n).values_list("answer"))
                picture = list(Subjective.objects.filter(id=qid).values_list("picture"))
                explain = list(Subjective.objects.filter(id=qid).values_list("explain"))'''
                result.append(content) #8
                result.append(choice1)
                result.append(choice2)
                result.append(choice3)
                result.append(choice4)
                result.append(answer)
                result.append(Answer)
                result.append(picture) #15
                result.append(explain)
        cursor.close()
        if result==[]:
            return JsonResponse({"result":1})
        else:
            return JsonResponse({"result":result})

def UploadFile(request):#上传文件
    if request.method == "POST":
        cursor = connection.cursor()
        if request.GET.get("File") is not None:
            file = request.FILES.get("file")
            print(file)
            baseUrl = "workFile"
            image_name = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + file.name
            f = open(os.path.join(baseUrl,image_name),'wb+')
            for i in file.chunks():
                f.write(i)
            f.close()
            url = '/workFile/'+image_name
            cursor.close()
            return JsonResponse({"url":url})
        if request.GET.get("up") is not None:
            data = json.loads(request.body)
            username = data.get("username")
            wid = data.get("wid")
            fileUrl = data.get("fileUrl")
            #sid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
            sid = GetIdByUsername(username)
            yes = data.get("yes")
            if yes==True:
                datetime = data.get("datetime")
                cursor.execute("update user_work set file=%s, finish='t',update=%s \
                    where sid=%s and wid=%s;",(fileUrl,datetime,sid,wid))
                #User_Work.objects.filter(sid=sid,wid=wid).update(file=fileUrl,finish=True,update=datetime)
            else:
                cursor.execute("update user_work set file=%s where sid=%s and wid=%s;",
                (fileUrl,sid,wid))
                #User_Work.objects.filter(sid=sid,wid=wid).update(file=fileUrl)
            cursor.close()
            return JsonResponse({"msg":1})

def GetStudentQuestion(request):#教师端评分获得题目
    if request.method == "POST":
        data = json.loads(request.body)
        wid = data.get("wid")
        number = data.get("number")
        sid = data.get("sid")
        cursor = connection.cursor()
        cursor.execute("select qid,type from work_question where wid=%s and number=%s;",
        (wid,number))
        Qid, Type = cursor.fetchone()
        '''qid = list(Work_Question.objects.filter(wid=wid,number=number).values_list("qid"))
        Qid = "".join('%s' %id for id in qid)
        type = list(Work_Question.objects.filter(wid=wid,number=number).values_list("type"))
        Type = "".join('%s' %id for id in type)'''
        if Type=='1':
            cursor.execute("select answer from user_question where sid=%s and wid=%s \
                and qid=%s and number=%s and type=%s;",(sid,wid,Qid,number,Type))
            sanswer = cursor.fetchone()[0]
            #sanswer = list(User_Question.objects.filter(sid=sid,wid=wid,qid=Qid,number=number,type=Type).values_list("answer"))
            cursor.execute("select content,choice1,choice2,choice3,choice4,answer,picture \
                from simple where wid=%s and id=%s;",(wid,Qid))
            content,choice1,choice2,choice3,choice4,answer,picture = cursor.fetchone()
            '''content = list(Simple.objects.filter(wid=wid,id=Qid).values_list("content"))
            choice1 = list(Simple.objects.filter(wid=wid,id=Qid).values_list("choice1"))
            choice2 = list(Simple.objects.filter(wid=wid,id=Qid).values_list("choice2"))
            choice3 = list(Simple.objects.filter(wid=wid,id=Qid).values_list("choice3"))
            choice4 = list(Simple.objects.filter(wid=wid,id=Qid).values_list("choice4"))
            answer = list(Simple.objects.filter(wid=wid,id=Qid).values_list("answer"))'''
            result = sanswer==answer
            cursor.close()
            #picture = list(Simple.objects.filter(wid=wid,id=Qid).values_list("picture"))
            return JsonResponse({
                "type":Type,
                "content":content,
                "choice1":choice1,
                "choice2":choice2,
                "choice3":choice3,
                "choice4":choice4,
                "sanswer": sanswer,
                "answer": answer,
                "result":result,
                "picture":picture
            })
        elif Type=='2':
            cursor.execute("select answer from user_question where sid=%s and wid=%s \
                and qid=%s and number=%s and type=%s;",(sid,wid,Qid,number,Type))
            sanswer = cursor.fetchone()[0]
            #sanswer = list(User_Question.objects.filter(sid=sid,wid=wid,qid=Qid,number=number,type=Type).values_list("answer"))
            cursor.execute("select content,choice1,choice2,choice3,choice4,answer,picture \
                from mutiple where wid=%s and id=%s;",(wid,Qid))
            content,choice1,choice2,choice3,choice4,answer,picture = cursor.fetchone()
            '''sanswer = list(User_Question.objects.filter(sid=sid,wid=wid,qid=Qid,number=number,type=Type).values_list("answer"))

            content = list(Multiple.objects.filter(wid=wid,id=Qid).values_list("content"))
            choice1 = list(Multiple.objects.filter(wid=wid,id=Qid).values_list("choice1"))
            choice2 = list(Multiple.objects.filter(wid=wid,id=Qid).values_list("choice2"))
            choice3 = list(Multiple.objects.filter(wid=wid,id=Qid).values_list("choice3"))
            choice4 = list(Multiple.objects.filter(wid=wid,id=Qid).values_list("choice4"))
            answer = list(Multiple.objects.filter(wid=wid,id=Qid).values_list("answer"))'''
            result = sanswer==answer
            cursor.close()
            #picture = list(Multiple.objects.filter(wid=wid,id=Qid).values_list("picture"))
            return JsonResponse({
                "type":Type,
                "content":content,
                "choice1":choice1,
                "choice2":choice2,
                "choice3":choice3,
                "choice4":choice4,
                "sanswer": sanswer,
                "answer": answer,
                "result":result,
                "picture":picture
            })
        elif Type=='3':
            cursor.execute("select content,answer,picture from judge where wid=%s \
                and id=%s;",(wid,Qid))
            content,answer,picture = cursor.fetchone()
            cursor.execute("select answer from user_question where sid=%s and wid=%s \
                and qid=%s and number=%s and type=%s;",(sid,wid,Qid,number,Type))
            sanswer = cursor.fetchone()[0]
            '''sanswer = "".join('%s' %id for id in list(User_Question.objects.filter(sid=sid,wid=wid,qid=Qid,number=number,type=Type).values_list("answer")))

            content = list(Judge.objects.filter(wid=wid,id=Qid).values_list("content"))
            answer = "".join('%s' %id for id in list(Judge.objects.filter(wid=wid,id=Qid).values_list("answer")))'''
            result = sanswer==answer
            cursor.close()
            #picture = list(Judge.objects.filter(wid=wid,id=Qid).values_list("picture"))
            return JsonResponse({
                "type":Type,
                "content":content,
                "sanswer": sanswer,
                "answer": answer,
                "result":result,
                "picture":picture
            })
        elif Type=='4':
            cursor.execute("select answer,judge from user_question where sid=%s and wid=%s \
                and qid=%s and number=%s and type=%s;",(sid,wid,Qid,number,Type))
            sanswer,result = cursor.fetchone()
            cursor.execute("select content,answer,picture from blank where \
                wid=%s and id=%s;",(wid,Qid))
            content, answer, picture = cursor.fetchone()
            cursor.close()
            '''sanswer = list(User_Question.objects.filter(sid=sid,wid=wid,qid=Qid,number=number,type=Type).values_list("answer"))

            content = list(Blank.objects.filter(wid=wid,id=Qid).values_list("content"))
            answer = list(Blank.objects.filter(wid=wid,id=Qid).values_list("answer"))
            result = list(User_Question.objects.filter(sid=sid,wid=wid,qid=Qid,number=number,type=Type).values_list("judge"))
            picture = list(Blank.objects.filter(wid=wid,id=Qid).values_list("picture"))'''
            return JsonResponse({
                "type":Type,
                "content":content,
                "sanswer": sanswer,
                "answer": answer,
                "result":result,
                "picture":picture
            })
        elif Type=='5':
            cursor.execute("select answer,judge from user_question where sid=%s and wid=%s \
                and qid=%s and number=%s and type=%s;",(sid,wid,Qid,number,Type))
            sanswer,result = cursor.fetchone()
            cursor.execute("select content,answer,picture from subjective where \
                wid=%s and id=%s;",(wid,Qid))
            content, answer, picture = cursor.fetchone()
            cursor.close()
            '''sanswer = list(User_Question.objects.filter(sid=sid,wid=wid,qid=Qid,number=number,type=Type).values_list("answer"))

            content = list(Subjective.objects.filter(wid=wid,id=Qid).values_list("content"))
            answer = list(Subjective.objects.filter(wid=wid,id=Qid).values_list("answer"))
            result = list(User_Question.objects.filter(sid=sid,wid=wid,qid=Qid,number=number,type=Type).values_list("judge"))
            picture = list(Subjective.objects.filter(wid=wid,id=Qid).values_list("picture"))'''
            return JsonResponse({
                "type":Type,
                "content":content,
                "sanswer": sanswer,
                "answer": answer,
                "result":result,
                "picture":picture
            })

def UpdateResult(request):#上传批改结果
    if request.method == "POST":
        data = json.loads(request.body)
        cursor = connection.cursor()
        if request.GET.get("s") is not None:
            sid = data.get("sid")
            wid = data.get("wid")
            comment = data.get("comment")
            score = data.get("score")

            print(comment)
            print(score)
            cursor.execute("update user_work set comment=%s,score=%s,ifscore='t' \
                where sid=%s and wid=%s;",(comment,score,sid,wid))
            #User_Work.objects.filter(sid=sid,wid=wid).update(comment=comment,score=score,ifscore=True)
            return JsonResponse({"msg":1})

        sid = data.get("sid")
        wid = data.get("wid")
        n = data.get("number")
        result = data.get("result")
        cursor.execute("update user_question set ischeck='t',judge=%s \
            where sid=%s and wid=%s and number=%s;",(result=='1',sid,wid,n))
        #User_Question.objects.filter(sid=sid,wid=wid,number=n).update(ischeck=True,judge=result=='1')
        print(result=='1')

        return JsonResponse({"msg":1})

def GetC(request):#学生获得作业对的教师评语
    if request.method == "POST":
        cursor = connection.cursor()
        data = json.loads(request.body)
        username = data.get("username")
        sid = GetIdByUsername(username)
        #sid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
        wid = data.get("wid")
        cursor.execute("select comment,score from user_work where \
            sid=%s and wid=%s;",(sid,wid))
        comment, score = cursor.fetchone()
        cursor.close()
        #comment = list(User_Work.objects.filter(sid=sid,wid=wid).values_list("comment"))
        #score = list(User_Work.objects.filter(sid=sid,wid=wid).values_list("score"))
        return JsonResponse({"comment":comment,"score":score})

def UpTo(request):#上传
    if request.method == "POST":
        cursor = connection.cursor()
        data = json.loads(request.body)

        if request.GET.get("share") is not None:
            username = data.get("username")
            #sid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
            sid = GetIdByUsername(username)
            wid = data.get("wid")
            cursor.execute("select good from user_work where \
                sid=%s and wid=%s;",(sid,wid))
            good = cursor.fetchone()[0]
            good = str(good)
            #good = "".join('%s' %id for id in list(User_Work.objects.filter(sid=sid,wid=wid).values_list("good")))
            print(good)
            if good=='False' or good=='false':
                cursor.execute("update user_work set good='t' where \
                    sid=%s and wid=%s;",(sid,wid))
                #User_Work.objects.filter(sid=sid,wid=wid).update(good=True)
                cursor.close()
                return JsonResponse({"msg":1})
            else:
                cursor.close()
                return  JsonResponse({"msg":0})

        if request.GET.get("cloud") is not None:
            username = data.get("username")
            sid = GetIdByUsername(username)
            #sid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
            wid = data.get("wid")
            number = data.get("number")
            date = datetime.date.today()
            cursor.execute("select cloud from user_question where sid=%s and \
                wid=%s and number=%s;",(sid,wid,number))
            cloud = cursor.fetchone()[0]
            #cloud = "".join('%s' %id for id in list(User_Question.objects.filter(sid=sid,wid=wid,number=number).values_list("cloud")))
            if cloud=='False' or cloud=='false':
                cursor.execute("update user_question set upload_time=%s,cloud='t' where \
                    sid=%s and wid=%s and number=%s;",(date,sid,wid,number))
                cursor.close()
                #User_Question.objects.filter(sid=sid,wid=wid,number=number).update(upload_time=date,cloud=True)
                return  JsonResponse({"msg":1})
            else:
                cursor.close()
                return  JsonResponse({"msg":0})

        if request.GET.get("goodcloud") is not None:
            username = data.get("username")
            tid = GetIdByUsername(username)
            #tid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
            wid = data.get("wid")
            cid = data.get("cid")
            n = data.get("n")
            sid = data.get("sid")
            cursor.execute("select qid from work_question where wid=%s and \
                number=%s;",(wid,n))
            qid = cursor.fetchone()[0]
            #qid = "".join('%s' %id for id in list(Work_Question.objects.filter(wid=wid,number=n).values_list("qid")))
            ##content = "".join('%s' %id for id in list(Subjective.objects.filter(id=qid).values_list("content")))
            cursor.execute("select answer from user_question where \
                sid=%s and wid=%s and qid=%s and number=%s;",(sid,wid,qid,n))
            answer = cursor.fetchone()[0]
            #answer = "".join('%s' %id for id in list(User_Question.objects.filter(sid=sid,wid=wid,qid=qid,number=n).values_list("answer")))
            date = datetime.date.today()
            #id = "".join('%s' %id for id in list(GoodWork.objects.filter(wid=wid,sid=sid,tid=tid,qid=qid,answer=answer).values_list("id")))
            cursor.execute("select id from goodwork where wid=%s and sid=%s \
                and tid=%s and qid=%s and answer=%s;",(wid,sid,tid,qid,answer))
            id = cursor.fetchone()[0]
            if id=="" or id==None:
                cursor.execute("insert into goodwork(wid,cid,qid,tid,sid,answer,upload_time,is_read) \
                    values (%s,%s,%s,%s,%s,%s,%s,'f');",(wid,cid,qid,tid,sid,answer,date))
                cursor.close()
                #GoodWork.objects.create(wid=wid,cid=cid,qid=qid,tid=tid,sid=sid,answer=answer,upload_time=date)
                return JsonResponse({"msg":1})
            else:
                cursor.close()
                return JsonResponse({"msg":0})

def AddCourse(request):#添加课程
    global Type, i
    if request.method == "POST":
        cursor = connection.cursor()
        data = json.loads(request.body)
        if request.GET.get("delete") is not None:
            cid = data.get("cid")
            cursor.execute("delete from course where id=%s;",(cid,))
            cursor.close()
            #Course.objects.filter(id=cid).delete()
            return JsonResponse({"msg":1})

        if request.GET.get("edit") is not None:
            cid = data.get("cid")
            cursor.execute("select sname from user_course where cid=%s;",(cid,))
            yilist = cursor.fetchall()
            #yilist = list(User_Course.objects.filter(cid=cid).values_list("sname"))
            cursor.execute("select username from public.user where type='S';")
            alllist = cursor.fetchall()
            #alllist = list(User.objects.filter(type='S').values_list("username"))
            weilist = list(set(alllist)-set(yilist))
            cursor.close()
            return JsonResponse({"yilist":yilist,"weilist":weilist})

        if request.GET.get("getin") is not None:
            username = data.get("username")
            cid = data.get("cid")
            cursor.execute("select max(id) from user_course;")
            maxid = cursor.fetchone()[0]
            '''idlist = cursor.fetchall()
            #idlist = list(User_Course.objects.all().values_list("id"))
            for Id in idlist:
                id = int("".join('%s' %id for id in Id))
                i = 1
                if id>i:
                    i=id
            User_Course.objects.create(id=i+1,sname=username,cid=cid)'''
            cursor.execute("insert into user_course(id,sname,cid) values \
                (%s,%s,%s);",(maxid+1,username,cid))
            #number = int("".join('%s' %id for id in list(Course.objects.filter(id=cid).values_list("number"))))
            cursor.execute("update course set number=number+1 where id=%s;",(cid,))
            #Course.objects.filter(id=cid).update(number=number+1)
            cursor.close()
            return JsonResponse({"msg":1})

        if request.GET.get("getout") is not None:
            username = data.get("username")
            cid = data.get("cid")
            cursor.execute("delete from user_course where cid=%s and sname=%s",(cid,username))
            cursor.execute("update course set number=number+1 where id=%s;",(cid,))
            cursor.close()
            #User_Course.objects.filter(cid=cid,sname=username).delete()
            #number = int("".join('%s' %id for id in list(Course.objects.filter(id=cid).values_list("number"))))
            #Course.objects.filter(id=cid).update(number=number-1)
            return JsonResponse({"msg":1})

        username = data.get("username")
        tid = GetIdByUsername(username)
        #tid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
        coursename = data.get("coursename")
        year = data.get("year")
        semester = data.get("semester")
        ty = data.get("type")
        maxnum = data.get("maxnum")
        tname = data.get("tname")
        credit = data.get("credit")

        if not all([username,tid,coursename,year,semester,ty,maxnum,tname,credit]):
            return JsonResponse({"code":0, "msg":'信息不完整！'})
        else:
            cursor.execute("select * from course where year=%s;",(year,))
            yearlist = cursor.fetchall()
            #yearlist = list(Course.objects.filter(year=year).values_list())
            cid = year*10000+len(yearlist)+1
            if ty==1:
                Type = 'PR'
            elif ty==2:
                Type = 'PE'
            elif ty==3:
                Type = 'MR'
            elif ty==4:
                Type = 'ME'
            print(cid)

            cursor.execute("insert into course(id,name,credit,maxnum,tname,type,\
                year,semester,tid) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (cid,coursename,credit,maxnum,tname,Type,year,semester,tid))
            '''Course.objects.create(
                id=cid,
                name=coursename,
                credit=credit,
                maxnum=maxnum,
                tname=tname,
                type=Type,
                year=year,
                semester=semester,
                tid=tid
            )'''
            cursor.close()
            return JsonResponse({"code":1, "msg":'添加此课程成功！'})

#计算向量余弦
def dot_product(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))
def magnitude(vector):
    return math.sqrt(dot_product(vector, vector))
def similarity(v1, v2):
    return dot_product(v1, v2) / (magnitude(v1) * magnitude(v2) + .00000000001)
def Recommend(request):#错题推荐功能
    if request.method == "POST":
        data = json.loads(request.body)
        wid = data.get("wid")
        number = data.get("number")
        qid = int("".join('%s' %id for id in list(User_Question.objects.filter(wid=wid,number=number).values_list("qid"))))
        ty0 = int("".join('%s' %id for id in list(User_Question.objects.filter(wid=wid,number=number).values_list("type"))))

        current_work_dir = os.path.dirname(__file__)
        stopwords = open(current_work_dir+'/hit_stopwords.txt',encoding='UTF-8').read().replace('\n',' ').split()

        questionList = []
        questionData = []
        IdList1 = list(Simple.objects.all().values_list("id"))
        for Id1 in IdList1:
            id1 = int("".join('%s' %id for id in Id1))
            type = 1
            questionData1 = []
            questionData1.append(id1)
            questionData1.append(type)
            questionData.append(questionData1)
            content1 = "".join('%s' %id for id in list(Simple.objects.filter(id=id1).values_list('content')))
            choice1 = "".join('%s' %id for id in list(Simple.objects.filter(id=id1).values_list('choice1')))
            choice2 = "".join('%s' %id for id in list(Simple.objects.filter(id=id1).values_list('choice2')))
            choice3 = "".join('%s' %id for id in list(Simple.objects.filter(id=id1).values_list('choice3')))
            choice4 = "".join('%s' %id for id in list(Simple.objects.filter(id=id1).values_list('choice4')))
            questionList.append(content1+choice1+choice2+choice3+choice4)

        IdList2 = list(Multiple.objects.all().values_list("id"))
        for Id2 in IdList2:
            id2 = int("".join('%s' %id for id in Id2))
            type = 2
            questionData2 = []
            questionData2.append(id2)
            questionData2.append(type)
            questionData.append(questionData2)
            content2 = "".join('%s' %id for id in list(Multiple.objects.filter(id=id2).values_list('content')))
            Choice1 = "".join('%s' %id for id in list(Multiple.objects.filter(id=id2).values_list('choice1')))
            Choice2 = "".join('%s' %id for id in list(Multiple.objects.filter(id=id2).values_list('choice2')))
            Choice3 = "".join('%s' %id for id in list(Multiple.objects.filter(id=id2).values_list('choice3')))
            Choice4 = "".join('%s' %id for id in list(Multiple.objects.filter(id=id2).values_list('choice4')))
            questionList.append(content2+Choice1+Choice2+Choice3+Choice4)

        IdList3 = list(Judge.objects.all().values_list("id"))
        for Id3 in IdList3:
            id3 = int("".join('%s' %id for id in Id3))
            type = 3
            questionData3 = []
            questionData3.append(id3)
            questionData3.append(type)
            questionData.append(questionData3)
            content3 = "".join('%s' %id for id in list(Judge.objects.filter(id=id3).values_list('content')))
            questionList.append(content3)

        IdList4 = list(Blank.objects.all().values_list("id"))
        for Id4 in IdList4:
            id4 = int("".join('%s' %id for id in Id4))
            type = 4
            questionData4 = []
            questionData4.append(id4)
            questionData4.append(type)
            questionData.append(questionData4)
            content4 = "".join('%s' %id for id in list(Blank.objects.filter(id=id4).values_list('content')))
            answer4 = "".join('%s' %id for id in list(Blank.objects.filter(id=id4).values_list('answer')))
            questionList.append(content4+answer4)

        IdList5 = list(Subjective.objects.all().values_list("id"))
        for Id5 in IdList5:
            id5 = int("".join('%s' %id for id in Id5))
            type = 5
            questionData5 = []
            questionData5.append(id5)
            questionData5.append(type)
            questionData.append(questionData5)
            content5 = "".join('%s' %id for id in list(Subjective.objects.filter(id=id5).values_list('content')))
            answer5 = "".join('%s' %id for id in list(Subjective.objects.filter(id=id5).values_list('answer')))
            questionList.append(content5+answer5)

        sent_words = [list(jieba.cut(sent0)) for sent0 in questionList]
        document = [" ".join(sent0) for sent0 in sent_words]
        tfidf_model = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", max_df=0.6, stop_words=stopwords).fit(document)

        sparse_result = tfidf_model.transform(document)
        weight = sparse_result.toarray()

        qlist = []
        for i in range(len(weight)):
            if questionData[i][0]==qid and questionData[i][1]==ty0:
                print(questionData[i])
                for j in range(len(weight)):
                    sim = similarity(weight[i],weight[j])
                    if sim>=0.2 and j!=i:
                        if questionData[j][1]==1:
                            content = list(Simple.objects.filter(id=questionData[j][0]).values_list("content"))
                            choice1 = list(Simple.objects.filter(id=questionData[j][0]).values_list("choice1"))
                            choice2 = list(Simple.objects.filter(id=questionData[j][0]).values_list("choice2"))
                            choice3 = list(Simple.objects.filter(id=questionData[j][0]).values_list("choice3"))
                            choice4 = list(Simple.objects.filter(id=questionData[j][0]).values_list("choice4"))
                            answer = list(Simple.objects.filter(id=questionData[j][0]).values_list("answer"))
                            picture = list(Simple.objects.filter(id=questionData[j][0]).values_list("picture"))
                            explain = list(Simple.objects.filter(id=questionData[j][0]).values_list("explain"))
                            qlist.append(content)
                            qlist.append(choice1)
                            qlist.append(choice2)
                            qlist.append(choice3)
                            qlist.append(choice4)
                            qlist.append(answer)
                            qlist.append(picture)
                            qlist.append(1)
                            qlist.append(explain)
                        elif questionData[j][1]==2:
                            content = list(Multiple.objects.filter(id=questionData[j][0]).values_list("content"))
                            choice1 = list(Multiple.objects.filter(id=questionData[j][0]).values_list("choice1"))
                            choice2 = list(Multiple.objects.filter(id=questionData[j][0]).values_list("choice2"))
                            choice3 = list(Multiple.objects.filter(id=questionData[j][0]).values_list("choice3"))
                            choice4 = list(Multiple.objects.filter(id=questionData[j][0]).values_list("choice4"))
                            answer = list(Multiple.objects.filter(id=questionData[j][0]).values_list("answer"))
                            picture = list(Multiple.objects.filter(id=questionData[j][0]).values_list("picture"))
                            explain = list(Multiple.objects.filter(id=questionData[j][0]).values_list("explain"))
                            qlist.append(content)
                            qlist.append(choice1)
                            qlist.append(choice2)
                            qlist.append(choice3)
                            qlist.append(choice4)
                            qlist.append(answer)
                            qlist.append(picture)
                            qlist.append(2)
                            qlist.append(explain)
                        elif questionData[j][1]==3:
                            content = list(Judge.objects.filter(id=questionData[j][0]).values_list("content"))
                            choice1 = 1
                            choice2 = 2
                            choice3 = 3
                            choice4 = 4
                            answer = list(Judge.objects.filter(id=questionData[j][0]).values_list("answer"))
                            picture = list(Judge.objects.filter(id=questionData[j][0]).values_list("picture"))
                            explain = list(Judge.objects.filter(id=questionData[j][0]).values_list("explain"))
                            qlist.append(content)
                            qlist.append(choice1)
                            qlist.append(choice2)
                            qlist.append(choice3)
                            qlist.append(choice4)
                            qlist.append(answer)
                            qlist.append(picture)
                            qlist.append(3)
                            qlist.append(explain)
                        elif questionData[j][1]==4:
                            content = list(Blank.objects.filter(id=questionData[j][0]).values_list("content"))
                            choice1 = 1
                            choice2 = 2
                            choice3 = 3
                            choice4 = 4
                            answer = list(Blank.objects.filter(id=questionData[j][0]).values_list("answer"))
                            picture = list(Blank.objects.filter(id=questionData[j][0]).values_list("picture"))
                            explain = list(Blank.objects.filter(id=questionData[j][0]).values_list("explain"))
                            qlist.append(content)
                            qlist.append(choice1)
                            qlist.append(choice2)
                            qlist.append(choice3)
                            qlist.append(choice4)
                            qlist.append(answer)
                            qlist.append(picture)
                            qlist.append(4)
                            qlist.append(explain)
                        elif questionData[j][1]==5:
                            content = list(Subjective.objects.filter(id=questionData[j][0]).values_list("content"))
                            choice1 = 1
                            choice2 = 2
                            choice3 = 3
                            choice4 = 4
                            answer = list(Subjective.objects.filter(id=questionData[j][0]).values_list("answer"))
                            picture = list(Subjective.objects.filter(id=questionData[j][0]).values_list("picture"))
                            explain = list(Subjective.objects.filter(id=questionData[j][0]).values_list("explain"))
                            qlist.append(content)
                            qlist.append(choice1)
                            qlist.append(choice2)
                            qlist.append(choice3)
                            qlist.append(choice4)
                            qlist.append(answer)
                            qlist.append(picture)
                            qlist.append(5)
                            qlist.append(explain)
        if qlist==[]:
            return JsonResponse({"qlist":1})
        else:
            return JsonResponse({"qlist":qlist})

def GetGood(request):#获得优秀作业
    if request.method == "POST":
        cursor = connection.cursor()
        data = json.loads(request.body)
        if request.GET.get("S") is not None:
            username = data.get("username")
            #Courselist = list(User_Course.objects.filter(sname=username).values_list("cid"))
            cursor.execute("select work.id from work,user_course where \
                work.cid=user_course.cid and user_course.sname=%s;",(username,))
            widList = cursor.fetchall()
            '''widList = []
            for course in Courselist:
                cid = "".join('%s' %id for id in course)
                widlist = list(Work.objects.filter(cid=cid).values_list("id"))
                for wid0 in widlist:
                    Wid0 = "".join('%s' %id for id in wid0)
                    widList.append(Wid0)'''

            uwidlist = []
            goodworkList = []
            for Wid in widList:
                wid = "".join('%s' %id for id in Wid)
                cursor.execute("select id from user_work where wid=%s and good='t';",(wid,))
                UWidlist = cursor.fetchall()
                #UWidlist = list(User_Work.objects.filter(wid=wid,good=True).values_list("id"))
                for UWid in UWidlist:
                    uwid = "".join('%s' %id for id in UWid)
                    uwidlist.append(uwid)

            for id in uwidlist:
                id = "".join('%s' %id for id in id)
                cursor.execute("select update,sid,wid,file from user_work \
                    where id=%s;",(id,))
                update, sid, wid,file = cursor.fetchone()
                cursor.execute("select username from public.user where id=%s;",(sid,))
                user = cursor.fetchone()[0]
                cursor.execute("select cid,ctime,chapter from work where id=%s;",(wid,))
                cid,ctime,chapter = cursor.fetchone()
                workmsg = (ctime,chapter)
                cursor.execute("select admin_id from sharedarea where cid=%s;",(cid,))
                admin_id = cursor.fetchone()[0]
                if admin_id=="None" or admin_id=="":
                    admin = "无"
                else:
                    cursor.execute("select username from public.user where id=%s;",(admin_id,))
                    admin = cursor.fetchone()[0]
                    #admin = list(User.objects.filter(id=admin_id).values_list("username"))
                cursor.execute("select name,tid from course where id=%s;",(cid,))
                coursemsg, tid = cursor.fetchone()
                cursor.execute("select username from public.user where id=%s;",(tid,))
                tname = cursor.fetchone()[0]
                '''update = list(User_Work.objects.filter(id=id).values_list("update"))
                sid = "".join('%s' %id for id in list(User_Work.objects.filter(id=id).values_list("sid")))
                user = list(User.objects.filter(id=sid).values_list("username"))
                wid = "".join('%s' %id for id in list(User_Work.objects.filter(id=id).values_list("wid")))
                file = "".join('%s' %id for id in list(User_Work.objects.filter(id=id).values_list("file")))
                cid = "".join('%s' %id for id in list(Work.objects.filter(id=wid).values_list("cid")))
                admin_id = "".join('%s' %id for id in list(SharedArea.objects.filter(cid=cid).values_list("admin_id")))
                
                workmsg = list(Work.objects.filter(id=wid).values_list("ctime","chapter"))
                coursemsg = list(Course.objects.filter(id=cid).values_list("name"))
                tid = "".join('%s' %id for id in list(Course.objects.filter(id=cid).values_list("tid")))
                tname = list(User.objects.filter(id=tid).values_list("username"))'''
                goodworkList.append(wid)
                goodworkList.append(coursemsg)
                goodworkList.append(tname)
                goodworkList.append(workmsg)
                goodworkList.append(user)
                goodworkList.append(update)
                goodworkList.append(admin)
                goodworkList.append(file)
            cursor.close()
            return JsonResponse({"goodwork":goodworkList})

        if request.GET.get("delete") is not None:
            wid = data.get("wid")
            username = data.get("username")
            sid = GetIdByUsername(username)
            cursor.execute("update user_work set good='f' where \
                wid=%s and sid=%s;",(wid,sid))
            #sid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
            #User_Work.objects.filter(wid=wid,sid=sid).update(good=False)
            cursor.close()
            return JsonResponse({"msg":1})

        if request.GET.get("download") is not None:
            wid = data.get("wid")
            username = data.get("username")
            sid = GetIdByUsername(username)
            cursor.execute("select file from user_work where \
                wid=%s and sid=%s;",(wid,sid))
            file = cursor.fetchone()[0]
            #sid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
            #file = "".join('%s' %id for id in list(User_Work.objects.filter(wid=wid,sid=sid).values_list("file")))
            print(file)
            cursor.close()
            return JsonResponse({"file":file})

        if request.GET.get("T") is not None:
            username = data.get("username")
            tid = GetIdByUsername(username)
            #tid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
            '''Courselist = list(Course.objects.filter(tid=tid).values_list("id"))

            widList = []
            for course in Courselist:
                cid = "".join('%s' %id for id in course)
                widlist = list(Work.objects.filter(cid=cid).values_list("id"))
                for wid0 in widlist:
                    Wid0 = "".join('%s' %id for id in wid0)
                    widList.append(Wid0)'''
            cursor.execute("select work.id from work,course where \
                cid=course.id and tid=%s;",(tid,))
            widList = cursor.fetchall()
            print(widList)
            uwidlist = []
            goodworkList = []
            for Wid in widList:
                wid = "".join('%s' %id for id in Wid)
                cursor.execute("select id from user_work where wid=%s and good='t';",(wid,))
                UWidlist = cursor.fetchall()
                #UWidlist = list(User_Work.objects.filter(wid=wid,good=True).values_list("id"))
                for UWid in UWidlist:
                    uwid = "".join('%s' %id for id in UWid)
                    uwidlist.append(uwid)

            for id in uwidlist:
                id = "".join('%s' %id for id in id)
                cursor.execute("select update,sid,wid,file from user_work \
                    where id=%s;",(id,))
                update, sid, wid,file = cursor.fetchone()
                cursor.execute("select username from public.user where id=%s;",(sid,))
                user = cursor.fetchone()[0]
                cursor.execute("select cid,ctime,chapter from work where id=%s;",(wid,))
                cid,ctime,chapter = cursor.fetchone()
                workmsg = (ctime,chapter)
                cursor.execute("select name,tid from course where id=%s;",(cid,))
                coursemsg, tid = cursor.fetchone()
                cursor.execute("select username from public.user where id=%s;",(tid,))
                tname = cursor.fetchone()[0]
                goodworkList.append(wid)
                goodworkList.append(coursemsg)
                goodworkList.append(tname)
                goodworkList.append(workmsg)
                goodworkList.append(user)
                goodworkList.append(update)
                goodworkList.append(file)

            return JsonResponse({"goodwork":goodworkList})

def UploadMaterial(request):#上传资料
    if request.method == "POST":
        cursor = connection.cursor()
        if request.GET.get("File") is not None:
            file = request.FILES.get("file")
            print(file)
            baseUrl = "Share"
            file_name = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + file.name
            f = open(os.path.join(baseUrl,file_name),'wb+')
            for i in file.chunks():
                f.write(i)
            f.close()
            url = 'Share/'+file_name
            return JsonResponse({"url":url,"file":file.name})

        if request.GET.get("up") is not None:
            data = json.loads(request.body)
            username = data.get("username")
            sid = GetIdByUsername(username)
            #sid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
            cid = data.get("cid")
            cursor.execute("select id from sharedarea where cid=%s;",(cid,))
            aid = cursor.fetchone()[0]
            #aid = "".join('%s' %id for id in list(SharedArea.objects.filter(cid=cid).values_list("id")))
            file = data.get("file")
            ti = data.get("time")
            filename = data.get("filename")
            #Time = ti[0:10]+" "+ti[11:19]
            #t = time.strptime(Time, "%Y-%m-%d %H:%M:%S")
            #tt = datetime.datetime.fromtimestamp(int(time.mktime(t))+28800, pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("insert into share_file(data_name,data_file,upload_id,update_time,\
                aid) values (%s,%s,%s,%s,%s);",(filename,file,sid,ti,aid))
            cursor.close()
            #Share_File.objects.create(data_name=filename,data_file=file,upload_id=sid,update_time=ti,aid=aid)
            return JsonResponse({"msg":1})

def ShareArea(request):#教师管理共享区
    if request.method == "POST":
        cursor = connection.cursor()
        data = json.loads(request.body)
        if request.GET.get("get") is not None:
            cid = data.get("cid")
            cursor.execute("select id from sharedarea where cid=%s;",(cid,))
            id = cursor.fetchone()[0]
            #id = "".join('%s' %id for id in list(SharedArea.objects.filter(cid=cid).values_list("id")))
            if id=="":
                return JsonResponse({"msg":0})
            else:
                return JsonResponse({"msg":1})

        if request.GET.get("create") is not None:
            cid = data.get("cid")
            cursor.execute("insert into sharedarea(cid) values (%s);",(cid,))
            #SharedArea.objects.create(cid=cid)

            return JsonResponse({"msg":1})

        if request.GET.get("getstudent") is not None:
            cid = data.get("cid")
            #namelist = list(User_Course.objects.filter(cid=cid).values_list("sname"))
            cursor.execute("select public.user.id from user_course,public.user \
                where public.user.username=sname and cid=%s;",(cid,))
            student = cursor.fetchall()
            '''
            student=[]
            for Name in namelist:
                name = "".join('%s' %id for id in Name)
                sid = list(User.objects.filter(username=name).values_list("id"))
                student.append(name)
                student.append(sid)'''
            cursor.execute("select admin_id from sharedarea where cid=%s;",(cid,))
            admin_id = cursor.fetchone()[0]
            #admin_id = "".join('%s' %id for id in list(SharedArea.objects.filter(cid=cid).values_list("admin_id")))
            cursor.close()
            return JsonResponse({"student":student,"admin_id":admin_id})

        if request.GET.get("setstudent") is not None:
            sid = data.get("sid")
            cid = data.get("cid")
            cursor.execute("select admin_id from sharedarea where cid=%s;",(cid,))
            admin_id = cursor.fetchone()[0]
            #admin_id = "".join('%s' %id for id in list(SharedArea.objects.filter(cid=cid).values_list("admin_id")))
            if admin_id=="None":
                cursor.execute("update sharedarea set admin_id=%s where cid=%s;",(sid,cid))
                cursor.close()
                # SharedArea.objects.filter(cid=cid).update(admin_id=sid)
                return JsonResponse({"msg":1})
            else:
                cursor.close()
                return JsonResponse({"msg":0})

        if request.GET.get("change") is not None:
            sid = data.get("sid")
            cid = data.get("cid")
            cursor.execute("update sharedarea set admin_id=%s where cid=%s;",(sid,cid))
            #SharedArea.objects.filter(cid=cid).update(admin_id=sid)
            cursor.close()
            return JsonResponse({"msg":1})

def GetMaterial(request):#共享资料操作
    if request.method == "POST":
        cursor = connection.cursor()
        data = json.loads(request.body)
        if request.GET.get("S") is not None:
            username = data.get("username")
            '''Courselist = list(User_Course.objects.filter(sname=username).values_list("cid"))

            aidlist = []
            for course in Courselist:
                cid = "".join('%s' %id for id in course)
                aidlist.append("".join('%s' %id for id in list(SharedArea.objects.filter(cid=cid).values_list("id"))))

            fidlist = []
            for aid0 in aidlist:
                if aid0!='':
                    Fid = list(Share_File.objects.filter(aid=aid0).values_list("id"))
                    for fid in Fid:
                        fid = int("".join('%s' %id for id in fid))
                        fidlist.append(fid)
            fidlist.sort()'''
            cursor.execute("select share_file.id from share_file,sharedarea,user_course \
                where share_file.aid=sharedarea.id and sharedarea.cid=user_course.cid \
                    and user_course.sname=%s;",(username,))
            fidlist = cursor.fetchall()
            result = []
            for fid in fidlist:
                cursor.execute("select aid,upload_id,data_name,update_time from share_file \
                    where id=%s;",(fid,))
                aid, upload_id,data_name,update_time = cursor.fetchone()
                cursor.execute("select cid,admin_id from sharedarea where id=%s;",(aid,))
                cid, admin_id = cursor.fetchone()
                cursor.execute("select tid,name from course where id=%s;",(cid,))
                tid,coursemsg = cursor.fetchone()
                cursor.execute("select username from public.user where id=%s;",(tid,))
                tname = cursor.fetchone()[0]
                cursor.execute("select username from public.user where id=%s;",(upload_id,))
                user = cursor.fetchone()[0]
                filemsg = (data_name,update_time)
                '''aid = "".join('%s' %id for id in list(Share_File.objects.filter(id=fid).values_list("aid")))
                cid = "".join('%s' %id for id in list(SharedArea.objects.filter(id=aid).values_list("cid")))
                coursemsg = list(Course.objects.filter(id=cid).values_list("name"))
                tid = "".join('%s' %id for id in list(Course.objects.filter(id=cid).values_list("tid")))
                tname = list(User.objects.filter(id=tid).values_list("username"))
                upload_id = "".join('%s' %id for id in list(Share_File.objects.filter(id=fid).values_list("upload_id")))
                user = list(User.objects.filter(id=upload_id).values_list("username"))
                filemsg = list(Share_File.objects.filter(id=fid).values_list("data_name","update_time"))
                admin_id = "".join('%s' %id for id in list(SharedArea.objects.filter(cid=cid).values_list("admin_id")))'''
                if admin_id=="None":
                    admin = "无"
                else:
                    cursor.execute("select username from public.user where id=%s;",(admin_id,))
                    admin = cursor.fetchone()[0]
                result.append(fid)
                result.append(cid)
                result.append(coursemsg)
                result.append(tname)
                result.append(user)
                result.append(filemsg)
                result.append(admin)
            cursor.close()
            return JsonResponse({"result":result})

        if request.GET.get("down") is not None:
            fid = data.get("fid")
            #data_file = "".join('%s' %id for id in list(Share_File.objects.filter(id=fid).values_list("data_file")))
            cursor.execute('select data_file from share_file where id=%s;',(fid,))
            data_file = cursor.fetchone()[0]
            return JsonResponse({"file":data_file})

        if request.GET.get("delete") is not None:
            fid = data.get("fid")
            cursor.execute('select data_file from share_file where id=%s;',(fid,))
            file = cursor.fetchone()[0]
            #file = "".join('%s' %id for id in list(Share_File.objects.filter(id=fid).values_list("data_file")))
            url = file
            print(url)
            current_work_dir = os.path.dirname(os.getcwd())
            os.remove(current_work_dir+'/mysite'+url)
            #Share_File.objects.filter(id=fid).delete()
            cursor.execute("delete from share_file where id=%s;",(fid,))
            return JsonResponse({"msg":1})

        if request.GET.get("T") is not None:
            username = data.get("username")
            tid = GetIdByUsername(username)
            #tid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
            '''Courselist = list(Course.objects.filter(tid=tid).values_list("id"))

            aidlist = []
            for course in Courselist:
                cid = "".join('%s' %id for id in course)
                aidlist.append("".join('%s' %id for id in list(SharedArea.objects.filter(cid=cid).values_list("id"))))

            fidlist = []
            for aid0 in aidlist:
                if aid0!='':
                    Fid = list(Share_File.objects.filter(aid=aid0).values_list("id"))
                    for fid in Fid:
                        fid = int("".join('%s' %id for id in fid))
                        fidlist.append(fid)
            fidlist.sort()'''
            cursor.execute("select share_file.id from share_file,sharedarea,course \
                where share_file.aid=sharedarea.id and sharedarea.cid=course.id \
                    and course.tid=%s;",(tid,))
            fidlist = cursor.fetchall()
            result = []
            for fid in fidlist:
                cursor.execute("select aid,upload_id,data_name,update_time from share_file \
                    where id=%s;",(fid,))
                aid, upload_id,data_name,update_time = cursor.fetchone()
                cursor.execute("select cid,admin_id from sharedarea where id=%s;",(aid,))
                cid, admin_id = cursor.fetchone()
                cursor.execute("select tid,name from course where id=%s;",(cid,))
                tid,coursemsg = cursor.fetchone()
                cursor.execute("select username from public.user where id=%s;",(tid,))
                tname = cursor.fetchone()[0]
                cursor.execute("select username from public.user where id=%s;",(upload_id,))
                user = cursor.fetchone()[0]
                filemsg = (data_name,update_time)
                result.append(fid)
                result.append(cid)
                result.append(coursemsg)
                result.append(tname)
                result.append(user)
                result.append(filemsg)
            cursor.close()
            return JsonResponse({"result":result})

        if request.GET.get("getcourse") is not None:
            username = data.get("username")
            '''Courselist = list(User_Course.objects.filter(sname=username).values_list("cid"))
            
            courseList = []
            for course in Courselist:
                cid = "".join('%s' %id for id in course)
                name = list(Course.objects.filter(id=cid).values_list("name"))
                courseList.append(cid)
                courseList.append(name)'''
            cursor.execute("select cid,name from user_course,course where course.id=cid \
                and user_course.sname=%s;",(username,))
            courseList = cursor.fetchall()
            cursor.close()
            return JsonResponse({"course":courseList})

        if request.GET.get("insert") is not None:
            cid = data.get("cid")
            cursor.execute("select id from sharedarea where cid=%s;",(cid,))
            id = cursor.fetchone()[0]
            cursor.close()
            #id = "".join('%s' %id for id in list(SharedArea.objects.filter(cid=cid).values_list("id")))
            if id=="":
                return JsonResponse({"msg":0})
            else:
                return JsonResponse({"msg":1})

        if request.GET.get("teachercourse") is not None:
            username = data.get("username")
            tid = GetIdByUsername(username)
            #tid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
            cursor.execute("select id,name from course where tid=%s;",(tid,))
            courseList = cursor.fetchall()
            #courseList = list(Course.objects.filter(tid=tid).values_list("id","name"))
            cursor.close()
            return JsonResponse({"course":courseList})

        if request.GET.get("getwork") is not None:
            cid = data.get("cid")
            #wid = list(Work.objects.filter(cid=cid).values_list("ctime"))
            cursor.execute("select ctime from work where cid=%s;",(cid,))
            widlist = cursor.fetchall()
            '''widlist = []
            for Wid in wid:
                Wid = int("".join('%s' %id for id in Wid))
                widlist.append(Wid)
            widlist.sort()'''
            cursor.close()
            return JsonResponse({"wid":widlist})

def GetAnyWork(request):#获得作业
    if request.method == "POST":
        cursor = connection.cursor()
        data = json.loads(request.body)
        username = data.get("username")
        wid =data.get("wid")
        sid = GetIdByUsername(username)
        #sid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))

        #num = len(list(Work_Question.objects.filter(wid=wid).values_list()))
        cursor.execute("select count(*) from work_question where wid=%s;",(wid,))
        num = cursor.fetchone()[0]
        result = []
        for n in range(num):
            cursor.execute("select qid,type from work_question where wid=%s and number=%s;",
            (wid,n+1))
            qid,type = cursor.fetchone()
            cursor.execute("select answer,judge from user_question where \
                wid=%s and sid=%s and number=%s;",(wid,sid,n+1))
            aj = cursor.fetchone()
            if aj == None:
                Answer, judge = (None,None)
            else:
                Answer, judge = aj
            '''qid = "".join('%s' %id for id in list(Work_Question.objects.filter(wid=wid,number=n+1).values_list("qid")))
            type = "".join('%s' %id for id in list(Work_Question.objects.filter(wid=wid,number=n+1).values_list("type")))
            Answer = list(User_Question.objects.filter(wid=wid,sid=sid,number=n+1).values_list("answer"))
            judge = list(User_Question.objects.filter(wid=wid,sid=sid,number=n+1).values_list("judge"))'''
            result.append(type)
            result.append(Answer)
            result.append(judge)
            t = int(type)
            if t==1:
                cursor.execute("select content,choice1,choice2,choice3,choice4,answer,\
                    picture,explain from simple where id=%s;",(qid,))
                content,choice1,choice2,choice3,choice4,answer,picture,explain = \
                    cursor.fetchone()
                result.append(content)
                result.append(choice1)
                result.append(choice2)
                result.append(choice3)
                result.append(choice4)
                result.append(answer)
                result.append(picture)
                result.append(explain)
            elif t==2:
                cursor.execute("select content,choice1,choice2,choice3,choice4,answer,\
                    picture,explain from mutiple where id=%s;",(qid,))
                content,choice1,choice2,choice3,choice4,answer,picture,explain = \
                    cursor.fetchone()
                result.append(content)
                result.append(choice1)
                result.append(choice2)
                result.append(choice3)
                result.append(choice4)
                result.append(answer)
                result.append(picture)
                result.append(explain)
            elif t==3:
                cursor.execute("select content,answer,picture,explain from \
                    judge where id=%s;",(qid,))
                content,answer,picture,explain = cursor.fetchone()
                choice1 = 1
                choice2 = 2
                choice3 = 3
                choice4 = 4
                result.append(content)
                result.append(choice1)
                result.append(choice2)
                result.append(choice3)
                result.append(choice4)
                result.append(answer)
                result.append(picture)
                result.append(explain)
            elif t==4:
                cursor.execute("select content,answer,picture,explain from \
                    blank where id=%s;",(qid,))
                content,answer,picture,explain = cursor.fetchone()
                choice1 = 1
                choice2 = 2
                choice3 = 3
                choice4 = 4
                result.append(content)
                result.append(choice1)
                result.append(choice2)
                result.append(choice3)
                result.append(choice4)
                result.append(answer)
                result.append(picture)
                result.append(explain)
            elif t==5:
                cursor.execute("select content,answer,picture,explain from \
                    subjective where id=%s;",(qid,))
                content,answer,picture,explain = cursor.fetchone()
                choice1 = 1
                choice2 = 2
                choice3 = 3
                choice4 = 4
                result.append(content) #8
                result.append(choice1)
                result.append(choice2)
                result.append(choice3)
                result.append(choice4)
                result.append(answer)
                result.append(picture) #15
                result.append(explain)
        cursor.close()
        return JsonResponse({"qlist":result})

def Message(request):#消息相关处理
    if request.method == "POST":
        data = json.loads(request.body)
        cursor = connection.cursor()
        if request.GET.get("send") is not None:
            username = data.get("user")
            wid = data.get("wid")
            cursor.execute("select ctime,deadline,name from work,course where course.id=cid \
                and work.id=%s;",(wid,))
            ctime,deadline,cname = cursor.fetchone()
            tid = GetIdByUsername(username)
            cursor.execute("select sid from user_work where wid=%s and finish='f';",(wid,))
            sidlist = cursor.fetchall()
            
            for Sid in sidlist:
                sid = "".join('%s' %id for id in Sid)
                tittle = "作业提交时间即将截止"
                message = str(cname)+"第"+str(ctime)+"次作业将于"+str(deadline)+"截止，请您尽快提交！"
                print(tittle)
                print(message)
                cursor.execute("insert into work_message(tid,sid,tittle,message,read) values \
                    (%s,%s,%s,%s,'f');",(tid,sid,tittle,message))
                #Work_Message.objects.create(tid=tid,sid=sid,tittle=tittle,message=message)
            return JsonResponse({"msg":1})

        if request.GET.get("getnum") is not None:
            username = data.get("username")
            sid = GetIdByUsername(username)
            #sid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
            #num = len(list(Work_Message.objects.filter(sid=sid,read=False).values_list("id")))
            cursor.execute("select count(id) from work_message where sid=%s and \
                read='f';",(sid,))
            num = cursor.fetchone()[0]
            cursor.close()
            return JsonResponse({"num":num})

        if request.GET.get("getmessage") is not None:
            username = data.get("username")
            sid = GetIdByUsername(username)
            #sid = "".join('%s' %id for id in list(User.objects.filter(username=username).values_list("id")))
            cursor.execute("select id,tittle,message,read from work_message \
                where sid=%s;",(sid,))
            message = cursor.fetchall()
            cursor.close()
            #message = list(Work_Message.objects.filter(sid=sid).values_list("id","tittle","message","read"))
            if message==[]:
                return JsonResponse({"message":1})
            else:
                return JsonResponse({"message":message})

        if request.GET.get("change") is not None:
            mid = data.get("mid")
            cursor.execute("update work_message set read='t' where id=%s;",(mid,))
            cursor.close()
            #Work_Message.objects.filter(id=mid).update(read=True)

            return JsonResponse({"msg":1})

def GetInfo(request):#答题情况
    if request.method == "POST":
        cursor = connection.cursor()
        data = json.loads(request.body)
        wid = data.get("wid")
        #finishnum = int("".join('%s' %id for id in list(Work.objects.filter(id=wid).values_list("finishnum"))))
        cursor.execute("select finishnum from work where id=%s;",(wid,))
        finishnum = cursor.fetchone()[0]
        cursor.execute('select count(*) from work_question where wid=%s;',(wid,))
        num = cursor.fetchone()[0]
        #num = len(list(Work_Question.objects.filter(wid=wid).values_list()))
        result = []
        for n in range(num):
            cursor.execute("select qid,type from work_question where wid=%s and number=%s;",
            (wid,n+1))
            qid,type = cursor.fetchone()
            cursor.execute("select count(*) from user_question where wid=%s \
                and number=%s and judge='t';",(wid,n+1))
            right = cursor.fetchone()[0]
            #right = len(list(User_Question.objects.filter(wid=wid,number=n+1,judge=True).values_list()))
            wrong = finishnum-right
            result.append(type)
            result.append(right)
            result.append(wrong)
            t = int(type)
            if t==1:
                cursor.execute("select content,choice1,choice2,choice3,choice4,answer,\
                    picture,explain from simple where id=%s;",(qid,))
                content,choice1,choice2,choice3,choice4,answer,picture,explain = \
                    cursor.fetchone()
                result.append(content)
                result.append(choice1)
                result.append(choice2)
                result.append(choice3)
                result.append(choice4)
                result.append(answer)
                result.append(picture)
                result.append(explain)
            elif t==2:
                cursor.execute("select content,choice1,choice2,choice3,choice4,answer,\
                    picture,explain from mutiple where id=%s;",(qid,))
                content,choice1,choice2,choice3,choice4,answer,picture,explain = \
                    cursor.fetchone()
                result.append(content)
                result.append(choice1)
                result.append(choice2)
                result.append(choice3)
                result.append(choice4)
                result.append(answer)
                result.append(picture)
                result.append(explain)
            elif t==3:
                cursor.execute("select content,answer,picture,explain from \
                    judge where id=%s;",(qid,))
                content,answer,picture,explain = cursor.fetchone()
                choice1 = 1
                choice2 = 2
                choice3 = 3
                choice4 = 4
                result.append(content)
                result.append(choice1)
                result.append(choice2)
                result.append(choice3)
                result.append(choice4)
                result.append(answer)
                result.append(picture)
                result.append(explain)
            elif t==4:
                cursor.execute("select content,answer,picture,explain from \
                    blank where id=%s;",(qid,))
                content,answer,picture,explain = cursor.fetchone()
                choice1 = 1
                choice2 = 2
                choice3 = 3
                choice4 = 4
                result.append(content)
                result.append(choice1)
                result.append(choice2)
                result.append(choice3)
                result.append(choice4)
                result.append(answer)
                result.append(picture)
                result.append(explain)
            elif t==5:
                cursor.execute("select content,answer,picture,explain from \
                    subjective where id=%s;",(qid,))
                content,answer,picture,explain = cursor.fetchone()
                choice1 = 1
                choice2 = 2
                choice3 = 3
                choice4 = 4
                result.append(content) #8
                result.append(choice1)
                result.append(choice2)
                result.append(choice3)
                result.append(choice4)
                result.append(answer)
                result.append(picture) #15
                result.append(explain)
        cursor.close()

        return JsonResponse({"qlist":result})
