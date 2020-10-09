import itertools
import os
import uuid
import cv2
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.utils import timezone
import base64
import re
import jieba
import jieba.posseg as pseg
import Levenshtein
import zipfile
from OnlineEducation.settings import BASE_DIR
from IAsystem.aescrypt import AESUtil
from backend.models import *

from django.db import connection,transaction

cursor = connection.cursor()

# 用户获取
def get_user(request):
    response = {}
    try:
        user_id = request.POST.get('user_id')
        user = User.objects.filter(id=user_id).values()
        if user:
            response['user'] = list(user)
            response['msg'] = '查询成功'
            response['code'] = 1
        return JsonResponse(response)
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = 0
    return JsonResponse(response)


# 头像获取
def get_avatar(request):
    try:
        user_id = request.COOKIES.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if user:
            image_path ="media/"+str(user.user_avatar)
            image = open(image_path, "rb")
        return HttpResponse(image, content_type="image/jpeg;image/png")
    except Exception as e:
        image = open("media/avatar/default.png", "rb")
    return HttpResponse(image, content_type="image/jpeg;image/png")


# 科目获取
def get_subject(request):
    response = {}
    try:
        subject_list = Subject.objects.all().values()
        response['subjects'] = list(subject_list)
        response['code'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = 0
    return JsonResponse(response)


def get_major(request):
    response = {}
    try:
        major_list = Major.objects.all().values()
        majors = list(major_list)
        for major in majors:
            major_obj = Major.objects.get(major_id=major['major_id'])
            subjects = Subject.objects.filter(major=major_obj).values()
            subjectList = list(subjects)
            major['subjectList'] = subjectList
        response['majors'] = majors
        response['code'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = 0
    return JsonResponse(response)


# 登录
def post_login(request):
    from django.contrib.auth.hashers import make_password, check_password
    response = {}
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        user1 = User.objects.get(username=username)
        if check_password(password, user1.password):
            response['code'] = 1
            response['id'] = user1.id
            response['username'] = user1.username
            response['type'] = user1.type
            return JsonResponse(response)
        response['code'] = 2
    except Exception as e:
        try:
            user2 = User.objects.get(email=username)
            if check_password(password, user2.password):
                response['code'] = 1
                response['id'] = user2.id
                response['username'] = user2.username
                response['type'] = user2.type
                return JsonResponse(response)
            response['code'] = 2
        except Exception as e:
            response['code'] = 3
    return JsonResponse(response)


# 注册
def register(request):
    from django.contrib.auth.hashers import make_password
    response = {}
    try:
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user1 = User.objects.get(username=username)
            response['code'] = 2
        except Exception as e1:
            try:
                user2 = User.objects.get(email=email)
                response['code'] = 3
            except Exception as e2:
                gender = request.POST.get('gender')
                raw_password = request.POST.get('password')
                password = make_password(raw_password)
                type = request.POST.get('type')
                user_obj = User(username=username, user_gender=gender, email=email, password=password, type=type)
                user_obj.save()
                response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


# 搜索
def search(request):
    response = {}
    src = []  # 存储分词结果集
    index_list = []  # 存储序号
    src_dict = {}  # 存储关键字组合序列
    base_records = []  # 记录放入结果集的基本问题id
    question_records = []  # 记录放入结果集的活动问题id
    request_records = []  # 记录放入结果集的需求id
    sorted_base_list = []  # 存储基本问题搜索结果
    sorted_question_list = []  # 存储活动问题搜索结果
    sorted_request_list = []  # 存储需求搜索结果
    patterns = []  # 存储匹配模式
    try:
        type = request.POST.get('type')
        keyword = request.POST.get('keyword')
        # 分词
        words = pseg.cut(keyword)
        # 获取名词或英文
        for w in words:
            if w.flag == 'n' or w.flag == 'eng' or w.flag == 'v':
                if w.flag == 'eng':
                    src.append(str(w.word).lower())
                else:
                    src.append(w.word)

        # 获得组合模式
        for i in range(len(src)):
            index_list.append(i)
            src_dict[i] = src[i]
        for i in range(1, len(src) + 1):
            iter = itertools.permutations(index_list, i)
            com_list = list(iter)
            for index in com_list:
                context = ''
                for item in index:
                    context += "(" + src_dict.get(item) + ")+.*"
                patterns.append(context)
        # 基本库查询
        if type == '0':
            base_question_obj = Base_question.objects.all().values()
        else:
            base_question_obj = Base_question.objects.filter(subject_id=type).values()
        if base_question_obj:
            base_questions = list(base_question_obj)
            for pattern in reversed(patterns):
                base_list = []
                base_distance_dict = {}
                for question in base_questions:
                    if re.search(r'' + pattern, str(question['description']).lower()):
                        if not question['base_question_id'] in base_records:
                            subject_obj = Subject.objects.get(subject_id=question['subject_id'])
                            question['subject'] = subject_obj.subject_name
                            base_list.append(question)
                            base_records.append(question['base_question_id'])
                for item in base_list:
                    distance = Levenshtein.distance(item['description'], keyword)
                    if distance in base_distance_dict.keys():
                        new_distance = distance + 1
                        base_distance_dict[new_distance] = item
                    else:
                        base_distance_dict[distance] = item
                for item in sorted(base_distance_dict.keys(), reverse=False):
                    sorted_base_list.append(base_distance_dict.get(item))
        response['base_questions'] = sorted_base_list
        # 活跃库查询
        if type == '0':
            question_obj = Question.objects.exclude(status=3).values()
        else:
            question_obj = Question.objects.filter(subject_id=type, status__exact=3).values()
        if question_obj:
            questions = list(question_obj)
            for pattern in reversed(patterns):
                question_list = []
                question_distance_dict = {}
                for question in questions:
                    if re.search(r'' + pattern, str(question['context']).lower()):
                        if not question['question_id'] in question_records:
                            subject_obj = Subject.objects.get(subject_id=question['subject_id'])
                            question['subject'] = subject_obj.subject_name
                            user = User.objects.get(id=question['user_id'])
                            question['username'] = user.username
                            path1 = 'media/'+ str(user.user_avatar)
                            image = cv2.imread(path1)
                            if path1.find('.jpg'):
                                avatar = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
                            else:
                                avatar = base64.b64encode(cv2.imencode('.png', image)[1]).decode()
                            question['avatar'] = avatar
                            question_obj = Question.objects.get(question_id=question['question_id'])
                            answer_obj = question_obj.answer_set.all().values().order_by('-score').order_by(
                                '-time').first()
                            answer = {}
                            if answer_obj:
                                answer['score'] = answer_obj['score']
                                answer['status'] = answer_obj['status']
                                answer['from_forum'] = answer_obj['from_forum']
                                answer['context'] = answer_obj['context']
                                user = User.objects.get(id=answer_obj['user_id'])
                                answer['username'] = user.username
                                path2 = 'media/'+ str(user.user_avatar)
                                image = cv2.imread(path2)
                                if path2.find('.jpg'):
                                    avatar = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
                                else:
                                    avatar = base64.b64encode(cv2.imencode('.png', image)[1]).decode()
                                answer['avatar'] = avatar
                            question['answer'] = answer
                            question_list.append(question)
                            question_records.append(question['question_id'])
                for item in question_list:
                    distance = Levenshtein.distance(keyword, item['context'])
                    if distance in question_distance_dict.keys():
                        new_distance = distance + 1
                        question_distance_dict[new_distance] = item
                    else:
                        question_distance_dict[distance] = item
                for item in sorted(question_distance_dict.keys(), reverse=False):
                    sorted_question_list.append(question_distance_dict.get(item))
        response['active_questions'] = sorted_question_list
        # 资源库查询
        if type == '0':
            request_obj = Request.objects.all().values()
        else:
            request_obj = Request.objects.filter(subject_id=type).values()
        if request_obj:
            requests = list(request_obj)
            for pattern in reversed(patterns):
                request_list = []
                request_distance_dict = {}
                for sub_request in requests:
                    if re.search(r'' + pattern, str(sub_request['context']).lower()):
                        if not sub_request['request_id'] in request_records:
                            subject_obj = Subject.objects.get(subject_id=sub_request['subject_id'])
                            sub_request['subject'] = subject_obj.subject_name
                            user = User.objects.get(id=sub_request['user_id'])
                            sub_request['username'] = user.username
                            path2 = 'media/'+ str(user.user_avatar)
                            image = cv2.imread(path2)
                            if path2.find('.jpg'):
                                avatar = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
                            else:
                                avatar = base64.b64encode(cv2.imencode('.png', image)[1]).decode()
                            sub_request['avatar'] = avatar
                            request_obj = Request.objects.get(request_id=sub_request['request_id'])
                            resource_obj = request_obj.resource_set.all().values().order_by('-number').order_by(
                                '-score').first()
                            resource = {}
                            if resource_obj:
                                user = User.objects.get(id=resource_obj['user_id'])
                                resource['username'] = user.username
                                path2 = 'media/'+ str(user.user_avatar)
                                image = cv2.imread(path2)
                                if path2.find('.jpg'):
                                    avatar = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
                                else:
                                    avatar = base64.b64encode(cv2.imencode('.png', image)[1]).decode()
                                resource['avatar'] = avatar
                                resource['resource_id'] = resource_obj['resource_id']
                                resource['location'] = resource_obj['location']
                                resource['number'] = resource_obj['number']
                                resource['score'] = resource_obj['score']
                            sub_request['resource'] = resource
                            request_list.append(sub_request)
                            request_records.append(sub_request['request_id'])
                for item in request_list:
                    distance = Levenshtein.distance(keyword, item['context'])
                    if distance in request_distance_dict.keys():
                        new_distance = distance + 1
                        request_distance_dict[new_distance] = item
                    else:
                        request_distance_dict[distance] = item
                for item in sorted(request_distance_dict.keys(), reverse=False):
                    sorted_request_list.append(request_distance_dict.get(item))
        response['requests'] = sorted_request_list
        if len(sorted_request_list) == 0 and list(sorted_question_list) == 0 and len(sorted_base_list) == 0:
            response['code'] == 0
        else:
            response['code'] = 1
    except Exception as e:
        print(str(e))
        response['code'] = 0
    return JsonResponse(response)


# 更新个人信息
def update_info(request):
    response = {}
    try:
        user_id = request.POST.get('user_id')
        username = request.POST.get('new_username')
        gender = request.POST.get('new_gender')
        birthday = request.POST.get('new_birthday')
        education = request.POST.get('new_education')
        address = request.POST.get('new_address')
        email = request.POST.get('new_email')
        telephone = request.POST.get('new_telephone')
        if birthday == 'null':
            cursor.execute("update public.user set username=%s,user_gender=%s,user_edu=%s,\
                user_addr=%s,email=%s,user_tel=%s where id=%s;",(username,gender,education,address,
                email,telephone))
            #result = User.objects.filter(id=user_id).update(username=username, user_gender=gender,
            #                                                   user_edu=education,
            #                                                   user_addr=address, email=email,
            #                                                   user_tel=telephone)
        else:
            cursor.execute("update public.user set username=%s,user_gender=%s,user_edu=%s,user_bir=%s,\
                user_addr=%s,email=%s,user_tel=%s where id=%s;",(username,gender,birthday,education,address,
                email,telephone))
            #result = User.objects.filter(id=user_id).update(username=username, user_gender=gender,
            #                                                user_bir=birthday, user_edu=education,
            #                                                user_addr=address, email=email,
            #                                                user_tel=telephone)
        #if result:
        response['code'] = 1
        response['msg'] = '修改成功'
        return JsonResponse(response)
    except Exception as e:
        print(str(e))
        response['code'] = 0
        response['msg'] = str(e)
    return JsonResponse(response)


# 修改密码
def change_password(request):
    from django.contrib.auth.hashers import make_password, check_password
    response = {}
    try:
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        new_password1 = request.POST.get('new_password1')
        user = User.objects.get(id=user_id)
        if user:
            if check_password(password, user.password):
                try:
                    store_password = make_password(new_password1)
                    result = User.objects.filter(id=user_id).update(password=store_password)
                    if result:
                        response['code'] = 1
                        response['msg'] = '修改密码成功'
                        return JsonResponse(response)
                except Exception as e:
                    response['code'] = 0
                    response['msg'] = '修改密码失败'
            else:
                response['code'] = 0
                response['msg'] = '原密码错误'
    except Exception as e:
        response['code'] = 0
        response['msg'] = '修改密码失败'
    return JsonResponse(response)


# 发布需求（问题/资源）
def release_request(request):
    response = {}
    try:
        user = request.POST.get('user_id')
        type = request.POST.get('type')
        subject = request.POST.get('subject')
        deadline = request.POST.get('deadline')
        score = request.POST.get('score')
        context = request.POST.get('context')
        stime = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
        if deadline == 'NaN-NaN-NaN NaN:NaN:NaN':
            etime = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            etime = deadline
        user_obj = User.objects.get(id=user)
        subject_obj = Subject.objects.get(subject_id=subject)
        if type == 'Q':
            base_question_obj = Base_question.objects.filter(subject=subject_obj).values()
            base_questions = list(base_question_obj)
            for base_question in base_questions:
                distance = Levenshtein.distance(context, base_question['description'])
                if distance < 2:
                    response['code'] = 2
                    response['msg'] = '数据库中有相似度极高的问题，请前往搜索查询'
                    return JsonResponse(response)
            question_obj = Question.objects.filter(subject=subject_obj).values()
            questions = list(question_obj)
            for question in questions:
                distance = Levenshtein.distance(context, question['context'])
                if distance < 2:
                    response['code'] = 2
                    response['msg'] = '数据库中有相似度极高的问题，请前往搜素查询'
                    return JsonResponse(response)
            cursor.execute("insert into question(stime,etime,score,status,context,subject_id,\
                user_id,number) values (%s,%s,%s,%s,%s,%s,%s,0); ",(stime,etime,score,1,context,
                subject_obj.subject_id,user_obj.id))
            cursor.execute("select question_id from question where stime=%s and etime=%s and score=%s \
                and user_id=%s and context=%s;",(stime,etime,score,user_obj.id,context))
            question_obj = cursor.fetchone()[0]
            #obj1 = Question(stime=stime, etime=etime, score=score, status=True,
            #                context=context, subject=subject_obj, user=user_obj)
            #obj1.save()
            ###
            
            with transaction.atomic():
                cursor.execute("insert into forum_topic(section_id_id,user_id_id,topic_title,\
                topic_time,topic_reply_time,topic_click_num,topic_reply_num,topic_collect_num,\
                    topic_like_num,topic_content,topic_content_file_check,topic_hot_num) values \
                        (%s,%s,%s,%s,%s,0,0,0,0,'','f',0); ",(2,user,context,stime,stime))
                cursor.execute("select currval('forum_topic_topic_id_seq') as id;")
                topic_id = cursor.fetchone()[0]
                cursor.execute("insert into forum_question(topic_id_id,question_id) values \
                    (%s,%s);",(topic_id,question_obj))
            #newTopic = Topic.objects.create(section_id_id=2, user_id_id=user, topic_title=context,
            #                                topic_time=stime, topic_reply_time=stime)
            #newQuestionToTopic = QuestionToTopic.objects.create(topic_id_id=newTopic.topic_id,
            #                                                    question_id=obj1.question_id)
            ###
        elif type == 'R':
            request_obj = Request.objects.filter(subject=subject_obj).values()
            requests = list(request_obj)
            for sub_request in requests:
                distance = Levenshtein.distance(context, sub_request['context'])
                if distance < 2:
                    response['code'] = 3
                    response['msg'] = '数据库中有相似度极高的需求，请前往搜索查询'
                    return JsonResponse(response)
            cursor.execute("insert into request(stime,etime,score,status,context,\
                subject_id,user_id,number) values (%s,%s,%s,%s,%s,%s,%s,0);",
                (stime,etime,score,True,context,subject_obj.subject_id,user_obj.id))
            #obj1 = Request(stime=stime, etime=etime, score=score, status=True,
            #               context=context, subject=subject_obj, user=user_obj)
            #obj1.save()
        response['code'] = 1
        response['msg'] = '发布成功'
    except Exception as e:
        print(e)
        response['code'] = 0
        response['msg'] = '发布失败'
    return JsonResponse(response)


# 获取个人需求（问题/资源）
def get_requests(request):
    response = {}
    try:
        check_status()
        user = request.POST.get('user_id')
        user_obj = User.objects.get(id=user)
        questions_obj = user_obj.question_set.all().values().order_by('-question_id')
        requests_obj = user_obj.request_set.all().values().order_by('-request_id')
        print("get")
        questions = list(questions_obj)
        requests = list(requests_obj)
        for sub_request in requests:
            user = User.objects.get(id=sub_request['user_id'])
            sub_request['username'] = user.username
            subject = Subject.objects.get(subject_id=sub_request['subject_id'])
            sub_request['subject'] = subject.subject_name
            request_obj = Request.objects.get(request_id=sub_request['request_id'])
            resources_obj = request_obj.resource_set.all().values().order_by('-time')
            resources = list(resources_obj)
            for resource in resources:
                user = User.objects.get(id=resource['user_id'])
                resource['username'] = user.username
                path1 = 'media/'+ str(user.user_avatar)
                image = cv2.imread(path1)
                if path1.find('.jpg'):
                    avatar = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
                else:
                    avatar = base64.b64encode(cv2.imencode('.png', image)[1]).decode()
                resource['avatar'] = avatar
            sub_request['resources'] = resources
        for question in questions:
            user = User.objects.get(id=question['user_id'])
            question['username'] = user.username
            subject = Subject.objects.get(subject_id=question['subject_id'])
            question['subject'] = subject.subject_name
            question_to_topic = QuestionToTopic.objects.get(question_id=question['question_id'])
            question['topic_id'] = question_to_topic.topic_id_id
            question_obj = Question.objects.get(question_id=question['question_id'])
            answers_obj = question_obj.answer_set.all().values().order_by('-answer_id')
            answers = list(answers_obj)
            for answer in answers:
                user = User.objects.get(id=answer['user_id'])
                answer['username'] = user.username
                path2 = 'media/'+ str(user.user_avatar)
                image = cv2.imread(path2)
                if path2.find('.jpg'):
                    avatar = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
                else:
                    avatar = base64.b64encode(cv2.imencode('.png', image)[1]).decode()
                answer['avatar'] = avatar
            question['answers'] = answers
        response['questions'] = questions
        response['requests'] = requests
        response['code'] = 1
    except Exception as e:
        print(e)
        response['code'] = 0
        response['msg'] = '查询失败'
    return JsonResponse(response)


# 获取热门需求（问题/资源）
def get_hot_requests(request):
    response = {}
    try:
        check_status()
        #print("check fin")
        request_obj = Request.objects.filter(status=1).values().order_by('score').order_by('-number')
        question_obj = Question.objects.filter(status=1).values().order_by('score').order_by('-number')
        #print("re qe")
        requests = list(request_obj)
        questions = list(question_obj)
        for sub_request in requests:
            user = User.objects.get(id=sub_request['user_id'])
            sub_request['username'] = user.username
            subject = Subject.objects.get(subject_id=sub_request['subject_id'])
            sub_request['subject'] = subject.subject_name
            path1 = 'media/'+ str(user.user_avatar)
            image = cv2.imread(path1)
            if path1.find('.jpg'):
                avatar = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
            else:
                avatar = base64.b64encode(cv2.imencode('.png', image)[1]).decode()
            sub_request['avatar'] = avatar
        #print("refin")
        for question in questions:
            user = User.objects.get(id=question['user_id'])
            question['username'] = user.username
            subject = Subject.objects.get(subject_id=question['subject_id'])
            question['subject'] = subject.subject_name
            path2 = 'media/'+ str(user.user_avatar)
            image = cv2.imread(path2)
            if path2.find('.jpg'):
                avatar = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
            else:
                avatar = base64.b64encode(cv2.imencode('.png', image)[1]).decode()
            question['avatar'] = avatar
        #print("qefin")
        response['requests'] = requests
        response['questions'] = questions
        response['code'] = 1
    except Exception as e:
        print(e)
        response['code'] = 0
    return JsonResponse(response)


# 查看问题详情
def get_question(request):
    response = {}
    try:
        question_id = request.POST.get('question_id')
        question_obj = Question.objects.get(question_id=question_id)
        question = model_to_dict(question_obj)
        user = User.objects.get(id=question_obj.user_id)
        question['user_id'] = user.id
        question['username'] = user.username
        subject = Subject.objects.get(subject_id=question['subject'])
        question['subject'] = subject.subject_name
        question_to_topic = QuestionToTopic.objects.get(question_id=question_id)
        question['topic_id'] = question_to_topic.topic_id_id
        path1 = 'media/'+ str(user.user_avatar)
        image = cv2.imread(path1)
        if path1.find('.jpg'):
            avatar = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
        else:
            avatar = base64.b64encode(cv2.imencode('.png', image)[1]).decode()
        question['avatar'] = avatar
        answers_obj = question_obj.answer_set.all().values().order_by('-answer_id')
        answers = list(answers_obj)
        for answer in answers:
            user = User.objects.get(id=answer['user_id'])
            answer['user_id'] = user.id
            answer['username'] = user.username
            path2 = 'media/'+ str(user.user_avatar)
            image = cv2.imread(path2)
            if path2.find('.jpg'):
                avatar = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
            else:
                avatar = base64.b64encode(cv2.imencode('.png', image)[1]).decode()
            answer['avatar'] = avatar
        question['answers'] = answers
        response['question'] = question
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


# 查看需求详情
def get_request(request):
    response = {}
    try:
        request_id = request.POST.get('request_id')
        request_obj = Request.objects.get(request_id=request_id)
        sub_request = model_to_dict(request_obj)
        user = User.objects.get(id=request_obj.user_id)
        sub_request['username'] = user.username
        subject = Subject.objects.get(subject_id=sub_request['subject'])
        sub_request['subject'] = subject.subject_name
        path1 = 'media/'+ str(user.user_avatar)
        image = cv2.imread(path1)
        if path1.find('.jpg'):
            avatar = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
        else:
            avatar = base64.b64encode(cv2.imencode('.png', image)[1]).decode()
        sub_request['avatar'] = avatar
        resources_obj = request_obj.resource_set.all().values().order_by('-resource_id')
        resources = list(resources_obj)
        for resource in resources:
            user = User.objects.get(id=resource['user_id'])
            resource['username'] = user.username
            path2 = 'media/'+ str(user.user_avatar)
            image = cv2.imread(path2)
            if path2.find('.jpg'):
                avatar = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
            else:
                avatar = base64.b64encode(cv2.imencode('.png', image)[1]).decode()
            resource['avatar'] = avatar
        sub_request['resources'] = resources
        response['sub_request'] = sub_request
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


# 回答问题
def submit_answer(request):
    response = {}
    try:
        question_id = request.POST.get('question_id')
        user_id = request.POST.get('user_id')
        answer = request.POST.get('answer')
        question_obj = Question.objects.get(question_id=question_id)
        user_obj = User.objects.get(id=user_id)
        time = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("insert into answer(context,status,time,score,question,user_id) \
            values (%s,%s,%s,%s,%s,%s,%s);",(answer,0,time,0,question.question_id,user_obj.id))
        #answer_obj = Answer(context=answer, status=0, time=time, score=0, question=question_obj, user=user_obj)
        #answer_obj.save()
        question = Question.objects.filter(question_id=question_id).first()
        number = question.number + 1
        cursor.execute("update question set number=%s where question_id=%s;",
        (number,question_id))
        #Question.objects.filter(question_id=question_id).update(number=number)
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


# 评分
def rate_answer(request):
    response = {}
    try:
        answer_id = request.POST.get('answer_id')
        score = request.POST.get('score')
        cursor.execute("update answer set score=%s where answer_id=%s;",(score,answer_id))
        #Answer.objects.filter(answer_id=answer_id).update(score=score)
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def rate_resource(request):
    response = {}
    try:
        resource_id = request.POST.get('resource_id')
        score = request.POST.get('score')
        cursor.execute("update resource set score=%s where resource_id=%s;",(score,resource_id))
        #Resource.objects.filter(resource_id=resource_id).update(score=score)
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def get_unique_name(origin_name):
    unique_id = str(uuid.uuid1())
    index = origin_name.index('.')
    unique_name = origin_name[0:index] + ''.join(unique_id.split('-')) + origin_name[index:len(origin_name)]
    return unique_name


def get_origin_name(unique_name):
    index = unique_name.index('.')
    origin_name = unique_name[0:index - 32] + unique_name[index:len(unique_name)]
    return origin_name


# 文件上传/下载
def upload_files(request):
    response = {}
    try:
        user_id = request.COOKIES.get('user_id')
        request_id = request.POST.get('request_id')
        dest_path = BASE_DIR + '/resource/' + user_id + '/'
        user_obj = User.objects.get(id=user_id)
        request_obj = Request.objects.get(request_id=request_id)
        files = request.FILES.getlist("file", None)
        if not files:
            response['code'] = 0
            response['msg'] = '上传失败'
            return JsonResponse(response)
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)
        for file in files:
            unique_name = get_unique_name(file.name)
            filepath = os.path.join(dest_path, unique_name)
            with open(filepath, 'wb') as fp:
                for part in file.chunks():
                    fp.write(part)
            imgUrl = '/resource/' + user_id + '/' + unique_name
            time = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("insert into resource(time,location,score,number,request_id,user_id) \
                values (%s,%s,%s,%s,%s,%s);",(time,imgUrl,0,0,request_obj.request_id,user_obj.id))
            #resource_obj = Resource(time=time, location=imgUrl, score=0, number=0, request=request_obj, user=user_obj)
            #resource_obj.save()
        number = request_obj.number + 1
        cursor.execute("update request set number=%s where request_id=%s;",
        (number,request_id))
        #Request.objects.filter(request_id=request_id).update(number=number)
        response['code'] = 1
        response['msg'] = '上传成功'
    except Exception as e:
        print(str(e))
        response['code'] = 0
        response['msg'] = '上传失败'
    return JsonResponse(response)


def download(request, resource_id, filename):
    def file_iterator(file, chunk_size=512 * 512 * 16):
        with open(file, 'rb') as f:
            if f:
                yield f.read(chunk_size)

    resource_obj = Resource.objects.get(resource_id=resource_id)
    the_file_name = BASE_DIR + resource_obj.location
    response = StreamingHttpResponse(file_iterator(the_file_name))
    number = resource_obj.number + 1
    cursor.execute("update resource set number=%s where resource_id=%s;",
    (resource_id,number))
    #Resource.objects.filter(resource_id=resource_id).update(number=number)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachement;filename="{0}"'.format(filename)
    return response


# 获取个人资源
def get_resources(request):
    response = {}
    user_id = request.POST.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        resource_obj = user.resource_set.all().values().order_by('-time')
        resources = list(resource_obj)
        for resource in resources:
            sub_request = Request.objects.get(request_id=resource['request_id'])
            resource['context'] = sub_request.context
        response['resources'] = resources
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def search_by_condition(request):
    response = {}
    condition_resources = []
    user_id = request.POST.get('user_id')
    type = request.POST.get('type')
    keyword = request.POST.get('keyword')
    try:
        user = User.objects.get(id=user_id)
        resource_obj = user.resource_set.all().values().order_by('-time')
        resources = list(resource_obj)
        for resource in resources:
            sub_request = Request.objects.get(request_id=resource['request_id'])
            resource['context'] = sub_request.context
        if not type == '0' and not keyword == '0':
            for resource in resources:
                if get_type(resource['location']) == type and contain(resource['location'], keyword):
                    condition_resources.append(resource)
        elif not type == '0':
            for resource in resources:
                if get_type(resource['location']) == type:
                    condition_resources.append(resource)
        elif not keyword == '0':
            for resource in resources:
                if contain(resource['location'], keyword):
                    condition_resources.append(resource)
        else:
            for resource in resources:
                condition_resources.append(resource)
        response['resources'] = condition_resources
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def get_type(name):
    type = name[name.rfind('.', 0, len(name)) + 1:len(name)]
    return type


def contain(origin, keyword):
    if origin.find(keyword, 0, len(origin)) > -1:
        return True
    else:
        return False


# 获取个人回答
def get_answers(request):
    response = {}
    user_id = request.POST.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        answers = user.answer_set.all().values().order_by('-time')
        answerList = list(answers)
        for answer in answerList:
            question = Question.objects.get(question_id=answer['question_id'])
            answer['question'] = question.context
        response['answers'] = answerList
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


# 检查问题/需求是否过期
def check_status():
    question_obj = Question.objects.filter(status=1).values()
    questions = list(question_obj)
    time = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
    for question in questions:
        etime = str(question['etime'])
        if time >= etime:
            cursor.execute("update question set status=%s where question_id=%s;",
            (0,question['question_id']))
            #Question.objects.filter(question_id=question['question_id']).update(status=0)
    request_obj = Request.objects.filter(status=1).values()
    #print("check ques fin")
    requests = list(request_obj)
    for request in requests:
        etime = str(request['etime'])
        if time >= etime:
            cursor.execute("update request set status=%s where request_id=%s;",
            (0,request['request_id']))
            #Request.objects.filter(request_id=request['request_id']).update(status=0)

# 重新激活问题/需求
def activate_request(request):
    response = {}
    request_id = request.POST.get('request_id')
    time = request.POST.get('time')
    try:
        request_obj = Request.objects.get(request_id=request_id)
        if request_obj.status == 1:
            cursor.execute("update request set etime=%s where request_id=%s;",
            (time,request_id))
            #Request.objects.filter(request_id=request_id).update(etime=time)
        elif request_obj.status == 0:
            cursor.execute("update request set etime=%s,status=%s where request_id=%s;",
            (time,1,request_id))
            #Request.objects.filter(request_id=request_id).update(etime=time, status=1)
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def activate_question(request):
    response = {}
    question_id = request.POST.get('question_id')
    time = request.POST.get('time')
    try:
        question_obj = Question.objects.get(question_id=question_id)
        if question_obj.status == 1:
            cursor.execute("update question set etime=%s where question_id=%s;",
            (time,question_id))
            #Question.objects.filter(question_id=question_id).update(etime=time)
        elif question_obj.status == 0:
            cursor.execute("update question set etime=%s,status=%s where question_id=%s;",
            (time,1,question_id))
            #Question.objects.filter(question_id=question_id).update(etime=time, status=1)
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def end_question(request):
    response = {}
    question_id = request.POST.get('question_id')
    try:
        cursor.execute("update question set status=%s where question_id=%s;",
            (2,question_id))
        #Question.objects.filter(question_id=question_id).update(status=2)
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


# 教师功能
# 选择适当答案上传至基本库
def accept_answer(request):
    response = {}
    question_id = request.POST.get('question_id')
    answer_id = request.POST.get('answer_id')
    try:
        question_obj = Question.objects.get(question_id=question_id)
        subject_obj = Subject.objects.get(subject_id=question_obj.subject_id)
        answer_obj = Answer.objects.get(answer_id=answer_id)
        last_question = Base_question.objects.order_by('base_question_id').last()
        new_id = last_question.base_question_id + 1
        cursor.execute("insert into base_question(base_question_id,description,answer,\
            subject_id) values (%s,%s,%s,%s);",(new_id,question_obj.context,answer_obj.context,
            subject_obj.subject_id))
        #base_question = Base_question.objects.create(base_question_id=new_id, description=question_obj.context,
        #                                             answer=answer_obj.context, subject=subject_obj)
        #base_question.save()
        cursor.execute("update question set status=%s where question_id=%s;",(3,question_id))
        cursor.execute("update answer set status=%s where answer_id=%s;",(2,answer_id))
        #Question.objects.filter(question_id=question_id).update(status=3)
        #Answer.objects.filter(answer_id=answer_id).update(status=2)
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


# 教师功能
# 教师直接回答问题至基本库
def submit_base(request):
    response = {}
    question_id = request.POST.get('question_id')
    answer = request.POST.get('answer')
    try:
        question_obj = Question.objects.get(question_id=question_id)
        subject_obj = Subject.objects.get(subject_id=question_obj.subject_id)
        description = question_obj.context
        last_question = Base_question.objects.order_by('base_question_id').last()
        new_id = last_question.base_question_id + 1
        cursor.execute("insert into base_question(base_question_id,description,answer,\
            subject_id) values (%s,%s,%s,%s);",(new_id,description,answer,subject_obj.subject_id))
        #base_question = Base_question.objects.create(base_question_id=new_id, description=description,
        #                                             answer=answer, subject=subject_obj)
        #base_question.save()
        cursor.execute("update question set status=%s where question_id=%s;",(3,question_id))
        #Question.objects.filter(question_id=question_id).update(status=3)
        response['code'] = 1
    except Exception as e:
        print(str(e))
        response['code'] = 0
    return JsonResponse(response)


def get_store_questions(request):
    response = {}
    try:
        questions_obj = Question.objects.filter(status=2).values().order_by('stime').order_by('number')
        questions = list(questions_obj)
        for question in questions:
            user = User.objects.get(id=question['user_id'])
            question['username'] = user.username
            subject = Subject.objects.get(subject_id=question['subject_id'])
            question['subject'] = subject.subject_name
            question_obj = Question.objects.get(question_id=question['question_id'])
            answers_obj = question_obj.answer_set.all().values().order_by('-answer_id')
            answers = list(answers_obj)
            for answer in answers:
                user = User.objects.get(id=answer['user_id'])
                answer['username'] = user.username
                path2 = 'media/'+ str(user.user_avatar)
                image = cv2.imread(path2)
                if path2.find('.jpg'):
                    avatar = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
                else:
                    avatar = base64.b64encode(cv2.imencode('.png', image)[1]).decode()
                answer['avatar'] = avatar
            question['answers'] = answers
        response['store_questions'] = questions
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
        response['msg'] = '查询失败'
    return JsonResponse(response)


def batch_download(request):
    response = {}

    def file_iterator(file, chunk_size=512 * 512 * 16):
        with open(file, 'rb') as f:
            if f:
                yield f.read(chunk_size)

    path = BASE_DIR + "/resource/download.zip"
    if os.path.exists(path):
        os.remove(path)
    resources = request.POST.get('resources')
    id_list = resources.split(',')
    zipFile = zipfile.ZipFile(path, 'w')
    for index in range(len(id_list)):
        resource_obj = Resource.objects.get(resource_id=id_list[index])
        file_path = BASE_DIR + resource_obj.location
        start = file_path.rindex('/')
        file_name = get_origin_name(file_path[start + 1:])
        zipFile.write(file_path, file_name, zipfile.ZIP_DEFLATED)
        number = resource_obj.number + 1
        cursor.execute("update resource set number=%s where resource_id=%s;",(number,resource_id))
        #Resource.objects.filter(resource_id=id_list[index]).update(number=number)
    zipFile.close()
    response['code'] = 1
    return JsonResponse(response)


def download_zip(request):
    path = BASE_DIR + "/resource/download.zip"
    with open(path, 'rb') as f:
        c = f.read()
    response = HttpResponse(c, content_type='application/zip')
    # zipFile = zipfile.ZipFile(path, 'w')
    # response = FileResponse(zipFile, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=download.zip'
    return response


def send_to_note(request):
    response = {}
    answer_id = request.POST.get('answer_id')
    try:
        # 当前用户
        answer_obj = Answer.objects.get(answer_id=answer_id)
        user_obj = User.objects.get(id=answer_obj.user_id)
        # 上传日期
        upload_date = timezone.localtime().strftime("%Y-%m-%d")
        # 上传时间
        upload_time = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
        # 修改回答状态
        Answer.objects.filter(answer_id=answer_id).update(upload_time=upload_time)
        answers = user_obj.answer_set.exclude(upload_time=None).order_by('upload_time').values()
        answerList = list(answers)
        note_text = ''
        # 笔记内容
        for answer in answerList:
            if get_date(str(answer['upload_time'])) == str(upload_date):
                question = Question.objects.get(question_id=answer['question_id'])
                question_context = question.context
                sub_note_text = "##### 问题:\n" + \
                                question_context + "\n" + \
                                "##### 优质回答:\n" + \
                                answer['context'] + "\n\n" + "---" + "\n"
                note_text += sub_note_text

        # 获取笔记本
        notebook = NoteBook.objects.get(notebook_name='优质问答笔记本', creator_id=user_obj)
        # 加密
        vi = b'HjRP7LlXuSsFMisz'  # 偏移量
        mode = 'CBC'  # 加密模式 使用CBC模式安全性更高
        encode_ = 'utf-8'
        # 加密密钥
        key = 'mycloudnote'
        # 设置加密器
        cipher = AESUtil(key, mode, vi, encode_)
        # 笔记内容加密
        en_text = cipher.aesencrypt(note_text)

        # 笔记名称
        note_title = upload_date + "优质问答"
        try:
            note_obj = Note.objects.get(note_title=note_title, writer_id=user_obj)
            # 添加笔记内容
            Note.objects.filter(note_title=note_title, writer_id=user_obj, notebook_id=notebook).update(
                note_text=en_text)
        except Exception as e:
            # 新增笔记
            note_obj = Note.objects.create(note_title=note_title, writer_id=user_obj, notebook_id=notebook,
                                           note_text=en_text)
        response['code'] = 1
    except Exception as e:
        print(str(e))
        response['code'] = 0
    return JsonResponse(response)


def get_date(time):
    date = time[0:10]
    return date
