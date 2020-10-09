from django.shortcuts import render

# Create your views here.
import json
import os
import random

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from docx import Document

# Create your views here.
from backend.models import *
from django.db import connection

cursor = connection.cursor()

def GetIdByUsername(username):
    cursor = connection.cursor()
    cursor.execute("select id from public.user where username=%s;",
    (username,))
    Id = cursor.fetchone()[0]
    cursor.close()
    return Id
# 注册
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)

        if request.GET.get("select") is not None:
            select_username = data.get("select_username")
            print(select_username)
            try:
                User.objects.get(username=select_username)
                return JsonResponse({
                    "status": 0,
                    "is_indb": 1
                })
            except:
                return JsonResponse({
                    'status': 0,
                    "is_indb": 0
                })
        username = data.get("username")
        type = data.get("type")
        password = data.get("password")
        email = data.get("email")
        if username is not None and password is not None and email is not None:
            user = User.objects.create_user(username=username, type=type, password=password, email=email)
            user.save()
            login_user = authenticate(request, username=username, password=password)
            if login_user:
                if type == 'T':
                    return JsonResponse({
                        "status": 0,
                        "type": "T",
                        "username": username,
                        "message": "Register and Login Success"
                    })
                else:
                    return JsonResponse({
                        "status": 0,
                        "type": "S",
                        "username": username,
                        "message": "Register and Login Success"
                    })
        else:
            return JsonResponse({
                "status": 2,
                "message": "注册失败, 该用户名已经存在."
            })

    else:
        return JsonResponse({
            "status": 1,
            "message": "error method"
        })


# 登录
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        if username is not None and password is not None:
            islogin = authenticate(request, username=username, password=password)
            type = User.objects.get(username=username).type
            if islogin:
                return JsonResponse({
                    "status": 0,
                    "message": "Login Success",
                    "type": type,
                    "username": username
                })
            else:
                return JsonResponse({
                    "status": 1,
                    "message": "登录失败, 请检查用户名或者密码是否输入正确."
                })
        else:
            return JsonResponse({
                "status": 2,
                "message": "参数错误"
            })


# 用户头像路径查询
def getAvatar(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        user = User.objects.get(username=username)
        return JsonResponse({
            "img": user.user_avatar
        })


# 教师课程查询
def findCourse(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        tid = User.objects.get(username=username)
        courseList = ExamCourse.objects.filter(tid=tid)
        nameList = []
        for course in courseList:
            nameList.append(course.name)
        return JsonResponse({
            "nameList": nameList
        })


# 添加试题
def addQuestion(request):
    if request.method == "POST":
        type = request.POST.get("type")
        username = request.POST.get("username")
        if type == '1':  # 单选
            content = request.POST.get("content")
            choice1 = request.POST.get("choice1")
            choice2 = request.POST.get("choice2")
            choice3 = request.POST.get("choice3")
            choice4 = request.POST.get("choice4")
            answer = request.POST.get("answer")
            picture = request.FILES.get("picture")
            if picture is not None:
                baseUrl = "media/question"
                destination = open(os.path.join(baseUrl + "/simple/", picture.name), 'wb+')
                for chunk in picture.chunks():
                    destination.write(chunk)
                destination.close()
            course = request.POST.get("course")
            chapter = request.POST.get("chapter")
            section = request.POST.get("section")
            count = request.POST.get("count")
            tid = User.objects.get(username=username)
            try:
                cursor.execute("insert into exam_question(type,tid,cid,chapter,section,count) values \
                    (%s,%s,%s,%s,%s,%s);",(type,tid.id,ExamCourse.objects.get(name=course).id,chapter,section,count))
                qid = ExamQuestion.objects.last().id
                cursor.execute("insert into exam_simple(content,choice1,choice2,choice3,choice4,\
                    answer,qid,picture) values (%s,%s,%s,%s,%s,%s,%s,%s);",(content,choice1,choice2,
                        choice3,choice4,answer,ExamQuestion.objects.get(id=qid).id,picture))
                #obj = ExamSimple(content=content, choice1=choice1, choice2=choice2, choice3=choice3, choice4=choice4,
                #                 answer=answer, qid=ExamQuestion.objects.get(id=qid), picture=picture)
                #obj.save()
            except Exception as e:
                print(e)
                return JsonResponse({
                    "msg": "添加失败"
                })
            return JsonResponse({
                "msg": "单选题添加成功"
            })
        elif type == "2":  # 多选
            content = request.POST.get("content")
            choice1 = request.POST.get("choice1")
            choice2 = request.POST.get("choice2")
            choice3 = request.POST.get("choice3")
            choice4 = request.POST.get("choice4")
            answerList = request.POST.get("answerList")
            answer = []
            for aw in answerList:
                if aw is not None and aw != ',':
                    answer.append(aw)
            picture = request.FILES.get("picture")
            if picture is not None:
                baseUrl = "media/question"
                destination = open(os.path.join(baseUrl + "/multiple", picture.name), 'wb+')
                for chunk in picture.chunks():
                    destination.write(chunk)
                destination.close()
            course = request.POST.get("course")
            chapter = request.POST.get("chapter")
            section = request.POST.get("section")
            count = request.POST.get("count")
            tid = User.objects.get(username=username)
            try:
                cursor.execute("insert into exam_question(type,tid,cid,chapter,section,count) values \
                    (%s,%s,%s,%s,%s,%s);",(type,tid,ExamCourse.objects.get(name=course),chapter,section,count))
                qid = ExamQuestion.objects.last().id
                cursor.execute("insert into exam_multiple(content,choice1,choice2,choice3,choice4,\
                    answer,qid,picture) values (%s,%s,%s,%s,%s,%s,%s,%s);",(content,choice1,choice2,
                        choice3,choice4,answer,ExamQuestion.objects.get(id=qid),picture))
                '''ExamQuestion.objects.create(type=type, tid=tid, cid=ExamCourse.objects.get(name=course),
                                            chapter=chapter, section=section, count=count)
                qid = ExamQuestion.objects.last().id
                obj = ExamMultiple(content=content, choice1=choice1, choice2=choice2, choice3=choice3, choice4=choice4,
                                   answer=answer, qid=ExamQuestion.objects.get(id=qid), picture=picture)
                obj.save()'''
            except Exception as e:
                print(e)
                return JsonResponse({
                    "msg": "添加失败"
                })
            return JsonResponse({
                "msg": "多选题添加成功"
            })
        elif type == "3":  # 填空
            content = request.POST.get("content")
            answer = request.POST.get("answer")
            picture = request.FILES.get("picture")
            if picture is not None:
                baseUrl = "media/question"
                destination = open(os.path.join(baseUrl + "/blank", picture.name), 'wb+')
                for chunk in picture.chunks():
                    destination.write(chunk)
                destination.close()
            course = request.POST.get("course")
            chapter = request.POST.get("chapter")
            section = request.POST.get("section")
            count = request.POST.get("count")
            tid = User.objects.get(username=username)
            try:
                cursor.execute("insert into exam_question(type,tid,cid,chapter,section,count) values \
                    (%s,%s,%s,%s,%s,%s);",(type,tid.id,ExamCourse.objects.get(name=course).id,chapter,section,count))
                qid = ExamQuestion.objects.last().id
                cursor.execute("insert into exam_blank(content,answer,qid,picture) values \
                    (%s,%s,%s,%s,%s,%s,%s,%s);",(content,answer,ExamQuestion.objects.get(id=qid).id,picture))
                '''ExamQuestion.objects.create(type=type, tid=tid, cid=ExamCourse.objects.get(name=course),
                                            chapter=chapter, section=section, count=count)
                qid = ExamQuestion.objects.last().id
                obj = ExamBlank(content=content, answer=answer, qid=ExamQuestion.objects.get(id=qid),
                                picture=picture)
                obj.save()'''
            except Exception as e:
                print(e)
                return JsonResponse({
                    "msg": "添加失败"
                })
            return JsonResponse({
                "msg": "填空题添加成功"
            })
        elif type == "4":  # 判断题
            content = request.POST.get("content")
            answer = request.POST.get("answer")
            picture = request.FILES.get("picture")
            if picture is not None:
                baseUrl = "media/question"
                destination = open(os.path.join(baseUrl + "/judge", picture.name), 'wb+')
                for chunk in picture.chunks():
                    destination.write(chunk)
                destination.close()
            course = request.POST.get("course")
            chapter = request.POST.get("chapter")
            section = request.POST.get("section")
            count = request.POST.get("count")
            tid = User.objects.get(username=username)
            try:
                cursor.execute("insert into exam_question(type,tid,cid,chapter,section,count) values \
                    (%s,%s,%s,%s,%s,%s);",(type,tid.id,ExamCourse.objects.get(name=course).id,chapter,section,count))
                qid = ExamQuestion.objects.last().id
                cursor.execute("insert into exam_judge(content,answer,qid,picture) values \
                    (%s,%s,%s,%s,%s,%s,%s,%s);",(content,answer,ExamQuestion.objects.get(id=qid).id,picture))
                '''ExamQuestion.objects.create(type=type, tid=tid, cid=ExamCourse.objects.get(name=course),
                                            chapter=chapter, section=section, count=count)
                qid = ExamQuestion.objects.last().id
                obj = ExamJudge(content=content, answer=answer, qid=ExamQuestion.objects.get(id=qid),
                                picture=picture)
                obj.save()'''
            except Exception as e:
                print(e)
                return JsonResponse({
                    "msg": "添加失败"
                })
            return JsonResponse({
                "msg": "判断题添加成功"
            })
        elif type == "5":  # 主观题
            content = request.POST.get("content")
            answer = request.POST.get("answer")
            picture = request.FILES.get("picture")
            if picture is not None:
                baseUrl = "media/question"
                destination = open(os.path.join(baseUrl + "/subjective", picture.name), 'wb+')
                for chunk in picture.chunks():
                    destination.write(chunk)
                destination.close()
            course = request.POST.get("course")
            chapter = request.POST.get("chapter")
            section = request.POST.get("section")
            count = request.POST.get("count")
            tid = User.objects.get(username=username)
            try:
                cursor.execute("insert into exam_question(type,tid,cid,chapter,section,count) values \
                    (%s,%s,%s,%s,%s,%s);",(type,tid.id,ExamCourse.objects.get(name=course).id,chapter,section,count))
                qid = ExamQuestion.objects.last().id
                cursor.execute("insert into exam_subjective(content,answer,qid,picture) values \
                    (%s,%s,%s,%s,%s,%s,%s,%s);",(content,answer,ExamQuestion.objects.get(id=qid).id,picture))
                '''ExamQuestion.objects.create(type=type, tid=tid, cid=ExamCourse.objects.get(name=course),
                                            chapter=chapter, section=section, count=count)
                qid = ExamQuestion.objects.last().id
                obj = ExamSubjective(content=content, answer=answer, qid=ExamQuestion.objects.get(id=qid),
                                     picture=picture)
                obj.save()'''
            except Exception as e:
                print(e)
                return JsonResponse({
                    "msg": "添加失败"
                })
            return JsonResponse({
                "msg": "主观题添加成功"
            })
        else:
            return JsonResponse({
                "msg": "添加失败",
                "type": type
            })


# 解析docx文件添加试题
def analyseDocx(request):
    if request.method == "POST":
        username = request.POST.get("username")
        uid = User.objects.get(username=username)
        docx = request.FILES.get("docx")
        if docx is not None:
            baseUrl = "media/docx"
            destination = open(os.path.join(baseUrl, docx.name), 'wb+')
            for chunk in docx.chunks():
                destination.write(chunk)
            destination.close()
        doc = Document(docx)
        contentList = []
        for p in doc.paragraphs:
            if p.text != "":
                contentList.append(p.text)
        if addWordToDB(contentList, uid, 0) is False:
            return JsonResponse({
                "msg": "上传失败，请参照上传说明检查文件内容格式"
            })
        return JsonResponse({
            "msg": "上传成功"
        })


# 将字符串列表转化为试题数据并添加至数据库
def addWordToDB(contentList, uid, n):
    length = len(contentList)
    if n >= length:
        return True
    type = contentList[n]
    courseName = contentList[n + 1]
    course = ExamCourse.objects.get(name=courseName)
    chapter = contentList[n + 2]
    section = contentList[n + 3]
    content = contentList[n + 4]
    next = 0
    if type == "1":
        choice1 = contentList[n + 5]
        choice2 = contentList[n + 6]
        choice3 = contentList[n + 7]
        choice4 = contentList[n + 8]
        answer = contentList[n + 9]
        count = contentList[n + 10]
        try:
            question = ExamQuestion.objects.create(type=type, tid=uid, cid=course, chapter=chapter, section=section, count=count)
            ExamSimple.objects.create(content=content, choice1=choice1, choice2=choice2,
                                      choice3=choice3, choice4=choice4, answer=answer, qid=question)
        except Exception as e:
            print(e)
            return False
        next = n + 11
    elif type == "2":
        choice1 = contentList[n + 5]
        choice2 = contentList[n + 6]
        choice3 = contentList[n + 7]
        choice4 = contentList[n + 8]
        answerList = contentList[n + 9]
        count = contentList[n + 10]
        answer = []
        for aw in answerList:
            answer.append(aw)
        try:
            question = ExamQuestion.objects.create(type=type, tid=uid, cid=course,
                                                   chapter=chapter, section=section, count=count)
            ExamMultiple.objects.create(content=content, choice1=choice1, choice2=choice2,
                                      choice3=choice3, choice4=choice4, answer=answer, qid=question)
        except Exception as e:
            print(e)
            return False
        next = n + 11
    elif type == "3":
        answer = contentList[n + 5]
        count = contentList[n + 6]
        try:
            question = ExamQuestion.objects.create(type=type, tid=uid, cid=course,
                                                   chapter=chapter, section=section, count=count)
            ExamBlank.objects.create(content=content, answer=answer, qid=question)
        except Exception as e:
            print(e)
            return False
        next = n + 7
    elif type == "4":
        answer = contentList[n + 5]
        count = contentList[n + 6]
        try:
            question = ExamQuestion.objects.create(type=type, tid=uid, cid=course,
                                                   chapter=chapter, section=section, count=count)
            ExamJudge.objects.create(content=content, answer=answer, qid=question)
        except Exception as e:
            print(e)
            return False
        next = n + 7
    elif type == "5":
        answer = contentList[n + 5]
        count = contentList[n + 6]
        try:
            question = ExamQuestion.objects.create(type=type, tid=uid, cid=course,
                                                   chapter=chapter, section=section, count=count)
            ExamSubjective.objects.create(content=content, answer=answer, qid=question)
        except Exception as e:
            print(e)
            return False
        next = n + 7
    else:
        return False
    if next == length:
        return True
    else:
        return addWordToDB(contentList, uid, next)


# 查询自己添加的试题
def selectQuestion(request):
    if request.method == "GET":
        username = request.GET.get("username")
        page = int(request.GET.get("currentPage"))
        tid = User.objects.get(username=username).id
        qList = list(ExamQuestion.objects.filter(tid=tid))
        qList.sort(key=lambda x: x.id)
        retList = []
        for question in qList:
            qid = question.id
            cid = question.cid.id
            if question.type == '1':
                try:
                    ExamSimple.objects.get(qid=qid)
                    retList.append({
                        "id": qid,
                        "course": ExamCourse.objects.get(id=cid).name,
                        "type": "单项选择题",
                        "content": ExamSimple.objects.get(qid=qid).content
                    })
                except ExamSimple.DoesNotExist:
                    continue
            elif question.type == '2':
                try:
                    ExamMultiple.objects.get(qid=qid)
                    retList.append({
                        "id": qid,
                        "course": ExamCourse.objects.get(id=cid).name,
                        "type": "多项选择题",
                        "content": ExamMultiple.objects.get(qid=qid).content
                    })
                except ExamMultiple.DoesNotExist:
                    continue
            elif question.type == '3':
                try:
                    ExamBlank.objects.get(qid=qid)
                    retList.append({
                        "id": qid,
                        "course": ExamCourse.objects.get(id=cid).name,
                        "type": "填空题",
                        "content": ExamBlank.objects.get(qid=qid).content
                    })
                except ExamBlank.DoesNotExist:
                    continue
            elif question.type == '4':
                try:
                    ExamJudge.objects.get(qid=qid)
                    retList.append({
                        "id": qid,
                        "course": ExamCourse.objects.get(id=cid).name,
                        "type": "判断题",
                        "content": ExamJudge.objects.get(qid=qid).content
                    })
                except ExamJudge.DoesNotExist:
                    continue
            elif question.type == '5':
                try:
                    ExamSubjective.objects.get(qid=qid)
                    retList.append({
                        "id": qid,
                        "course": ExamCourse.objects.get(id=cid).name,
                        "type": "主观题",
                        "content": ExamSubjective.objects.get(qid=qid).content
                    })
                except ExamSubjective.DoesNotExist:
                    continue
        total = len(retList)
        ret = retList[10 * (page - 1) + 1:10 * page + 1]
        return JsonResponse({
            "tableData": ret,
            "total": total,
            "currentPage": page
        })


# 查询试题具体信息
def findQuestion(request):
    if request.method == "GET":
        qid = request.GET.get("qid")
        question = ExamQuestion.objects.get(id=int(qid))
        if question.type == "1":
            simple = ExamSimple.objects.get(qid=question)
            return JsonResponse({
                "type": question.type,
                "content": simple.content,
                "choice1": simple.choice1,
                "choice2": simple.choice2,
                "choice3": simple.choice3,
                "choice4": simple.choice4,
                "answer": simple.answer,
                "count": question.count
            })
        elif question.type == "2":
            multiple = ExamMultiple.objects.get(qid=question)
            return JsonResponse({
                "type": question.type,
                "content": multiple.content,
                "choice1": multiple.choice1,
                "choice2": multiple.choice2,
                "choice3": multiple.choice3,
                "choice4": multiple.choice4,
                "answerList": multiple.answer,
                "count": question.count
            })
        elif question.type == "3":
            blank = ExamBlank.objects.get(qid=question)
            return JsonResponse({
                "type": question.type,
                "content": blank.content,
                "answer": blank.answer,
                "count": question.count
            })
        elif question.type == "4":
            judge = ExamJudge.objects.get(qid=question)
            return JsonResponse({
                "type": question.type,
                "content": judge.content,
                "answer": judge.answer,
                "count": question.count
            })
        elif question.type == "5":
            subjective = ExamSubjective.objects.get(qid=question)
            return JsonResponse({
                "type": question.type,
                "content": subjective.content,
                "answer": subjective.answer,
                "count": question.count
            })


# 修改试题信息
def changeQuestion(request):
    if request.method == "POST":
        data = request.POST
        qid = data.get("qid")
        type = data.get("type")
        question = ExamQuestion.objects.get(id=int(qid))
        cursor.execute("update exam_question set count=%s where id=%s;",
        (data.get("count"),int(qid)))
        #question.count = data.get("count")
        #question.save()
        if type == "1":
            cursor.execute("update exam_simple set content=%s,choice1=%s,choice2=%s,\
                choice3=%s,choice4=%s,answer=%s where qid=%s;",(data.get("content"),
                data.get("choice1"),data.get("choice2"),data.get("choice3"),data.get("choice4"),
                data.get("answer"),question.id))
            '''simple = ExamSimple.objects.get(qid=question)
            simple.content = data.get("content")
            simple.choice1 = data.get("choice1")
            simple.choice2 = data.get("choice2")
            simple.choice3 = data.get("choice3")
            simple.choice4 = data.get("choice4")
            simple.answer = data.get("answer")
            simple.save()'''
        elif type == "2":
            '''multiple = ExamMultiple.objects.get(qid=question)
            multiple.content = data.get("content")
            multiple.choice1 = data.get("choice1")
            multiple.choice2 = data.get("choice2")
            multiple.choice3 = data.get("choice3")
            multiple.choice4 = data.get("choice4")'''
            answerList = data.get("answerList")
            answer = []
            for aw in answerList:
                if aw == "A" or answer == "B" or answer == "C" or answer == "D":
                    answer.append(aw)
            #multiple.answer = answer
            cursor.execute("update exam_multiple set content=%s,choice1=%s,choice2=%s,\
                choice3=%s,choice4=%s,answer=%s where qid=%s;",(data.get("content"),
                data.get("choice1"),data.get("choice2"),data.get("choice3"),data.get("choice4"),
                answer,question.id))
            #multiple.save()
        elif type == "3":
            cursor.execute("update exam_blank set content=%s,answer=%s where \
                qid=%s;",(data.get("content"),data.get("answer"),question.id))
            '''blank = ExamBlank.objects.get(qid=question)
            blank.content = data.get("content")
            blank.answer = data.get("answer")
            blank.save()'''
        elif type == "4":
            '''judge = ExamJudge.objects.get(qid=question)
            judge.content = data.get("content")'''
            janswer = data.get("answer")
            answer = True
            if janswer == "0":
                answer = False
            #judge.answer = answer
            cursor.execute("update exam_judge set content=%s,answer=%s where \
                qid=%s;",(data.get("content"),answer,question.id))
            #judge.save()
        elif type == "5":
            cursor.execute("update exam_subjective set content=%s,answer=%s where \
                qid=%s;",(data.get("content"),data.get("answer"),question.id))
            '''subjective = ExamSubjective.objects.get(qid=question)
            subjective.content = data.get("content")
            subjective.answer = data.get("answer")
            subjective.save()'''
        return JsonResponse({
            "msg": "试题修改成功 "
        })


# 查询课程相关试题
def chooseQuestion(request):
    if request.method == "GET":
        course = request.GET.get("course")
        cid = ExamCourse.objects.get(name=course).id
        qList = ExamQuestion.objects.filter(cid=cid)
        retList = []
        for question in qList:
            qid = question.id
            if question.type == '1':
                retList.append({
                    "id": qid,
                    "type": "单项选择题",
                    "count": question.count,
                    "content": ExamSimple.objects.get(qid=qid).content
                })
            elif question.type == '2':
                retList.append({
                    "id": qid,
                    "type": "多项选择题",
                    "count": question.count,
                    "content": ExamMultiple.objects.get(qid=qid).content
                })
            elif question.type == '3':
                retList.append({
                    "id": qid,
                    "type": "填空题",
                    "count": question.count,
                    "content": ExamBlank.objects.get(qid=qid).content
                })
            elif question.type == '4':
                retList.append({
                    "id": qid,
                    "type": "判断题",
                    "count": question.count,
                    "content": ExamJudge.objects.get(qid=qid).content
                })
            elif question.type == '5':
                retList.append({
                    "id": qid,
                    "type": "主观题",
                    "count": question.count,
                    "content": ExamSubjective.objects.get(qid=qid).content
                })
        return JsonResponse(retList, safe=False)


# 添加试卷试题
def addPaper(request):
    if request.method == 'POST':
        idList = request.POST.get('idList')
        username = request.POST.get('username')
        papername = request.POST.get('papername')
        course = request.POST.get('course')
        sscore = request.POST.get('sscore')
        scount = request.POST.get('scount')
        mscore = request.POST.get('mscore')
        mcount = request.POST.get('mcount')
        bscore = request.POST.get('bscore')
        bcount = request.POST.get('bcount')
        jscore = request.POST.get('jscore')
        jcount = request.POST.get('jcount')
        sbscore = request.POST.get('sbscore')
        sbcount = request.POST.get('sbcount')
        if scount != '0':
            scount = int(scount)
            sscore = int(sscore)
        if mcount != '0':
            mcount = int(mcount)
            mscore = int(mscore)
        if bcount != '0':
            bcount = int(bcount)
            bscore = int(bscore)
        if jcount != '0':
            jcount = int(jcount)
            jscore = int(jscore)
        if sbcount != '0':
            sbcount = int(sbcount)
            sbscore = int(sbscore)
        list = idList.split(',')
        cid = ExamCourse.objects.get(name=course)
        tid = GetIdByUsername(username)
        cursor.execute("insert into exam_paper(name,tid,qidlist,cid) values \
            (%s,%s,%s,%s);",(papername,tid,list,cid.id))
        cursor.execute("select id from exam_paper where name=%s and tid=%s and cid=%s;",(papername,tid,cid))
        paper = cursor.fetchone()[0]
        #paper = ExamPaper.objects.create(name=papername, tid=User.objects.get(username=username), qidlist=list, cid=cid)
        for id in list:
            question = ExamQuestion.objects.get(id=id)
            score = 0
            if question.type == '1':
                score = sscore
                #ExamPaperScore.objects.create(pid=paper, qid=question, score=score)
            elif question.type == '2':
                score = mscore
                #ExamPaperScore.objects.create(pid=paper, qid=question, score=score)
            elif question.type == '3':
                score = bscore
                #ExamPaperScore.objects.create(pid=paper, qid=question, score=score)
            elif question.type == '4':
                score = jscore
                #ExamPaperScore.objects.create(pid=paper, qid=question, score=score)
            elif question.type == '5':
                score = sbscore
                #ExamPaperScore.objects.create(pid=paper, qid=question, score=score)
            else:
                return JsonResponse({
                    'msg': '添加失败'
                })
            cursor.execute("insert into exam_paper_score(pid,qid,score) values \
                (%s,%s,%s);",(paper,question.id,score))
        return JsonResponse({
            'msg': '试卷添加成功'
        })
    else:
        return JsonResponse({
            'msg': '添加失败'
        })


# 教师试卷查询
def findPaper(request):
    if request.method == "POST":  # 试卷名列表查询
        data = json.loads(request.body)
        username = data.get("username")
        coursename = data.get("course")
        tid = User.objects.get(username=username)
        course = ExamCourse.objects.get(name=coursename)
        paperList = ExamPaper.objects.filter(tid=tid, cid=course)
        nameList = []
        for paper in paperList:
            nameList.append(paper.name)
        return JsonResponse({
            "nameList": nameList
        })
    if request.method == "GET":  # 试卷详细信息查询
        username = request.GET.get("username")
        tid = User.objects.get(username=username).id
        paperList = ExamPaper.objects.filter(tid=tid)
        retList = []
        for paper in paperList:
            retList.append({
                "id": paper.id,
                "course": paper.cid.name,
                "name": paper.name
            })
        return JsonResponse(retList, safe=False)


# 教师发布考试
def addExam(request):
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        course = request.POST.get("course")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        paper = request.POST.get("paper")
        now = datetime.datetime.now()
        new_start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        new_end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        if new_start_time < now:
            return JsonResponse({
                "msg": "开始时间错误"
            })
        elif new_end_time < now:
            return JsonResponse({
                "msg": "截止时间错误"
            })
        elif new_end_time < new_start_time:
            return JsonResponse({
                "msg": "截止时间应晚于开始时间"
            })
        else:
            cursor.execute("insert into exam(name,tid,status,start_time,end_time,cid,pid) \
                values (%s,%s,%s,%s,%s,%s,%s);",(name,GetIdByUsername(username),0,start_time,
                end_time,ExamCourse.objects.get(name=course).id,ExamPaper.objects.get(name=paper).id))
            '''Exam.objects.create(name=name, tid=User.objects.get(username=username), status=0,
                                start_time=start_time, end_time=end_time,
                                cid=ExamCourse.objects.get(name=course), pid=ExamPaper.objects.get(name=paper))'''
            return JsonResponse({
                "msg": "考试发布成功"
            })


# 教师查询考试
def findExam(request):
    if request.method == "GET":  # 教师查询考试信息
        username = request.GET.get("username")
        uid = User.objects.get(username=username)
        examList = Exam.objects.filter(tid=uid)
        retList = []
        now = timezone.now()
        for exam in examList:
            course = ExamCourse.objects.get(id=exam.cid.id)
            s_time = exam.start_time
            e_time = exam.end_time
            status = ''
            if now < s_time:
                status = "未开始"
            elif now > e_time:
                status = "已结束"
                exam.status = "2"
                exam.save()
            else:
                status = "进行中"
            retList.append({
                "id": exam.id,
                "name": exam.name,
                "course": course.name,
                "start_time": exam.start_time.strftime("%Y-%m-%d %H:%M"),
                "end_time": exam.end_time.strftime("%Y-%m-%d %H:%M"),
                "status": status
            })
        return JsonResponse(retList, safe=False)
    if request.method == "POST":  # 教师查询已结束考试名称列表
        data = json.loads(request.body)
        username = data.get("username")
        tid = User.objects.get(username=username)
        examList = Exam.objects.filter(tid=tid)
        nameList = []
        now = timezone.now()
        for exam in examList:
            if exam.end_time < now:
                nameList.append(exam.name)
        return JsonResponse({
            "nameList": nameList
        })


# 教师修改考试
def changeExam(request):
    if request.method == "POST":
        data = json.loads(request.body)
        eid = data.get("eid")
        name = data.get("name")
        s_time = data.get("start_time")
        e_time = data.get("end_time")
        start_time = datetime.datetime.strptime(s_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(e_time, "%Y-%m-%d %H:%M:%S")
        cursor.execute("update exam set name=%s,start_time=%s,end_time=%s \
            where id=%s;",(name,start_time,end_time,int(eid)))
        '''exam = Exam.objects.get(id=int(eid))
        exam.name = name
        exam.start_time = start_time
        exam.end_time = end_time
        exam.save()'''
        return JsonResponse({
            "msg": "考试修改成功"
        })


# 学生查询考试
def selectExam(request):
    if request.method == "GET":
        username = request.GET.get("username")
        uid = User.objects.get(username=username).id
        scclist = StudentChooseCourse.objects.filter(uid=uid)
        retList = []
        now = timezone.now()
        for scc in scclist:
            cid = scc.cid.id
            course = ExamCourse.objects.get(id=cid).name
            examList = Exam.objects.filter(cid=cid)
            for exam in examList:
                tid = exam.tid
                if User.objects.get(id=tid.id).type == "T" or tid.id == uid:
                    s_time = exam.start_time
                    e_time = exam.end_time
                    status = ''
                    if now < s_time:
                        status = "未开始"
                    elif now > e_time:
                        status = "已结束"
                        exam.status = "2"
                        exam.save()
                    else:
                        exam.status = "1"
                        exam.save()
                        status = "进行中"
                    if exam.status == "1":
                        answer = ExamAnswer.objects.filter(eid=exam.id, uid=uid)
                        if len(answer) > 0:
                            status = "已完成"
                    retList.append({
                        'id': exam.id,
                        'course': course,
                        'name': exam.name,
                        'start_time': exam.start_time.strftime("%Y-%m-%d %H:%M"),
                        'end_time': exam.end_time.strftime("%Y-%m-%d %H:%M"),
                        'status': status
                    })
        return JsonResponse(retList, safe=False)


# 学生考试试卷查询
def selectPaper(request):
    if request.method == "POST":
        data = json.loads(request.body)
        eid = data.get("eid")
        pid = Exam.objects.get(id=eid).pid.id
        paper = ExamPaper.objects.get(id=pid)
        qidlist = paper.qidlist
        return JsonResponse({
            'eid': eid,
            'pid': pid,
            'name': paper.name,
            'count': len(qidlist)
        })


# 试卷题目查询
def getQuestion(request):
    if request.method == "GET":
        pid = request.GET.get("pid")
        count = int(request.GET.get("count"))
        paper = ExamPaper.objects.get(id=pid)
        qidList = paper.qidlist
        total = len(qidList)
        qid = qidList[count - 1]
        question = ExamQuestion.objects.get(id=qid)
        score = ExamPaperScore.objects.get(pid=paper, qid=question).score
        if question.type == "1":  # 单选
            simple = ExamSimple.objects.get(qid=qid)
            content = simple.content
            choice1 = simple.choice1
            choice2 = simple.choice2
            choice3 = simple.choice3
            choice4 = simple.choice4
            img = ''
            if simple.picture.name != "":
                img = simple.picture.path
            return JsonResponse({
                'qid': qid,
                'type': question.type,
                'content': content,
                'choice1': choice1,
                'choice2': choice2,
                'choice3': choice3,
                'choice4': choice4,
                'img': img,
                'score': score,
                'total': total,
                'nextcount': count + 1
            })
        elif question.type == "2":  # 多选
            multiple = ExamMultiple.objects.get(qid=qid)
            content = multiple.content
            choice1 = multiple.choice1
            choice2 = multiple.choice2
            choice3 = multiple.choice3
            choice4 = multiple.choice4
            img = ''
            if multiple.picture.name != "":
                img = multiple.picture.path
            return JsonResponse({
                'qid': qid,
                'type': question.type,
                'content': content,
                'choice1': choice1,
                'choice2': choice2,
                'choice3': choice3,
                'choice4': choice4,
                'img': img,
                'score': score,
                'total': total,
                'nextcount': count + 1
            })
        elif question.type == "3":  # 填空
            blank = ExamBlank.objects.get(qid=qid)
            content = blank.content
            img = ''
            if blank.picture.name != "":
                img = blank.picture.path
            return JsonResponse({
                'qid': qid,
                'type': question.type,
                'content': content,
                'img': img,
                'score': score,
                'total': total,
                'nextcount': count + 1
            })
        elif question.type == "4":  # 判断
            judge = ExamJudge.objects.get(qid=qid)
            content = judge.content
            img = ''
            if judge.picture.name != "":
                img = judge.picture.path
            return JsonResponse({
                'qid': qid,
                'type': question.type,
                'content': content,
                'img': img,
                'score': score,
                'total': total,
                'nextcount': count + 1
            })
        elif question.type == "5":  # 主观
            subjective = ExamSubjective.objects.get(qid=qid)
            content = subjective.content
            img = ''
            if subjective.picture.name != "":
                img = subjective.picture.path
            return JsonResponse({
                'qid': qid,
                'type': question.type,
                'content': content,
                'img': img,
                'score': score,
                'total': total,
                'nextcount': count + 1
            })


# 学生答案更新
def updateAnswer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        eid = data.get("eid")
        qid = data.get("qid")
        username = data.get("username")
        uid = User.objects.get(username=username)
        answer = data.get("answer")
        answerList = data.get("answerList")
        if len(answerList) >= 1:
            #qid=ExamQuestion.objects.get(id=qid)
            try:
                old = ExamAnswer.objects.get(qid=ExamQuestion.objects.get(id=qid), eid=Exam.objects.get(id=eid), uid=uid)
                cursor.execute("update exam_answer set answer=%s where id=%s;",(str(answerList),old.id))
                #old.answer = answerList
                #old.save()
            except ExamAnswer.DoesNotExist:
                cursor.execute("insert into exam_answer(qid,eid,uid,answer,score,cloud,is_read) \
                    values (%s,%s,%s,%s,0,'f','f');",(qid,eid,uid.id,str(answerList)))
                #ExamAnswer.objects.create(qid=ExamQuestion.objects.get(id=qid), eid=Exam.objects.get(id=eid), uid=uid,
                #                          answer=answerList)
        else:
            try:
                old = ExamAnswer.objects.get(qid=ExamQuestion.objects.get(id=qid), eid=Exam.objects.get(id=eid), uid=uid)
                cursor.execute("update exam_answer set answer=%s where id=%s;",(answer,old.id))
                #old.answer = answerList
                #old.save()
            except ExamAnswer.DoesNotExist:
                cursor.execute("insert into exam_answer(qid,eid,uid,answer,score,cloud,is_read) values \
                    (%s,%s,%s,%s,0,'f','f');",(qid,eid,uid.id,answer))
        return JsonResponse({
            "msg": "success"
        })


# 学生提交试卷
def checkAnswer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        uid = User.objects.get(username=username)
        eid = data.get("eid")
        exam = Exam.objects.get(id=eid)
        paper = ExamPaper.objects.get(id=exam.pid.id)
        qidList = paper.qidlist
        score = 0
        for qid in qidList:
            question = ExamQuestion.objects.get(id=qid)
            sanswer = ExamAnswer.objects.get(qid=question, uid=uid, eid=exam)
            qscore = ExamPaperScore.objects.get(pid=paper, qid=question).score
            if question.type == '1':
                simple = ExamSimple.objects.get(qid=question)
                if sanswer.answer == simple.answer:
                    score += qscore
                    cursor.execute("update exam_answer set is_right='t',score=%s \
                        where id=%s;",(qscore,sanswer.id))
                    '''sanswer.is_right = True
                    sanswer.score = qscore
                    sanswer.save()'''
                else:
                    cursor.execute("update exam_answer set is_right='f',score=%s \
                        where id=%s;",(0,sanswer.id))
                    '''sanswer.score = 0
                    sanswer.is_right = False
                    sanswer.save()'''
            if question.type == '4':
                judge = ExamJudge.objects.get(qid=question)
                if sanswer.answer == "1":
                    cursor.execute("update exam_answer set answer=%s where id=%s;",
                    ('True',sanswer.id))
                else:
                    cursor.execute("update exam_answer set answer=%s where id=%s;",
                    ('False',sanswer.id))
                if sanswer.answer == judge.answer:
                    score += qscore
                    cursor.execute("update exam_answer set is_right='t',score=%s \
                        where id=%s;",(qscore,sanswer.id))
                else:
                    cursor.execute("update exam_answer set is_right='f',score=%s \
                        where id=%s;",(0,sanswer.id))
            if question.type == '2':
                multiple = ExamMultiple.objects.get(qid=question)
                answer = multiple.answer
                sanswerset = set(sanswer.answer)
                answerset = set(answer)
                if answerset.intersection(sanswerset) == answerset:
                    cursor.execute("update exam_answer set is_right='t',score=%s \
                        where id=%s;",(qscore,sanswer.id))
                    score += qscore
                elif answerset.union(sanswerset):
                    score += (qscore / 2)
                    cursor.execute("update exam_answer set is_right='f',score=%s \
                        where id=%s;",(qscore/2,sanswer.id))
                else:
                    cursor.execute("update exam_answer set is_right='f',score=%s \
                        where id=%s;",(0,sanswer.id))
        cursor.execute("insert into exam_score(eid,uid,obj_score,sub_score,total_score) \
            values (%s,%s,%s,%s,%s);",(exam.id,uid.id,score,0,0))
        #ExamScore.objects.create(eid=exam, uid=uid, obj_score=score)
        return JsonResponse({
            "msg": "success",
            "score": score
        })


#  教师客观题成绩查询
def getScore(request):
    if request.method == "GET":
        examname = request.GET.get("exam")
        exam = Exam.objects.get(name=examname)
        answerList = ExamAnswer.objects.filter(eid=exam)
        stuList = []
        retList = []
        for answer in answerList:
            if answer.uid.id not in stuList:
                stuList.append(answer.uid.id)
        for stu in stuList:
            score = 0
            status = "0"
            total = 0
            stuAnswerList = ExamAnswer.objects.filter(eid=exam, uid=User.objects.get(id=stu))
            for stuAnswer in stuAnswerList:
                question = ExamQuestion.objects.get(id=stuAnswer.qid.id)
                if (question.type == '1') or (question.type == '2') or (question.type == '4'):
                    score += stuAnswer.score
                else:
                    status = "0"
                    total += 1
                    if stuAnswer.score != -1:
                        status = "1"
            retList.append({
                "examname": examname,
                "username": User.objects.get(id=stu).username,
                "score": score,
                "status": status,
                "total": total
            })
        return JsonResponse(retList, safe=False)


#  主观题类查询
def getAnswer(request):
    if request.method == "GET":
        username = request.GET.get("username")
        uid = User.objects.get(username=username)
        examname = request.GET.get("examname")
        exam = Exam.objects.get(name=examname)
        count = int(request.GET.get("count"))
        answerList = ExamAnswer.objects.filter(eid=exam, uid=uid)
        dict = {}
        questionList = []
        for answer in answerList:
            question = ExamQuestion.objects.get(id=answer.qid.id)
            if (question.type == '3') or (question.type == '5'):
                questionList.append(question)
                dict.setdefault(question.id, answer.id)
        questionList.sort(key=lambda x: x.id)
        retQuestion = questionList[count - 1]
        score = ExamPaperScore.objects.get(pid=exam.pid, qid=retQuestion).score
        if retQuestion.type == '3':
            blank = ExamBlank.objects.get(qid=retQuestion)
            return JsonResponse({
                "content": blank.content,
                "score": score,
                "answer": blank.answer,
                "stuanswer": ExamAnswer.objects.get(eid=exam, uid=uid, qid=retQuestion).answer,
                "total": len(questionList),
                "qid": retQuestion.id,
                "count": count,
                "aid": dict.get(retQuestion.id)
            })
        else:
            subjective = ExamSubjective.objects.get(qid=retQuestion)
            return JsonResponse({
                "content": subjective.content,
                "score": score,
                "answer": subjective.answer,
                "stuanswer": ExamAnswer.objects.get(eid=exam, uid=uid, qid=retQuestion).answer,
                "total": len(questionList),
                "qid": retQuestion.id,
                "count": count,
                "aid": dict.get(retQuestion.id)
            })


# 教师上传学生答案至云笔记
def teacherCloud(request):
    if request.method == "POST":
        data = json.loads(request.body)
        teacherName = data.get("teacher")
        studentName = data.get("student")
        aid = data.get("aid")
        teacher = User.objects.get(username=teacherName)
        student = User.objects.get(username=studentName)
        answer = ExamAnswer.objects.get(id=int(aid))
        now = timezone.datetime.now()
        try:
            tc = ExamTeacherCloud.objects.get(tid=teacher, sid=student, aid=answer)
            return JsonResponse({
                "msg": "请勿重复上传"
            })
        except ExamTeacherCloud.DoesNotExist:
            cursor.execute("insert into exam_teacher_cloud(tid,sid,aid,update_time,cloud) \
                values(%s,%s,%s,%s,%s);",(teacher.id,student.id,answer.id,now,True))
            #ExamTeacherCloud.objects.create(tid=teacher, sid=student, aid=answer, update_time=now, cloud=True)
        return JsonResponse({
            "msg": "上传成功，上传时间：" + now.strftime("%Y-%m-%d %H:%M")
        })


# 主观题成绩添加
def addScore(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        examname = data.get("examname")
        qid = int(data.get("qid"))
        score = int(data.get("score"))
        user = User.objects.get(username=username)
        exam = Exam.objects.get(name=examname)
        question = ExamQuestion.objects.get(id=qid)
        allscore = ExamPaperScore.objects.get(pid=exam.pid, qid=question).score
        if score == allscore:
            answer = ExamAnswer.objects.get(eid=exam, uid=user, qid=question)
            answer.is_right = True
        else:
            answer = ExamAnswer.objects.get(eid=exam, uid=user, qid=question)
            answer.is_right = False
        cursor.execute("update exam_answer set score=%s where id=%s;",(score,answer.id))
        #answer.score = score
        #answer.save()
        return JsonResponse({
            "msg": "success"
        })


# 全部成绩添加
def addAllScore(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        examname = data.get("examname")
        eid = Exam.objects.get(name=examname)
        uid = User.objects.get(username=username)
        answerList = ExamAnswer.objects.filter(eid=eid, uid=uid)
        subscore = 0
        for answer in answerList:
            question = ExamQuestion.objects.get(id=answer.qid.id)
            if question.type == "3" or question.type == "5":
                subscore += answer.score
        stu_score = ExamScore.objects.get(uid=uid, eid=eid)
        cursor.execute("update exam_score set sub_score=%s,total_score=%s \
            where id=%s;",(subscore,stu_score.obj_score + subscore,stu_score.id))
        '''stu_score.sub_score = subscore
        stu_score.total_score = stu_score.obj_score + subscore
        stu_score.save()'''
        return JsonResponse({
            "msg": "addscore success"
        })


# 总成绩查询
def getTotalScore(request):
    if request.method == "GET":
        exam = request.GET.get("exam")
        eid = Exam.objects.get(name=exam)
        now = timezone.now()
        if eid.end_time > now:
            return JsonResponse({
                "status": -1
            })
        scoreList = ExamScore.objects.filter(eid=eid)
        retList = []
        for score in scoreList:
            username = User.objects.get(id=score.uid.id).username
            retList.append({
                "username": username,
                "objscore": score.obj_score,
                "subscore": score.sub_score,
                "totalscore": score.total_score
            })
        return JsonResponse(retList, safe=False)


#  教师任课添加
def addCourse(request):
    if request.method == "POST":
        data = json.loads(request.body)
        teacher = data.get("teacher")
        name = data.get("name")
        cursor.execute("insert into exam_course(name,tid,maxnum,status,time) \
            values (%s,%s,%s,%s,%s);",(name,GetIdByUsername(teacher),20,1,0))
        #ExamCourse.objects.create(name=name, tid=User.objects.get(username=teacher))
        return JsonResponse({
            "msg": "success"
        })


# 课程章节添加
def addSection(request):
    if request.method == "POST":
        data = json.loads(request.body)
        course = data.get("course")
        chapterCount = data.get("chapterCount")
        chapterName = data.get("chapterName")
        sectionCount = data.get("sectionCount")
        sectionName = data.get("sectionName")
        cid = ExamCourse.objects.get(name=course)
        section = ExamSection.objects.filter(cid=cid, chapter_count=chapterCount, section_count=sectionCount)
        if len(section) == 1:
            return JsonResponse({
                "msg": "该课程章节已存在，请选择其他章节进行添加"
            })
        else:
            chapters = ExamSection.objects.filter(cid=cid, chapter_count=chapterCount)
            for c in chapters:
                if c.chapter != chapterName:
                    return JsonResponse({
                        "msg": "章节名错误，请保持同一章节的章名相同"
                    })
            cursor.execute("insert into exam_section(cid,chapter_count,chapter,\
                section_count,section) values (%s,%s,%s,%s,%s);",(cid.id,chapterCount,
                chapterName,sectionCount,sectionName))
            #ExamSection.objects.create(cid=cid, chapter_count=chapterCount, chapter=chapterName,
            #                           section_count=sectionCount, section=sectionName)
            return JsonResponse({
                "msg": "课程章节添加成功"
            })


# 学生选课添加
def addSCC(request):
    if request.method == "POST":
        data = json.loads(request.body)
        student = data.get("student")
        course = data.get("course")
        cursor.execute("insert into student_c_course(uid,cid,status) \
            values (%s,%s,%s);",(GetIdByUsername(student),
            ExamCourse.objects.get(name=course).id,1))
        #StudentChooseCourse.objects.create(uid=User.objects.get(username=student),
        #                                   cid=ExamCourse.objects.get(name=course))
        return JsonResponse({
            "msg": "success"
        })


# 教师成绩可视化
def showScore(request):
    if request.method == "GET":
        exam = request.GET.get("exam")
        order = request.GET.get("order")
        eid = Exam.objects.get(name=exam)
        scoreList = []
        retList = []
        if order == "up":
            scoreList = ExamScore.objects.filter(eid=eid).order_by('total_score')
        elif order == "down":
            scoreList = ExamScore.objects.filter(eid=eid).order_by('-total_score')
        else:
            scoreList = ExamScore.objects.filter(eid=eid)
        for score in scoreList:
            username = User.objects.get(id=score.uid.id).username
            retList.append({
                "name": username,
                "score": score.total_score
            })
        return JsonResponse(retList, safe=False)


# 教师题目错误率可视化
def showQuestion(request):
    if request.method == "GET":
        exam = request.GET.get("exam")
        type = request.GET.get("type")
        eid = Exam.objects.get(name=exam)
        qidList = ExamPaper.objects.get(id=eid.pid.id).qidlist
        count = 1
        retList = []
        for qid in qidList:
            right = 0
            wrong = 0
            answerList = ExamAnswer.objects.filter(eid=eid, qid=ExamQuestion.objects.get(id=qid))
            for answer in answerList:
                if answer.is_right:
                    right += 1
                else:
                    wrong += 1
            if type == "1":
                retList.append({
                    "count": "第" + str(count) + "题",
                    "right": right,
                    "wrong": -wrong
                })
            else:
                retList.append({
                    "count": "第" + str(count) + "题",
                    "percentage": int((right / (right + wrong)) * 100)
                })
            count += 1
        return JsonResponse(retList, safe=False)


# 学生课程成绩可视化
def showStudentScore(request):
    if request.method == "GET":
        username = request.GET.get("username")
        course = request.GET.get("course")
        uid = User.objects.get(username=username)
        cid = ExamCourse.objects.get(name=course)
        eList = Exam.objects.filter(cid=cid)
        examList = []
        retList = []
        now = timezone.now()
        for exam in eList:
            if exam.end_time < now:
                examList.append(exam)
        examList.sort(key=lambda x: x.end_time)
        for exam in examList:
            tid = exam.tid
            if User.objects.get(id=tid.id).type == "T":
                try:
                    score = ExamScore.objects.get(uid=uid, eid=exam)
                    retList.append({
                        "name": exam.name,
                        "score": score.obj_score + score.sub_score
                    })
                except ExamScore.DoesNotExist:
                    retList = retList
        return JsonResponse(retList, safe=False)


# 学生成绩查询
def getStudentScore(request):
    if request.method == "GET":
        username = request.GET.get("username")
        uid = User.objects.get(username=username)
        scoreList = ExamScore.objects.filter(uid=uid)
        retList = []
        now = timezone.now()
        for score in scoreList:
            exam = Exam.objects.get(id=score.eid.id)
            if exam.end_time < now:
                retList.append({
                    "exam": exam.name,
                    "course": exam.cid.name,
                    "obj_score": score.obj_score,
                    "sub_score": score.sub_score,
                    "total_score": score.obj_score + score.sub_score
                })
        return JsonResponse(retList, safe=False)


# 学生考试查询
def findStuExam(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        uid = User.objects.get(username=username).id
        scclist = StudentChooseCourse.objects.filter(uid=uid)
        nameList = []
        now = timezone.now()
        for scc in scclist:
            cid = scc.cid.id
            examList = Exam.objects.filter(cid=cid)
            for exam in examList:
                if exam.end_time < now:
                    tid = exam.tid
                    if User.objects.get(id=tid.id).type == "T" or tid.id == uid:
                        nameList.append(exam.name)
        return JsonResponse({
            "nameList": nameList
        })


# 学生错题查询
def getWrong(request):
    if request.method == "GET":
        exam = request.GET.get("exam")
        username = request.GET.get("username")
        uid = User.objects.get(username=username)
        eid = Exam.objects.get(name=exam)
        answerList = ExamAnswer.objects.filter(eid=eid, uid=uid)
        retList = []
        for answer in answerList:
            if answer.is_right is not True:
                stu_answer = answer.answer
                question = ExamQuestion.objects.get(id=answer.qid.id)
                content = ''
                right_answer = ''
                if question.type == "1":
                    simple = ExamSimple.objects.get(qid=question)
                    content = simple.content
                    right_answer = simple.answer
                    if right_answer == "1":
                        right_answer = "A"
                    elif right_answer == "2":
                        right_answer = "B"
                    elif right_answer == "3":
                        right_answer = "C"
                    else:
                        right_answer = "D"
                    if stu_answer == "1":
                        stu_answer = "A"
                    elif stu_answer == "2":
                        stu_answer = "B"
                    elif stu_answer == "3":
                        stu_answer = "C"
                    else:
                        stu_answer = "D"
                elif question.type == "2":
                    multiple = ExamMultiple.objects.get(qid=question)
                    content = multiple.content
                    right_answer = multiple.answer
                    retanswer = []
                    for sa in stu_answer:
                        if sa == "A" or sa == "B" or sa == "C" or sa == "D":
                            retanswer.append(sa)
                    retanswer.sort()
                    stu_answer = retanswer
                elif question.type == "3":
                    blank = ExamBlank.objects.get(qid=question)
                    content = blank.content
                    right_answer = blank.answer
                elif question.type == "4":
                    judge = ExamJudge.objects.get(qid=question)
                    content = judge.content
                    if not judge.answer:
                        right_answer = "错误"
                    else:
                        right_answer = "正确"
                    if stu_answer == "False":
                        stu_answer = "错误"
                    else:
                        stu_answer = "正确"
                elif question.type == "5":
                    subjective = ExamSubjective.objects.get(qid=question)
                    content = subjective.content
                    right_answer = subjective.answer
                retList.append({
                    "id": answer.id,
                    "content": content,
                    "answer": right_answer,
                    "stu_answer": stu_answer
                })
        return JsonResponse(retList, safe=False)


# 错题上传云笔记
def goToCloud(request):
    if request.method == "POST":
        data = json.loads(request.body)
        aid = data.get("id")
        answer = ExamAnswer.objects.get(id=int(aid))
        if answer.cloud:
            return JsonResponse({
                "msg": "已上传，请勿重复上传"
            })
        answer.cloud = True
        now = timezone.now()
        cursor.execute("update exam_answer set cloud='t',update_time=%s \
            where id=%s;",(now,answer.id))
        #answer.update_time = now
        #answer.save()
        return JsonResponse({
            "msg": "上传成功，上传时间：" + str(now)
        })


# 课程章节查询
def getSection(request):
    if request.method == "GET":
        course = request.GET.get("course")
        cid = ExamCourse.objects.get(name=course)
        sectionList = ExamSection.objects.filter(cid=cid)
        retList = []
        chapterList = []
        for section in sectionList:
            if chapterList.count(section.chapter_count) == 0:
                chapterList.append(section.chapter_count)
        chapterList.sort()
        for chapter in chapterList:
            sections = ExamSection.objects.filter(cid=cid, chapter_count=chapter)
            for section in sections:
                retList.append({
                    "id": section.id,
                    "chapter": "第" + str(section.chapter_count) + "章：" + section.chapter,
                    "section": "第" + str(section.section_count) + "节：" + section.section
                })
        return JsonResponse(retList, safe=False)


# 课程章查询
def findChapter(request):
    if request.method == "POST":
        data = json.loads(request.body)
        coursename = data.get("course")
        cid = ExamCourse.objects.get(name=coursename)
        sections = ExamSection.objects.filter(cid=cid)
        dict = {}
        for section in sections:
            dict.setdefault(str(section.chapter_count), section.chapter)
        chapterOption = []
        for key in dict:
            chapterOption.append({
                "value": key,
                "label": dict.get(key)
            })
        return JsonResponse({
            "chapteroption": chapterOption
        })


# 课程节查询
def findSection(request):
    if request.method == "POST":
        data = json.loads(request.body)
        coursename = data.get("course")
        chapter = data.get("chapter")
        cid = ExamCourse.objects.get(name=coursename)
        sectionList = ExamSection.objects.filter(cid=cid, chapter_count=int(chapter))
        dict = {}
        for section in sectionList:
            dict.setdefault(str(section.section_count), section.section)
            sectionOption = []
        for key in dict:
            sectionOption.append({
                "value": key,
                "label": dict.get(key)
            })
        return JsonResponse({
            "sectionoption": sectionOption
        })


# 学生课程查询
def getStuCourse(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        uid = User.objects.get(username=username)
        sccList = StudentChooseCourse.objects.filter(uid=uid)
        nameList = []
        for scc in sccList:
            course = ExamCourse.objects.get(id=scc.cid.id)
            nameList.append(course.name)
        return JsonResponse({
            "nameList": nameList
        })


# 学生测验添加
def addTest(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        count = int(data.get("count"))
        course = data.get("course")
        uid = User.objects.get(username=username)
        cid = ExamCourse.objects.get(name=course)
        paperList = ExamPaper.objects.filter(cid=cid)
        qidList = []
        for paper in paperList:
            for qid in paper.qidlist:
                question = ExamQuestion.objects.get(id=qid)
                if question.type == "1" or question.type == "2" or question.type == "4":
                    if qidList.count(qid) == 0:
                        qidList.append(qid)
        qidListForTest = []
        while len(qidListForTest) < count:
            temp = random.randint(0, len(qidList) - 1)
            if qidListForTest.count(qidList[temp]) == 0:
                qidListForTest.append(qidList[temp])
        now = timezone.now()
        paperName = cid.name + "测验试卷" + now.strftime("%Y-%m-%d %H:%M:%S")
        examName = cid.name + "测验考试" + now.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("insert into exam_paper(name,qidlist,tid,cid) values \
            (%s,%s,%s,%s);",(paperName,qidListForTest,uid.id,cid.id))
        cursor.execute("select id from exam_paper where name=%s and tid=%s \
            and cid=%s;",(paperName,uid.id,cid.id))
        paper = cursor.fetchone()[0]
        #paper = ExamPaper.objects.create(name=paperName, qidlist=qidListForTest, tid=uid, cid=cid)
        for qid in qidListForTest:
            cursor.execute("insert into exam_paper_score(pid,qid,score) values \
                (%s,%s,%s);",(paper,ExamQuestion.objects.get(id=qid).id,10))
            #ExamPaperScore.objects.create(pid=paper, qid=ExamQuestion.objects.get(id=qid), score=10)
        delta = datetime.timedelta(days=1)
        cursor.execute("insert into exam(name,cid,pid,tid,start_time,end_time,status) \
            values (%s,%s,%s,%s,%s,%s,%s);",(examName,cid.id,paper,uid.id,now,now+delta,1))
        #Exam.objects.create(name=examName, cid=cid, pid=paper, tid=uid, start_time=now, end_time=now + delta, status=1)
        return JsonResponse({
            "msg": "success"
        })


# ************************************以下为自动组卷算法处理************************************
# *************************************主要思路为遗传算法*************************************
# 教师组卷主方法
def autoPaper(request):
    if request.method == "POST":
        print('autopaper')
        def strgetnum(s):
            if s == '':
                return 0
            else:
                return int(s)
        data = json.loads(request.body)
        papername = data.get("papername")
        sectionList = data.get("sectionoption")
        coursename = data.get("course")
        count = data.get("count")
        username = data.get("username")
        scount = data.get("simplecount")
        sscore = data.get("simplescore")
        mcount = data.get("multiplecount")
        mscore = data.get("multiplescore")
        bcount = data.get("blankcount")
        bscore = data.get("blankscore")
        jcount = data.get("judgecount")
        jscore = data.get("judgescore")
        sbcount = data.get("subjectivecount")
        sbscore = data.get("subjectivescore")
        digitlist =[ strgetnum(i) for i in [count,scount,sscore,mcount,mscore,bcount,bscore,jcount,jscore,sbcount,sbscore]]
        count,scount,sscore,mcount,mscore,bcount,bscore,jcount,jscore,sbcount,sbscore = digitlist
        print('data get')
        Ecount = int(count) / 100
        EFitness = 0.98  # 适应度期望值
        course = ExamCourse.objects.get(name=coursename)
        autoPaper = AutoPaper(scount, sscore, mcount, mscore, bcount, bscore, jcount, jscore, sbcount, sbscore)
        autoPaperList = initPapers(20, course, autoPaper)  # 种群初始数量设为20
        print('init finished')
        for autoPaper in autoPaperList:  # 计算适应度，并写入autoPaper的paperFitness
            autoPaper.paperFitness = fitness(sectionList, Ecount, course, autoPaper)
            if autoPaper.paperFitness >= EFitness:  # 判断是否有个体符合期望
                addPaperToDB(autoPaper, papername, username, course)
                print('return 0')
                return JsonResponse({
                    "msg": "添加成功",
                    "status": "初始化获得的试卷个体"
                })
        print('calculate finished')
        print('len(autoPaperlist):%d' % (len(autoPaperList)))
        i = 0
        while i < 10:  # 最大迭代次数10
            autoPaperList = choose(autoPaperList)  # 选择
            print("choose fin")
            print('len(autoPaperlist):%d' % (len(autoPaperList)))
            autoPaperList = exchange(autoPaperList)  # 交叉
            print("exchange fin")
            print('len(autoPaperlist):%d' % (len(autoPaperList)))
            print('turn %d' % i )
            for autoPaper in autoPaperList:  # 计算适应度，更改autoPaper的paperFitness
                autoPaper.paperFitness = fitness(sectionList, Ecount, course, autoPaper)
                if autoPaper.paperFitness >= EFitness:  # 判断是否有个体符合期望
                    addPaperToDB(autoPaper, papername, username, course)
                    print('return 1')
                    return JsonResponse({
                        "msg": "添加成功",
                        "status": "交叉后获得的试卷个体"
                    })
            print('len(autoPaperlist):%d' % (len(autoPaperList)))
            autoPaperList = change(autoPaperList)  # 变异
            for autoPaper in autoPaperList:  # 计算适应度，并写入autoPaper的paperFitness
                autoPaper.paperFitness = fitness(sectionList, Ecount, course, autoPaper)
                if autoPaper.paperFitness >= EFitness:  # 判断是否有个体符合期望
                    addPaperToDB(autoPaper, papername, username, course)
                    print('return 2')
                    return JsonResponse({
                        "msg": "添加成功",
                        "status": "变异后获得的试卷个体"
                    })
            i = i + 1
        maxFitness = -9999.0
        print('iter finished')
        for autoPaper in autoPaperList:  # 计算适应度
            autoPaper.paperFitness = fitness(sectionList, Ecount, course, autoPaper)
            if autoPaper.paperFitness > maxFitness:
                maxFitness = autoPaper.paperFitness
        print('final calc finished, maxfintness:%d' % maxFitness)
        for autoPaper in autoPaperList:
            if autoPaper.paperFitness == maxFitness:
                addPaperToDB(autoPaper, papername, username, course)
                print('return 3')
                return JsonResponse({
                    "msg": "添加成功",
                    "status": "达到最大迭代次数的试卷个体"
                })
        print('return 4')
        return JsonResponse({
            "msg": "出现错误"
        })


# 辅助试卷类
class AutoPaper:
    qidList = []
    scount = 0
    sscore = 0
    mcount = 0
    mscore = 0
    bcount = 0
    bscore = 0
    jcount = 0
    jscore = 0
    sbcount = 0
    sbscore = 0
    paperFitness = 0.0

    def __init__(self, scount, sscore, mcount, mscore, bcount, bscore, jcount, jscore, sbcount, sbscore):
        self.scount = scount
        self.sscore = sscore
        self.mcount = mcount
        self.mscore = mscore
        self.bcount = bcount
        self.bscore = bscore
        self.jcount = jcount
        self.jscore = jscore
        self.sbcount = sbcount
        self.sbscore = sbscore


# 生成初始种群
def initPapers(count, course, autoPaper):
    """

    :param count:  初始种群个体数量
    :param course: 课程对象
    :param autoPaper: 试卷个体
    :return: AutoPaper对象的列表
    """
    autoPaperList = []
    for i in range(count):
        tempPaper = AutoPaper(autoPaper.scount, autoPaper.sscore, autoPaper.mcount, autoPaper.mscore, autoPaper.bcount,
                              autoPaper.bscore, autoPaper.jcount, autoPaper.jscore, autoPaper.sbcount, autoPaper.sbscore)
        autoPaperList.append(initAPaper(course, tempPaper))
    return autoPaperList


# 生成一张符合要求的试卷
def initAPaper(course, autoPaper):
    questionList = ExamQuestion.objects.filter(cid=course)
    sListForPaper = []  # 选入试卷单选列表
    mListForPaper = []  # 选入试卷多选列表
    bListForPaper = []  # 选入试卷填空列表
    jListForPaper = []  # 选入试卷判断列表
    sbListForPaper = []  # 选入试卷主观列表
    squestionList = []  # 课程所有单选列表
    mquestionList = []  # 课程所有多选列表
    bquestionList = []  # 课程所有填空列表
    jquestionList = []  # 课程所有判断列表
    sbquestionList = []  # 课程所有主观列表
    for question in questionList:
        if question.type == "1":
            squestionList.append(question.id)
        if question.type == "2":
            mquestionList.append(question.id)
        if question.type == "3":
            bquestionList.append(question.id)
        if question.type == "4":
            jquestionList.append(question.id)
        if question.type == "5":
            sbquestionList.append(question.id)
    randomList(squestionList, sListForPaper, autoPaper.scount)
    randomList(mquestionList, mListForPaper, autoPaper.mcount)
    randomList(bquestionList, bListForPaper, autoPaper.bcount)
    randomList(jquestionList, jListForPaper, autoPaper.jcount)
    randomList(sbquestionList, sbListForPaper, autoPaper.sbcount)
    idList = sListForPaper + mListForPaper + bListForPaper + jListForPaper + sbListForPaper
    autoPaper.qidList = idList
    return autoPaper


# 生成一个不重复的试题编号的随机列表
def randomList(questionList, randlist, length):
    """

    :param questionList: 全部试题编号列表
    :param randlist: 生成的列表
    :param length: 生成列表长度
    """
    count = len(questionList)
    while len(randlist) < length:
        temp = random.randint(0, count - 1)
        if randlist.count(questionList[temp]) == 0:
            randlist.append(questionList[temp])


# 适应度函数
def fitness(EsectionList, Ecount, cid, autoPaper):
    """

    :param EsectionList: 期望的课程章节列表
    :param Ecount: 期望的难度系数
    :param qidList: 试卷的题目列表
    :param cid: 相关课程id
    :param autoPaper: 试卷个体
    :return: 个体适应度（最大为1）
    """
    sectionList = []
    ncount = 0.0
    qidList = autoPaper.qidList
    for qid in qidList:
        question = ExamQuestion.objects.get(id=qid)
        chapter = question.chapter
        section = question.section
        foundsection = ExamSection.objects.get(cid=cid, chapter_count=chapter, section_count=section)
        if sectionList.count(foundsection.id) == 0:
            sectionList.append(foundsection.id)
        count = question.count
        if question.type == "1":
            ncount = autoPaper.sscore * getCount(count) + ncount
        elif question.type == "2":
            ncount = autoPaper.mscore * getCount(count) + ncount
        elif question.type == "3":
            ncount = autoPaper.bscore * getCount(count) + ncount
        elif question.type == "4":
            ncount = autoPaper.jscore * getCount(count) + ncount
        elif question.type == "5":
            ncount = autoPaper.sbscore * getCount(count) + ncount
    sumscore = autoPaper.sscore * autoPaper.scount + autoPaper.mscore * autoPaper.mcount + autoPaper.bscore * \
               autoPaper.bcount + autoPaper.jscore * autoPaper.jcount + autoPaper.sbscore * autoPaper.sbcount
    nratio = abs(Ecount - (ncount / sumscore))  # 难度系数相关系数
    scount = 0.0
    for sid in sectionList:
        for esid in EsectionList:
            if esid == sid:
                scount += 1.0
    sratio = 1 - scount / len(EsectionList)  # 课程章节相关度系数
    return 1 - (sratio + nratio)


# 选择(轮盘赌选择)
def choose(autoPaperList):
    """

    :param autoPaperList: 种群
    :return: 选择后的种群，大小为原先的一半
    """
    '''selectList = []
    sumFitness = 0.0
    for autoPaper in autoPaperList:
        sumFitness += autoPaper.paperFitness
    while len(selectList) <= (len(autoPaperList) / 2):
        degree = 0.0
        randDegree = random.randint(1, 10) * 0.1 * sumFitness
        print("randDegree:%d" % randDegree)
        for autoPaper in autoPaperList:
            degree += autoPaper.paperFitness
            print("degree:%d" % degree)
            if degree >= randDegree:
                if selectList.count(autoPaper) == 0:
                    selectList.append(autoPaper)
                break'''
    selectList = sorted(autoPaperList, key=lambda x:x.paperFitness,reverse=True)
    print([i.paperFitness for i in selectList])
    return selectList[:len(selectList)//2+1]


# 交叉
def exchange(autoPaperList):
    count = len(autoPaperList) * 2
    exchangeList = []
    while len(exchangeList) <= count:
        index1 = random.randint(0, len(autoPaperList) - 1)
        index2 = random.randint(0, len(autoPaperList) - 1)
        if index1 != index2:
            autoPaper1 = autoPaperList[index1]
            autoPaper2 = autoPaperList[index2]
            newAutoPaper1 = AutoPaper(autoPaper1.scount, autoPaper1.sscore, autoPaper1.mcount,
                                      autoPaper1.mscore, autoPaper1.bcount, autoPaper1.bscore,
                                      autoPaper1.jcount, autoPaper1.jscore, autoPaper1.sbcount,
                                      autoPaper1.sbscore)
            newAutoPaper1.qidList = []
            for qid in autoPaper1.qidList:
                newAutoPaper1.qidList.append(qid)
            newAutoPaper2 = AutoPaper(autoPaper2.scount, autoPaper2.sscore, autoPaper2.mcount,
                                      autoPaper2.mscore, autoPaper2.bcount, autoPaper2.bscore,
                                      autoPaper2.jcount, autoPaper2.jscore, autoPaper2.sbcount,
                                      autoPaper2.sbscore)
            newAutoPaper2.qidList = []
            for qid in autoPaper2.qidList:
                newAutoPaper2.qidList.append(qid)
            if autoPaper1.scount != 0:
                temp = random.randint(0, autoPaper1.scount - 1)
                ex = newAutoPaper1.qidList[temp]
                newAutoPaper1.qidList[temp] = newAutoPaper2.qidList[temp]
                newAutoPaper2.qidList[temp] = ex
            if autoPaper1.mcount != 0:
                temp = random.randint(autoPaper1.scount,
                                      autoPaper1.scount + autoPaper1.mcount - 1)
                ex = newAutoPaper1.qidList[temp]
                newAutoPaper1.qidList[temp] = newAutoPaper2.qidList[temp]
                newAutoPaper2.qidList[temp] = ex
            if autoPaper1.bcount != 0:
                temp = random.randint(autoPaper1.scount + autoPaper1.mcount,
                                      autoPaper1.scount + autoPaper1.mcount + autoPaper1.bcount - 1)
                ex = newAutoPaper1.qidList[temp]
                newAutoPaper1.qidList[temp] = newAutoPaper2.qidList[temp]
                newAutoPaper2.qidList[temp] = ex
            if autoPaper1.jcount != 0:
                temp = random.randint(autoPaper1.scount + autoPaper1.mcount + autoPaper1.bcount,
                                      autoPaper1.scount + autoPaper1.mcount + autoPaper1.bcount + autoPaper1.jcount - 1)
                ex = newAutoPaper1.qidList[temp]
                newAutoPaper1.qidList[temp] = newAutoPaper2.qidList[temp]
                newAutoPaper2.qidList[temp] = ex
            if autoPaper1.sbcount != 0:
                temp = random.randint(autoPaper1.scount + autoPaper1.mcount + autoPaper1.bcount + autoPaper1.jcount,
                                      autoPaper1.scount + autoPaper1.mcount + autoPaper1.bcount + autoPaper1.jcount
                                      + autoPaper1.sbcount - 1)
                ex = newAutoPaper1.qidList[temp]
                newAutoPaper1.qidList[temp] = newAutoPaper2.qidList[temp]
                newAutoPaper2.qidList[temp] = ex
            same1 = False
            same2 = False
            for paper in exchangeList:
                if newAutoPaper1.qidList == paper.qidList:
                    same1 = True
                    break
                if newAutoPaper2.qidList == paper.qidList:
                    same2 = True
                    break
            for qid in newAutoPaper1.qidList:
                if newAutoPaper1.qidList.count(qid) != 1:
                    same1 = True
                    break
            for qid in newAutoPaper2.qidList:
                if newAutoPaper2.qidList.count(qid) != 1:
                    same2 = True
                    break
            if not same1:
                exchangeList.append(newAutoPaper1)
            if not same2:
                exchangeList.append(newAutoPaper2)
    return exchangeList


# 变异
def change(autoPaperList):
    index1 = random.randint(0, len(autoPaperList) - 1)
    autoPaper = autoPaperList[index1]
    index2 = random.randint(0, len(autoPaper.qidList) - 1)
    qid = autoPaper.qidList[index2]
    question = ExamQuestion.objects.get(id=qid)
    newQuestionList = ExamQuestion.objects.filter(cid=question.cid, type=question.type,
                                                  chapter=question.chapter, section=question.section)
    index3 = random.randint(0, len(newQuestionList) - 1)
    autoPaperList[index1].qidList[index2] = newQuestionList[index3].id
    return autoPaperList


# 将试卷添加进数据库
def addPaperToDB(autoPaper, papername, username, course):
    tid = GetIdByUsername(username)
    cursor.execute("insert into exam_paper(name,tid,cid,qidlist) values \
        (%s,%s,%s,%s);",(papername,tid,course.id,autoPaper.qidList))
    cursor.execute("select id from exam_paper where name=%s and tid=%s and cid=%s;",
    (papername,tid,course.id))
    paper = cursor.fetchone()[0]
    #paper = ExamPaper.objects.create(name=papername, tid=User.objects.get(username=username), cid=course, qidlist=autoPaper.qidList)
    for qid in autoPaper.qidList:
        question = ExamQuestion.objects.get(id=qid)
        if question.type == '1':
            cursor.execute("insert into exam_paper_score(pid,qid,score) values \
                (%s,%s,%s);",(paper,question.id,autoPaper.sscore))
            #ExamPaperScore.objects.create(pid=paper, qid=question, score=autoPaper.sscore)
        elif question.type == '2':
            cursor.execute("insert into exam_paper_score(pid,qid,score) values \
                (%s,%s,%s);",(paper,question.id,autoPaper.mscore))
            #ExamPaperScore.objects.create(pid=paper, qid=question, score=autoPaper.mscore)
        elif question.type == '3':
            cursor.execute("insert into exam_paper_score(pid,qid,score) values \
                (%s,%s,%s);",(paper,question.id,autoPaper.bscore))
            #ExamPaperScore.objects.create(pid=paper, qid=question, score=autoPaper.bscore)
        elif question.type == '4':
            cursor.execute("insert into exam_paper_score(pid,qid,score) values \
                (%s,%s,%s);",(paper,question.id,autoPaper.jscore))
            #ExamPaperScore.objects.create(pid=paper, qid=question, score=autoPaper.jscore)
        elif question.type == '5':
            cursor.execute("insert into exam_paper_score(pid,qid,score) values \
                (%s,%s,%s);",(paper,question.id,autoPaper.sbscore))
            #ExamPaperScore.objects.create(pid=paper, qid=question, score=autoPaper.sbscore)
    print("addpapertodb fin")


# 难度系数对照
def getCount(i):
    if i == 1:
        return 1.0
    elif i == 2:
        return 0.8
    elif i == 3:
        return 0.5
    elif i == 4:
        return 0.3
    elif i == 5:
        return 0.1
    else:
        return 0
