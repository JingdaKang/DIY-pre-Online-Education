import os
from django.shortcuts import render
from django.http import JsonResponse
from backend.models import *
from django.utils import timezone as datetime
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
import json
from django.db.models import Q
import time

from django.db import connection,transaction
# Create your views here.
cursor = connection.cursor()

def topics(request):
    if request.method == "GET":
        section = int(request.GET.get('tab', default=3))
        if(section == 1): #热门
            topics = Topic.objects.all().order_by("-topic_hot_num", "-topic_id")
        elif(section == 2):
            username = request.user.username
            if(username == None or username.strip() == ''):
                topics = Topic.objects.all().order_by("-topic_hot_num", "-topic_id")
            else:
                user = User.objects.get(username=username)
                following_users = Follow.objects.filter(follow_by_user_id=user.id)
                following_user_id = []
                for following_user in following_users:
                    following_user_id.append(following_user.follow_on_user_id)
                topics = Topic.objects.filter(user_id__in=following_user_id).order_by("-topic_id")
                if(topics.count() == 0):
                    topics = Topic.objects.all().order_by("-topic_hot_num", "-topic_id")


        elif(section == 3):
            topics = Topic.objects.all().order_by("-topic_id")

        elif(section > 3):
            filter_section = section - 3
            topics = Topic.objects.all().filter(section_id=filter_section).order_by("-topic_id")
        else:
            topics = Topic.objects.all()
        result = []
        for topic in topics:
            temp = {}
            temp['topic_id'] = topic.topic_id
            temp['topic_title'] = topic.topic_title
            temp['topic_content'] = topic.topic_content[0:100]
            temp['topic_user_id'] = topic.user_id_id
            author = User.objects.get(id=topic.user_id_id)
            temp['topic_username'] = author.username
            temp['topic_avatar_url'] = str(author.user_avatar)
            temp['topic_click_num'] = topic.topic_click_num
            temp['topic_reply_num'] = topic.topic_reply_num
            temp['topic_like_num'] = topic.topic_like_num
            temp['topic_hot_num'] = topic.topic_hot_num
            temp['topic_create_time'] = topic.topic_time
            temp['topic_reply_time'] = topic.topic_reply_time

            #是否解决
            temp['topic_section'] = topic.section_id_id
            if topic.section_id_id == 2:
                qtt = QuestionToTopic.objects.filter(topic_id=topic.topic_id)
                if qtt.count() == 1:
                    for q in qtt:
                        question = Question.objects.get(question_id=q.question_id)
                        if question is not None and question.status == 3:
                            temp['is_solved'] = 1
                        else:
                            temp['is_solved'] = 0
                else:
                    temp['is_solved'] = 0

            result.append(temp)

        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        if username is not None and password is not None:
            isLogin = authenticate(request, username=username, password=password) #校验用户名密码
            if isLogin:
                login(request, isLogin)
                return JsonResponse({
                    "status": 0,
                    "message": "登陆成功",
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


def register(request):
    if request.method == "POST":
        data = json.loads(request.body)

        if request.GET.get("check") is not None:
            check_username = data.get("check_username")
            print(check_username)
            try:
                User.objects.get(username=check_username)
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
        password = data.get("password")

        if username is not None and password is not None:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login_user = authenticate(request, username=username, password=password)
                if login_user:
                    login(request, login_user)
                    return JsonResponse({
                        "status": 0,
                        "message": "注册成功"
                    })

            except:
                return JsonResponse({
                    "status": 2,
                    "message": "注册失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def logout_user(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({
            "status": 0,
            "message": "退出成功",
        })
    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！",
        })


def topic_detail(request, topic_id):
    if request.method == "GET":
        username = request.user.username
        topic_get_id = topic_id
        topic = Topic.objects.get(topic_id=topic_get_id)
        result = {}
        result['topic_id'] = int(topic_get_id)
        author = User.objects.get(id=topic.user_id_id)
        result['topic_user_id'] = author.id
        result['topic_username'] = author.username
        result['topic_avatar_url'] = str(author.user_avatar)
        result['topic_user_credit'] = author.user_credit
        result['topic_title'] = topic.topic_title
        result['section_name'] = Section.objects.get(section_id=topic.section_id_id).section_name
        result['topic_content'] = topic.topic_content
        result['topic_click_num'] = topic.topic_click_num
        result['topic_reply_num'] = topic.topic_reply_num
        result['topic_collect_num'] = topic.topic_collect_num
        result['topic_like_num'] = topic.topic_like_num
        result['topic_create_time'] = topic.topic_time
        result['topic_content_file_check'] = topic.topic_content_file_check
        if username is None or username.strip() != '':
            user = User.objects.get(username=username)
            if_following = Follow.objects.filter(follow_on_user=author.id, follow_by_user=user.id)
            if (if_following.exists()):
                result['if_following'] = 1
            else:
                result['if_following'] = 0

            if_praise = Like.objects.filter(like_type=1, like_user_id=user.id, like_content_id=topic.topic_id)
            if (if_praise.exists()):
                result['if_praise'] = 1
            else:
                result['if_praise'] = 0

            if_collect = Collect.objects.filter(user_id=user.id, topic_id=topic.topic_id)
            if (if_collect.exists()):
                result['if_collect'] = 1
            else:
                result['if_collect'] = 0
        else:
            result['if_following'] = 0
            result['if_praise'] = 0
            result['if_collect'] = 0

        if(topic.topic_content_file_check):
            result['topic_file_id'] = topic.file_id_id
            file = ForumFile.objects.get(file_id=topic.file_id_id)
            result['file_name'] = file.file_name
            result['file_url'] = str(file.file_url)

        #是否解决
        rec_answer = ""
        if topic.section_id_id == 2:
            qtt = QuestionToTopic.objects.filter(topic_id=topic.topic_id)
            if qtt.count() == 1:
                for q in qtt:
                    question = Question.objects.get(question_id=q.question_id)
                    if question is not None and question.status == 3:
                        result['is_solved'] = 1
                        answer_str = ""
                        answer_set = Answer.objects.filter(question_id=q.question_id)
                        for a in answer_set:
                            if answer_str.strip() == "":
                                answer_str += str(a.context)
                        rec_answer += answer_str

                    else:
                        result['is_solved'] = 0
            else:
                result['is_solved'] = 0
        result['rec_answer'] = rec_answer
        #
        replies_result = []
        if(Reply.objects.filter(reply_topic_id=topic_get_id).count() != 0):
            replies = Reply.objects.filter(reply_topic_id=topic_get_id).order_by("reply_id")
            for reply in replies:
                temp = {}
                temp['reply_id'] = reply.reply_id
                temp['user_id'] = reply.user_id_id
                reply_author = User.objects.get(id=reply.user_id_id)
                temp['reply_username'] = reply_author.username
                temp['reply_avatar_url'] = str(reply_author.user_avatar)
                temp['reply_content'] = reply.reply_content
                temp['reply_time'] = reply.reply_time
                temp['reply_like_num'] = reply.reply_like_num
                replies_result.append(temp)

        result['replies'] = replies_result

        user_other_topics = []
        user_topics = Topic.objects.filter(user_id_id=author.id).order_by("-topic_id")[:10]
        for user_topic in user_topics:
            if user_topic.topic_id != topic_id:
                temp2 = {}
                temp2["topic_id"] = user_topic.topic_id
                temp2["topic_title"] = user_topic.topic_title
                user_other_topics.append(temp2)

        result['user_other_topics'] = user_other_topics
        #cursor.execute("update forum_topic set topic_click_num=topic_click_num+1,\
        #    topic_hot_num=topic_hot_num+5 where topic_id=%s;",(topic_id,))
        topic.topic_click_num = topic.topic_click_num + 1
        topic.topic_hot_num = topic.topic_hot_num + 5
        topic.save()

        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def user_post_detail(request):
    if request.method == "GET":
        get_username = request.GET.get('user')
        user = User.objects.get(username=get_username)
        result = {}
        result['user_id'] = user.id
        result['username'] = user.username
        topics_result = []
        if(Topic.objects.filter(user_id=user.id).count() != 0):
            topics = Topic.objects.filter(user_id=user.id).order_by("-topic_id")
            for topic in topics:
                temp = {}
                temp['topic_id'] = topic.topic_id
                temp['user_id'] = user.id
                temp['topic_username'] = user.username
                temp['topic_title'] = topic.topic_title
                temp['section_name'] = Section.objects.get(section_id=topic.section_id_id).section_name
                temp['topic_time'] = topic.topic_time
                temp['topic_reply_time'] = topic.topic_reply_time
                temp['topic_reply_num'] = topic.topic_reply_num
                topics_result.append(temp)

        result['topics'] = topics_result

        replies_result = []
        if(Reply.objects.filter(user_id=user.id).count() != 0):
            replies = Reply.objects.filter(user_id=user.id).order_by("-reply_id")
            for reply in replies:
                temp = {}
                reply_topic = Topic.objects.get(topic_id=reply.reply_topic_id_id)
                temp['reply_id'] = reply.reply_id
                temp['user_id'] = user.id
                temp['reply_username'] = user.username
                temp['reply_avatar_url'] = str(user.user_avatar)
                temp['reply_topic_id'] = reply_topic.topic_id
                temp['reply_topic_title'] = reply_topic.topic_title
                temp['reply_content'] = reply.reply_content
                temp['reply_time'] = reply.reply_time
                replies_result.append(temp)

        result['replies'] = replies_result
        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def section_name(request):
    if request.method == "GET":
        sections = Section.objects.all().order_by("section_id")
        result = []
        for section in sections:
            temp = {}
            temp["id"] = section.section_id
            temp["name"] = section.section_name
            temp["count"] = Topic.objects.filter(section_id = section.section_id).count()
            result.append(temp)


        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def search(request):
    if request.method == "GET":
        keyword = str(request.GET.get('keyword', default=''))
        result = []
        topics = Topic.objects.filter(Q(topic_title__icontains= keyword) | Q(topic_content__icontains =keyword))

        for topic in topics:
            temp = {}
            temp['topic_id'] = topic.topic_id
            temp['topic_title'] = topic.topic_title
            temp['topic_user_id'] = topic.user_id_id
            author = User.objects.get(id=topic.user_id_id)
            temp['topic_username'] = author.username
            temp['topic_avatar_url'] = str(author.user_avatar)
            temp['topic_click_num'] = topic.topic_click_num
            temp['topic_reply_num'] = topic.topic_reply_num
            temp['topic_like_num'] = topic.topic_like_num
            temp['topic_create_time'] = topic.topic_time
            temp['topic_reply_time'] = topic.topic_reply_time

            result.append(temp)

        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def user_info_detail(request):
    if request.method == "GET":
        get_username = request.GET.get('user')
        user = User.objects.get(username=get_username)
        result = {}
        result['user_id'] = user.id
        result['username'] = user.username
        result['avatar_url'] = str(user.user_avatar)
        result['user_gender'] = user.user_gender
        result['user_bir'] = user.user_bir
        result['user_edu'] = user.user_edu
        result['user_addr'] = user.user_addr
        result['user_tel'] = user.user_tel
        result['user_type'] = user.type
        result['user_following_num'] = user.user_following_num
        result['user_follower_num'] = user.user_follower_num
        result['user_credit'] = user.user_credit
        result['user_unread_count'] = Message.objects.filter(message_receive_user=user.id, message_read=False).count()

        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def add_reply(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.user.username
        print(username)
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 4,
                "message": "请先登录哦"
            })
        user_id = user.id
        reply_topic_id = int(data.get("reply_topic_id"))
        reply_content = data.get("reply_content")
        reply_time = datetime.now()
        if reply_content.strip() == '':
            return JsonResponse({
                "status": 3,
                "message": "回复不能为空"
            })
        elif user_id is not None and reply_topic_id is not None and reply_content is not None:
            try:
                with transaction.atomic():
                    cursor.execute("insert into forum_reply(user_id_id,reply_topic_id_id,reply_content,\
                        reply_time,reply_like_num) values (%s,%s,%s,%s,0);",(user_id,reply_topic_id,reply_content,
                        reply_time))
                    new_reply = Reply.objects.latest('reply_id')
                #new_reply = Reply.objects.create(user_id_id=user_id, reply_topic_id_id=reply_topic_id,
                #                                 reply_content=reply_content, reply_time=reply_time)
                topic = Topic.objects.get(topic_id=reply_topic_id)
                topic.topic_reply_num = topic.topic_reply_num + 1
                topic.topic_hot_num = topic.topic_hot_num + 45
                topic.topic_reply_time = reply_time
                topic.save()
                user.user_credit = user.user_credit + 1
                user.save()
                author = User.objects.get(id=topic.user_id_id)
                message_content = "您的帖子\""+ topic.topic_title + "\"有了新回复"
                cursor.execute("insert into forum_message(message_send_user_id,message_receive_user_id,\
                    message_related_type,message_related_id,message_content,message_read,message_time) \
                        values (%s,%s,%s,%s,%s,'f',now());",(user.id,author.id,1,topic.topic_id,message_content))
                '''new_message = Message.objects.create(message_send_user_id=user.id, message_receive_user_id=author.id,
                                                     message_related_type=1, message_related_id=topic.topic_id,
                                                     message_content=message_content)'''
                return JsonResponse({
                    "status": 0,
                    "message": "发布回复成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "发布回复失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def delete_reply(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.user.username
        try:
            cur_user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 4,
                "message": "请先登录哦"
            })
        reply_id = data.get("reply_id")
        reply = Reply.objects.get(reply_id=reply_id)
        reply_topic_id = reply.reply_topic_id_id
        user = User.objects.get(id=reply.user_id_id)
        if cur_user.id != user.id:
            return JsonResponse({
                "status": 3,
                "message": "无权限"
            })
        if reply_id is not None:
            try:
                Reply.objects.filter(reply_id=reply_id).delete()
                topic = Topic.objects.get(topic_id=reply_topic_id)
                topic.topic_reply_num = topic.topic_reply_num - 1
                topic.topic_hot_num = topic.topic_hot_num - 45
                topic.save()
                user.user_credit = user.user_credit - 1
                user.save()
                return JsonResponse({
                    "status": 0,
                    "message": "删除回复成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "删除回复失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def add_topic(request):
    if request.method == "POST":
        username = request.user.username
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 3,
                "message": "请先登录哦"
            })
        if(request.POST.get("section_id") == ''):
            return JsonResponse({
                "status": 4,
                "message": "请选择板块！"
            })
        user_id = user.id
        section_id = int(request.POST.get("section_id"))
        topic_title = request.POST.get("topic_title")
        topic_content = request.POST.get("topic_content")
        topic_time = datetime.now()
        file = request.FILES.get("file")
        file_check = False
        if file is not None:
            try:
                file_check = True
                file_name = file.name
                with transaction.atomic():
                    cursor.execute("insert into forum_file(user_id_id,file_name,file_url) \
                        values (%s,%s,%s);",(user.id,file_name,file))
                    new_file = ForumFile.objects.latest('file_id')
                #new_file = ForumFile.objects.create(user_id_id=user.id, file_name=file_name,
                #                                    file_url=file)
                file_id = new_file.file_id
            except:
                return JsonResponse({
                    "status": 6,
                    "message": "附件上传失败"
                })
        if topic_title.strip() == '' or section_id == '':
            return JsonResponse({
                "status": 5,
                "message": "标题不能为空"
            })
        elif user_id is not None and section_id is not None and topic_title is not None and topic_content is not None :
            try:
                with transaction.atomic():
                    cursor.execute("insert into forum_topic(section_id_id,user_id_id,topic_title,\
                        topic_content,topic_time,topic_reply_time,topic_click_num,topic_like_num,\
                            topic_reply_num,topic_collect_num,topic_hot_num,topic_content_file_check) \
                            values (%s,%s,%s,%s,%s,%s,0,0,0,0,0,'f');",(section_id,user_id,topic_title,
                            topic_content,topic_time,topic_time))
                    new_topic = Topic.objects.latest('topic_id')
                #new_topic = Topic.objects.create(section_id_id=section_id, user_id_id=user_id, topic_title=topic_title,
                #                                 topic_content=topic_content, topic_time=topic_time, topic_reply_time=topic_time)
                user.user_credit = user.user_credit + 5
                user.save()
                if file_check is True:
                    new_topic.topic_content_file_check = True
                    new_topic.file_id_id = file_id
                    new_topic.save()
                return JsonResponse({
                    "topic_id": new_topic.topic_id,
                    "status": 0,
                    "message": "发布主题成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "发布主题失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def group_name(request):
    if request.method == "GET":
        groups = Group.objects.all()
        result = []
        for group in groups:
            temp = {}
            temp["id"] = group.group_id
            temp["name"] = group.group_name
            temp["count"] = Discuss.objects.filter(group_id = group.group_id).count()
            result.append(temp)


        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def user_group_name(request):
    if request.method == "GET":
        username = request.GET.get('user')
        user = User.objects.get(username=username)
        join_groups = GroupMember.objects.filter(group_user_id_id=user.id)

        if(join_groups.exists() == False):
            return JsonResponse({"status": 2, "message": "未加入任何小组"})

        groups = []
        for join_group in join_groups:
            group = Group.objects.get(group_id=join_group.group_id_id)
            groups.append(group)

        result = []
        for group in groups:
            temp = {}
            temp["id"] = group.group_id
            temp["name"] = group.group_name
            temp["count"] = Discuss.objects.filter(group_id = group.group_id).count()
            result.append(temp)


        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def user_not_in_group_name(request):
    if request.method == "GET":
        username = request.GET.get('user')
        if username is None or username.strip() == '':
            return group_name(request)
        user = User.objects.get(username=username)
        groups = Group.objects.all()
        result = []
        for group in groups:
            if(GroupMember.objects.filter(group_id=group.group_id, group_user_id=user.id).exists() == False):
                temp = {}
                temp["id"] = group.group_id
                temp["name"] = group.group_name
                temp["count"] = Discuss.objects.filter(group_id=group.group_id).count()
                result.append(temp)


        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def group_discuss(request):
    if request.method == "GET":
        tab = int(request.GET.get('tab', default=0))
        if(tab == 0):
            username = request.GET.get('user')
            if(username == None or username.strip() == ''):
                discuss_set = Discuss.objects.all().order_by("-discuss_click_num", "-discuss_id")
            else:
                user = User.objects.get(username=username)
                join_groups = GroupMember.objects.filter(group_user_id=user.id)
                join_groups_id = []
                for join_group in join_groups:
                    join_groups_id.append(join_group.group_id)
                discuss_set = Discuss.objects.filter(group_id__in=join_groups_id).order_by("-discuss_id")


        elif(tab == -1):
            discuss_set = Discuss.objects.all().order_by("-discuss_hot_num", "-discuss_id")
        elif(tab > 0):
            filter_group = tab
            discuss_set = Discuss.objects.all().filter(group_id=filter_group).order_by("-discuss_id")
        else:
            discuss_set = Discuss.objects.all()
        result = []
        for discuss in discuss_set:
            temp = {}
            temp['discuss_id'] = discuss.discuss_id
            temp['discuss_title'] = discuss.discuss_title
            temp['user_id'] = discuss.user_id_id
            author = User.objects.get(id=discuss.user_id_id)
            temp['discuss_username'] = author.username
            temp['discuss_avatar_url'] = str(author.user_avatar)
            temp['discuss_click_num'] = discuss.discuss_click_num
            temp['discuss_reply_num'] = discuss.discuss_reply_num
            temp['discuss_time'] = discuss.discuss_time
            temp['discuss_reply_time'] = discuss.discuss_reply_time

            result.append(temp)

        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def add_group(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.user.username
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 6,
                "message": "请先登录哦"
            })
        user_id = user.id
        group_name = data.get("group_name")
        if user.user_credit < 30 and user.type == 'S':
            return JsonResponse({
                "status": 5,
                "message": "贡献度不足，请提高贡献度到30以上"
            })

        if group_name.strip() == '':
            return JsonResponse({
                "status": 3,
                "message": "小组名不能为空"
            })
        else:
            result = Group.objects.filter(group_name=group_name)
            if result.exists():
                return JsonResponse({
                    "status": 4,
                    "message": "小组名已存在"
                })
        if group_name is not None:
            try:
                with transaction.atomic():
                    cursor.execute("insert into forum_group(group_name,group_owner_id_id) values (%s,%s);",
                    (group_name,user_id))
                    new_group = Group.objects.latest('group_id')
                    cursor.execute("insert into forum_group_member(group_id_id,group_user_id_id) values (%s,%s);",
                    (new_group.group_id,user_id))
                #new_group = Group.objects.create(group_name=group_name, group_owner_id_id=user_id)
                #group_member = GroupMember.objects.create(group_id_id=new_group.group_id, group_user_id_id=user_id)
                return JsonResponse({
                    "status": 0,
                    "message": "创建成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "创建失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def discuss_detail(request, discuss_id):
    if request.method == "GET":
        username = request.user.username
        discuss_id = discuss_id
        discuss = Discuss.objects.get(discuss_id=discuss_id)
        result = {}
        result['discuss_id'] = int(discuss_id)
        author = User.objects.get(id=discuss.user_id_id)
        result['discuss_user_id'] = author.id
        result['discuss_username'] = author.username
        result['discuss_avatar_url'] = str(author.user_avatar)
        result['discuss_user_credit'] = author.user_credit
        result['discuss_title'] = discuss.discuss_title
        result['group_name'] = Group.objects.get(group_id=discuss.group_id_id).group_name
        result['discuss_content'] = discuss.discuss_content
        result['discuss_click_num'] = discuss.discuss_click_num
        result['discuss_reply_num'] = discuss.discuss_reply_num
        result['discuss_time'] = discuss.discuss_time
        result['discuss_reply_time'] = discuss.discuss_reply_time
        result['discuss_content_file_check'] = discuss.discuss_content_file_check
        if username is None or username.strip() != '':
            user = User.objects.get(username=username)
            if_focus = FocusDiscuss.objects.filter(focus_user_id=user.id, focus_discuss_id=discuss_id)
            if (if_focus.exists()):
                result['if_focus'] = 1
            else:
                result['if_focus'] = 0
        else:
            result['if_focus'] = 0

        if(discuss.discuss_content_file_check):
            result['discuss_file_id'] = discuss.discuss_file_id_id
            file = ForumFile.objects.get(file_id=discuss.discuss_file_id_id)
            result['file_name'] = file.file_name
            result['file_url'] = str(file.file_url)

        replies_result = []
        if(DiscussReply.objects.filter(discuss_reply_discuss_id=discuss_id).count() != 0):
            replies = DiscussReply.objects.filter(discuss_reply_discuss_id=discuss_id).order_by("discuss_reply_id")
            for reply in replies:
                temp = {}
                temp['discuss_reply_id'] = reply.discuss_reply_id
                temp['discuss_user_id'] = reply.discuss_user_id_id
                reply_author = User.objects.get(id=reply.discuss_user_id_id)
                temp['discuss_reply_username'] = reply_author.username
                temp['discuss_reply_avatar_url'] = str(reply_author.user_avatar)
                temp['discuss_reply_content'] = reply.discuss_reply_content
                temp['discuss_reply_time'] = reply.discuss_reply_time
                replies_result.append(temp)


        result['replies'] = replies_result

        user_other_discuss = []
        user_discuss_set = Discuss.objects.filter(user_id_id=author.id).order_by("-discuss_id")[:10]
        for user_discuss in user_discuss_set:
            if user_discuss.discuss_id != discuss_id:
                temp2 = {}
                temp2["discuss_id"] = user_discuss.discuss_id
                temp2["discuss_title"] = user_discuss.discuss_title
                user_other_discuss.append(temp2)

        result['user_other_discuss'] = user_other_discuss
        discuss.discuss_click_num = discuss.discuss_click_num + 1
        discuss.discuss_hot_num = discuss.discuss_hot_num + 10
        discuss.save()

        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def add_discuss_reply(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.user.username
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 2,
                "message": "请先登录哦"
            })
        user_id = user.id
        reply_topic_id = int(data.get("discuss_id"))
        reply_content = data.get("discuss_reply_content")
        reply_time = datetime.now()
        group_id = Discuss.objects.get(discuss_id=reply_topic_id).group_id
        check_focus = FocusDiscuss.objects.filter(focus_user=user_id, focus_discuss=reply_topic_id).exists()
        check_group_member = GroupMember.objects.filter(group_id=group_id, group_user_id=user_id).exists()
        if reply_content.strip() == '':
            return JsonResponse({
                "status": 4,
                "message": "回复不能为空"
            })
        elif check_focus is False and check_group_member is False:
            return JsonResponse({
                "status": 3,
                "message": "加入该小组或加入此讨论帖后才能回帖"
            })
        elif user_id is not None and reply_topic_id is not None and reply_content is not None:
            try:
                cursor.execute("insert into forum_discuss_reply(discuss_user_id_id,discuss_reply_discuss_id_id,\
                    discuss_reply_content,discuss_reply_time) values(%s,%s,%s,%s);",(user_id,reply_topic_id,reply_content,reply_time))
                #new_reply = DiscussReply.objects.create(discuss_user_id_id=user_id, discuss_reply_discuss_id_id=reply_topic_id,
                #                                        discuss_reply_content=reply_content, discuss_reply_time=reply_time)
                discuss = Discuss.objects.get(discuss_id=reply_topic_id)
                discuss.discuss_reply_num = discuss.discuss_reply_num + 1
                discuss.discuss_hot_num = discuss.discuss_hot_num + 90
                discuss.discuss_reply_time = reply_time
                discuss.save()
                user.user_credit = user.user_credit + 1
                user.save()
                author = User.objects.get(id=discuss.user_id_id)
                message_content = "您的小组讨论\""+ discuss.discuss_title + "\"有了新回复"
                cursor.execute("insert into forum_message(message_send_user_id,message_receive_user_id,\
                    message_related_type,message_related_id,message_content,message_read,message_time) \
                        values (%s,%s,%s,%s,%s,'f',now());",(user.id,author.id,2,discuss.discuss_id,message_content))
                #new_message = Message.objects.create(message_send_user_id=user.id, message_receive_user_id=author.id,
                #                                     message_related_type=2, message_related_id=discuss.discuss_id,
                #                                     message_content=message_content)
                return JsonResponse({
                    "status": 0,
                    "message": "发布回复成功"
                })
            except:
                return JsonResponse({
                    "status": 5,
                    "message": "发布回复失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def delete_discuss_reply(request):
    if request.method == "POST":
        data = json.loads(request.body)
        discuss_reply_id = data.get("discuss_reply_id")
        reply = DiscussReply.objects.get(discuss_reply_id=discuss_reply_id)
        reply_discuss_id = reply.discuss_reply_discuss_id_id
        user = User.objects.get(id=reply.discuss_user_id_id)
        if discuss_reply_id is not None:
            try:
                DiscussReply.objects.filter(discuss_reply_id=discuss_reply_id).delete()
                discuss = Discuss.objects.get(discuss_id=reply_discuss_id)
                discuss.discuss_reply_num = discuss.discuss_reply_num - 1
                discuss.discuss_hot_num = discuss.discuss_hot_num - 90
                discuss.save()
                user.user_credit = user.user_credit - 1
                user.save()

                return JsonResponse({
                    "status": 0,
                    "message": "删除回复成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "删除回复失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def add_discuss(request):
    if request.method == "POST":
        username = request.user.username
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 3,
                "message": "请先登录哦"
            })
        if(request.POST.get("group_id") == ''):
            return JsonResponse({
                "status": 4,
                "message": "请选择板块！"
            })

        user_id = user.id
        group_id = int(request.POST.get("group_id"))
        result = GroupMember.objects.filter(group_id=group_id, group_user_id=user_id)
        if(result.exists() == False):
            return JsonResponse({
                "status": 5,
                "message": "加入该小组后才能发帖"
            })

        discuss_title = request.POST.get("discuss_title")
        discuss_content = request.POST.get("discuss_content")
        discuss_time = datetime.now()
        file = request.FILES.get("file")
        file_check = False
        if file is not None:
            try:
                file_check = True
                file_name = file.name
                with transaction.atomic():
                    cursor.execute("insert into forum_file(user_id_id,file_name,file_url) \
                        values (%s,%s,%s);",(user.id,file_name,file))
                    new_file = ForumFile.objects.latest('file_id')
                #new_file = ForumFile.objects.create(user_id_id=user.id, file_name=file_name,
                #                                    file_url=file)
                file_id = new_file.file_id
            except:
                return JsonResponse({
                    "status": 7,
                    "message": "附件上传失败"
                })
        if discuss_title.strip() == '':
            return JsonResponse({
                "status": 6,
                "message": "标题不能为空"
            })
        elif user_id is not None and group_id is not None and discuss_title is not None and discuss_content is not None :
            try:
                with transaction.atomic():
                    cursor.execute("insert into forum_discuss(group_id_id,user_id_id,discuss_title,\
                        discuss_content,discuss_time,discuss_reply_time,discuss_click_num,discuss_reply_num,\
                            discuss_hot_num,discuss_content_file_check) values (%s,%s,%s,%s,%s,%s,0,0,0,'f');",
                            (group_id,user_id,discuss_title,discuss_content,discuss_time,discuss_time))
                    new_discuss = Discuss.objects.latest('discuss_id')
                #new_discuss = Discuss.objects.create(group_id_id=group_id, user_id_id=user_id, discuss_title=discuss_title,
                #                                   discuss_content=discuss_content, discuss_time=discuss_time, discuss_reply_time=discuss_time)
                user.user_credit = user.user_credit + 5
                user.save()
                if file_check is True:
                    new_discuss.discuss_content_file_check = True
                    new_discuss.discuss_file_id_id = file_id
                    new_discuss.save()
                return JsonResponse({
                    "discuss_id": new_discuss.discuss_id,
                    "status": 0,
                    "message": "发布小组讨论成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "发布小组讨论失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def user_discuss_detail(request):
    if request.method == "GET":
        get_username = request.GET.get('user')
        user = User.objects.get(username=get_username)
        result = {}
        result['user_id'] = user.id
        result['username'] = user.username
        discuss_result = []
        if(Discuss.objects.filter(user_id=user.id).count() != 0):
            discuss_set = Discuss.objects.filter(user_id=user.id).order_by("-discuss_id")
            for discuss in discuss_set:
                temp = {}
                temp['discuss_id'] = discuss.discuss_id
                temp['user_id'] = user.id
                temp['discuss_username'] = user.username
                temp['discuss_title'] = discuss.discuss_title
                temp['discuss_time'] = discuss.discuss_time
                temp['group_name'] = Group.objects.get(group_id=discuss.group_id_id).group_name
                temp['discuss_reply_time'] = discuss.discuss_reply_time
                temp['discuss_reply_num'] = discuss.discuss_reply_num
                discuss_result.append(temp)

        result['discuss'] = discuss_result

        replies_result = []
        if(DiscussReply.objects.filter(discuss_user_id=user.id).count() != 0):
            replies = DiscussReply.objects.filter(discuss_user_id=user.id).order_by("-discuss_reply_id")
            for reply in replies:
                temp = {}
                reply_discuss = Discuss.objects.get(discuss_id=reply.discuss_reply_discuss_id_id)
                temp['reply_id'] = reply.discuss_reply_id
                temp['user_id'] = user.id
                temp['reply_username'] = user.username
                temp['reply_discuss_id'] = reply_discuss.discuss_id
                temp['reply_discuss_title'] = reply_discuss.discuss_title
                temp['reply_content'] = reply.discuss_reply_content
                temp['reply_time'] = reply.discuss_reply_time
                replies_result.append(temp)

        result['replies'] = replies_result
        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def praise(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.user.username
        type = int(data.get("type"))
        content_id = int(data.get("content_id"))
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 5,
                "message": "请先登录哦"
            })
        check_like = Like.objects.filter(like_type=type, like_user_id=user.id, like_content_id=content_id)
        if check_like.exists():
                return JsonResponse({
                    "status": 3,
                    "message": "您已对该内容点赞"
                })
        if type == 1:
            try:
                topic = Topic.objects.get(topic_id=content_id)
                if topic.user_id_id == user.id:
                    return JsonResponse({
                        "status": 4,
                        "message": "不能给自己点赞哦~"
                    })
                cursor.execute("insert into forum_like(like_type,like_user_id_id,like_content_id) values\
                    (%s,%s,%s);",(type,user.id,content_id))
                #Like.objects.create(like_type=type, like_user_id_id=user.id, like_content_id=content_id)
                topic.topic_like_num = topic.topic_like_num + 1
                topic.topic_hot_num = topic.topic_hot_num + 25
                topic.save()
                topic_user = User.objects.get(id=topic.user_id_id)
                topic_user.user_credit = topic_user.user_credit + 2
                topic_user.save()
                return JsonResponse({
                    "status": 0,
                    "message": "点赞成功~"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "点赞失败"
                })
        elif type == 2:
            try:
                reply = Reply.objects.get(reply_id=content_id)
                if reply.user_id_id == user.id:
                    return JsonResponse({
                        "status": 4,
                        "message": "不能给自己点赞哦~"
                    })
                cursor.execute("insert into forum_like(like_type,like_user_id_id,like_content_id) values\
                (%s,%s,%s);",(type,user.id,content_id))
                #Like.objects.create(like_type=type, like_user_id_id=user.id, like_content_id=content_id)
                reply.reply_like_num = reply.reply_like_num + 1
                reply.save()
                return JsonResponse({
                    "status": 0,
                    "message": "点赞成功~"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "点赞失败"
                })
        else:
            return JsonResponse({
                "status": 2,
                "message": "点赞失败"
            })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def collect(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.user.username
        topic_id = int(data.get("topic_id"))
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 4,
                "message": "请先登录哦"
            })
        check_collect = Collect.objects.filter(user_id=user.id, topic_id=topic_id)
        if check_collect.exists():
                return JsonResponse({
                    "status": 3,
                    "message": "您已收藏该主题"
                })
        try:
            cursor.execute("insert into forum_collect(user_id_id,topic_id_id) values \
                (%s,%s)",(user.id,topic_id))
            #Collect.objects.create(user_id_id=user.id, topic_id_id=topic_id)
            topic = Topic.objects.get(topic_id=topic_id)
            topic.topic_collect_num = topic.topic_collect_num + 1
            topic.topic_hot_num = topic.topic_hot_num + 25
            topic.save()
            topic_user = User.objects.get(id=topic.user_id_id)
            topic_user.user_credit = topic_user.user_credit + 2
            topic_user.save()
            return JsonResponse({
                "status": 0,
                "message": "收藏成功~"
            })
        except:
            return JsonResponse({
                "status": 2,
                "message": "收藏失败"
            })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def delete_collect(request):
    if request.method == "POST":
        data = json.loads(request.body)
        topic_id = data.get("collect_topic_id")
        username = request.user.username
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 3,
                "message": "请先登录哦"
            })
        user_id = user.id
        if topic_id is not None and user_id is not None:
            try:
                Collect.objects.filter(user_id_id=user.id, topic_id_id=topic_id).delete()
                topic = Topic.objects.get(topic_id=topic_id)
                topic.topic_collect_num = topic.topic_collect_num - 1
                topic.topic_hot_num = topic.topic_hot_num - 25
                topic.save()
                topic_user = User.objects.get(id=topic.user_id_id)
                topic_user.user_credit = topic_user.user_credit - 2
                topic_user.save()

                return JsonResponse({
                    "status": 0,
                    "message": "删除收藏成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "删除收藏失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def user_collect(request):
    if request.method == "GET":
        get_username = request.GET.get('user')
        user = User.objects.get(username=get_username)
        result = {}
        result['user_id'] = user.id
        result['username'] = user.username
        collect_result = []
        if(Collect.objects.filter(user_id=user.id).count() != 0):
            collect_set = Collect.objects.filter(user_id=user.id).order_by("-collect_id")
            for collect in collect_set:
                topic = Topic.objects.get(topic_id=collect.topic_id_id)
                temp = {}
                temp['topic_id'] = topic.topic_id
                temp['topic_title'] = topic.topic_title
                temp['topic_time'] = topic.topic_time
                temp['section_name'] = Section.objects.get(section_id=topic.section_id_id).section_name
                temp['topic_reply_time'] = topic.topic_reply_time
                temp['topic_reply_num'] = topic.topic_reply_num
                collect_result.append(temp)

        result['collect'] = collect_result

        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def follow(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.user.username
        follow_on_user_id = int(data.get("follow_on_user"))
        try:
            follow_by_user = User.objects.get(username=username)
            follow_on_user = User.objects.get(id=follow_on_user_id)
        except:
            return JsonResponse({
                "status": 4,
                "message": "请先登录哦"
            })
        check_follow = Follow.objects.filter(follow_by_user=follow_by_user.id, follow_on_user=follow_on_user.id)
        if check_follow.exists():
            return JsonResponse({
                "status": 3,
                "message": "您已关注该用户"
            })
        if follow_by_user.id == follow_on_user.id:
            return JsonResponse({
                "status": 5,
                "message": "不能关注自己哦~"
            })
        try:
            cursor.execute("insert into forum_follow(follow_by_user_id,follow_on_user_id) values\
                (%s,%s);",(follow_by_user.id,follow_on_user.id))
            #Follow.objects.create(follow_by_user_id=follow_by_user.id, follow_on_user_id=follow_on_user.id)
            follow_on_user.user_credit = follow_on_user.user_credit + 2
            follow_on_user.save()
            return JsonResponse({
                "status": 0,
                "message": "关注成功~"
            })
        except:
            return JsonResponse({
                "status": 2,
                "message": "关注失败"
            })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def unfollow(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.user.username
        follow_on_user_id = int(data.get("follow_on_user"))
        try:
            follow_by_user = User.objects.get(username=username)
            follow_on_user = User.objects.get(id=follow_on_user_id)
        except:
            return JsonResponse({
                "status": 4,
                "message": "请先登录哦"
            })
        if follow_by_user is not None and follow_on_user is not None:
            try:
                Follow.objects.filter(follow_by_user=follow_by_user.id, follow_on_user=follow_on_user.id).delete()
                follow_on_user.user_credit = follow_on_user.user_credit - 2
                follow_on_user.save()

                return JsonResponse({
                    "status": 0,
                    "message": "取消关注成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "取消关注失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def user_following(request):
    if request.method == "GET":
        get_username = request.GET.get('user')
        user = User.objects.get(username=get_username)
        result = {}
        result['user_id'] = user.id
        result['username'] = user.username
        follow_result = []
        if(Follow.objects.filter(follow_by_user=user.id).count() != 0):
            follow_set = Follow.objects.filter(follow_by_user=user.id)
            for follow in follow_set:
                follow_on_user = User.objects.get(id=follow.follow_on_user_id)
                temp = {}
                temp['follow_user_id'] = follow_on_user.id
                temp['follow_user_username'] = follow_on_user.username
                temp['follow_user_avatar'] = str(follow_on_user.user_avatar)
                temp['follow_user_credit'] = follow_on_user.user_credit
                temp['follow_user_post_num'] = Topic.objects.filter(user_id_id=follow_on_user.id).count()
                temp['follow_user_reply_num'] = Reply.objects.filter(user_id_id=follow_on_user.id).count()
                follow_result.append(temp)

        result['follow'] = follow_result

        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def user_follower(request):
    if request.method == "GET":
        get_username = request.GET.get('user')
        user = User.objects.get(username=get_username)
        result = {}
        result['user_id'] = user.id
        result['username'] = user.username
        follow_result = []
        if(Follow.objects.filter(follow_on_user=user.id).count() != 0):
            follow_set = Follow.objects.filter(follow_on_user=user.id)
            for follow in follow_set:
                follow_by_user = User.objects.get(id=follow.follow_by_user_id)
                temp = {}
                temp['follow_user_id'] = follow_by_user.id
                temp['follow_user_username'] = follow_by_user.username
                temp['follow_user_avatar'] = str(follow_by_user.user_avatar)
                temp['follow_user_credit'] = follow_by_user.user_credit
                temp['follow_user_post_num'] = Topic.objects.filter(user_id_id=follow_by_user.id).count()
                temp['follow_user_reply_num'] = Reply.objects.filter(user_id_id=follow_by_user.id).count()
                if_following = Follow.objects.filter(follow_on_user=follow_by_user.id, follow_by_user=user.id)
                if(if_following.exists()):
                    temp['follow_user_if_following'] = 1
                else:
                    temp['follow_user_if_following'] = 0
                follow_result.append(temp)

        result['follow'] = follow_result

        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def focus_discuss(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.user.username
        discuss_id = int(data.get("discuss_id"))
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 4,
                "message": "请先登录哦"
            })
        check_focus = FocusDiscuss.objects.filter(focus_user=user.id, focus_discuss=discuss_id)
        if check_focus.exists():
                return JsonResponse({
                    "status": 3,
                    "message": "您已加入该讨论"
                })
        try:
            cursor.execute("insert into forum_focus_discuss(focus_user_id,focus_discuss_id) \
                values(%s,%s);",(user.id,discuss_id))
            #FocusDiscuss.objects.create(focus_user_id=user.id, focus_discuss_id=discuss_id)
            return JsonResponse({
                "status": 0,
                "message": "加入成功,现在可以参与讨论了~"
            })
        except:
            return JsonResponse({
                "status": 2,
                "message": "加入失败"
            })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def user_focus(request):
    if request.method == "GET":
        get_username = request.GET.get('user')
        user = User.objects.get(username=get_username)
        result = {}
        result['user_id'] = user.id
        result['username'] = user.username
        focus_result = []
        if(FocusDiscuss.objects.filter(focus_user=user.id).count() != 0):
            focus_set = FocusDiscuss.objects.filter(focus_user=user.id)
            for focus in focus_set:
                discuss = Discuss.objects.get(discuss_id=focus.focus_discuss_id)
                temp = {}
                temp['discuss_id'] = discuss.discuss_id
                temp['discuss_title'] = discuss.discuss_title
                temp['discuss_time'] = discuss.discuss_time
                temp['discuss_reply_num'] = discuss.discuss_reply_num
                focus_result.append(temp)

        result['focus'] = focus_result

        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def apply_join_group(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.user.username
        group_id = int(data.get("group_id"))
        group = Group.objects.get(group_id=group_id)
        apply_message = data.get("apply_message")
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 4,
                "message": "请先登录哦"
            })
        check_join = GroupMember.objects.filter(group_id=group.group_id, group_user_id=user.id)
        if check_join.exists():
            return JsonResponse({
                "status": 3,
                "message": "您已加入该小组"
            })
        check_apply = GroupApply.objects.filter(group_id=group.group_id, group_user_id=user.id)
        if check_apply.exists():
            return JsonResponse({
                "status": 5,
                "message": "正在等待小组长同意中，请不要重复申请~"
            })
        try:
            cursor.execute("insert into forum_group_apply(group_id_id,group_user_id_id,\
                group_apply_message) values (%s,%s,%s);",(group.group_id,user.id,apply_message))
            #GroupApply.objects.create(group_id_id=group.group_id, group_user_id_id=user.id,
            #                          group_apply_message=apply_message)
            return JsonResponse({
                "status": 0,
                "message": "申请提交成功,请等待小组长同意~"
            })
        except:
            return JsonResponse({
                "status": 2,
                "message": "申请提交失败"
            })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def user_receive_apply(request):
    if request.method == "GET":
        get_username = request.user.username
        try:
            user = User.objects.get(username=get_username)
        except:
            return JsonResponse({
                "status": 2,
                "message": "请先登录哦"
            })

        result = {}
        result['user_id'] = user.id
        result['username'] = user.username
        user_groups = Group.objects.filter(group_owner_id=user.id)
        groups_id = []
        if user_groups.exists() is False:
            result['apply'] = []
            return JsonResponse({"status": 0, "data": result})
        for user_group in user_groups:
            groups_id.append(user_group.group_id)
        apply_result = []
        if(GroupApply.objects.filter(group_id__in=groups_id).count() != 0):
            apply_set = GroupApply.objects.filter(group_id__in=groups_id).order_by("-group_apply_id")
            for apply in apply_set:
                temp = {}
                temp['apply_id'] = apply.group_apply_id
                temp['apply_group_name'] = Group.objects.get(group_id=apply.group_id_id).group_name
                temp['apply_username'] = User.objects.get(id=apply.group_user_id_id).username
                temp['apply_message'] = apply.group_apply_message
                apply_result.append(temp)

        result['apply'] = apply_result

        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def handle_apply(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.user.username
        handle_user = User.objects.get(username=username)
        group_apply_id = int(data.get("group_apply_id"))
        group_apply = GroupApply.objects.get(group_apply_id=group_apply_id)
        group = Group.objects.get(group_id=group_apply.group_id_id)
        apply_user = User.objects.get(id=group_apply.group_user_id_id)
        handle_result = int(data.get("handle_result"))
        if(handle_user.id != group.group_owner_id_id):
            return JsonResponse({
                "status": 3,
                "message": "您不是小组所有人，无法操作"
            })

        check_join = GroupMember.objects.filter(group_id=group.group_id, group_user_id=apply_user.id)
        if check_join.exists():
            return JsonResponse({
                "status": 4,
                "message": "对方已加入该小组"
            })

        if(handle_result == 1):
            try:
                cursor.execute("insert into forum_group_member(group_id_id,group_user_id_id) values\
                    (%s,%s);",(group.group_id,apply_user.id))
                #GroupMember.objects.create(group_id_id=group.group_id, group_user_id_id=apply_user.id)
                GroupApply.objects.get(group_apply_id=group_apply_id).delete()
                message_content = "申请加入小组["+ group.group_name + "]已通过"
                cursor.execute("insert into forum_message(message_send_user_id,message_receive_user_id,\
                    message_related_type,message_content,message_read,message_time) \
                        values (%s,%s,%s,%s,'f',now());",(handle_user.id,apply_user.id,0,message_content))
                #new_message = Message.objects.create(message_send_user_id=handle_user.id, message_receive_user_id=apply_user.id,
                #                                     message_content=message_content)
                return JsonResponse({
                    "status": 0,
                    "message": "已批准加入~"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "操作失败"
                })
        elif(handle_result == 0):
            try:
                GroupApply.objects.get(group_apply_id=group_apply_id).delete()
                message_content = "申请加入小组["+ group.group_name + "]已被拒绝"
                cursor.execute("insert into forum_message(message_send_user_id,message_receive_user_id,\
                    message_related_type,message_content,message_read,message_time) \
                        values (%s,%s,%s,%s,'f',now());",(handle_user.id,apply_user.id,0,message_content))
                #new_message = Message.objects.create(message_send_user_id=handle_user.id, message_receive_user_id=apply_user.id,
                #                                     message_content=message_content)
                return JsonResponse({
                    "status": 0,
                    "message": "已拒绝申请"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "操作失败"
                })
        else:
            return JsonResponse({
                "status": 2,
                "message": "失败"
            })


    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def recommend_group(request):
    if request.method == "GET":
        username = request.GET.get('user')
        user = User.objects.get(username=username)
        join_group_records = GroupMember.objects.filter(group_user_id_id=user.id)
        result = []
        if(join_group_records.exists() == False):
            groups = Group.objects.all().order_by("group_id")[:5]
            for group in groups:
                if (GroupMember.objects.filter(group_id=group.group_id, group_user_id=user.id).exists() == False):
                    temp = {}
                    temp["id"] = group.group_id
                    temp["name"] = group.group_name
                    result.append(temp)
            return JsonResponse({"status": 0, "data": result})

        user_join_groups = set() #当前用户加入的组集合
        user_join_groups_id = [] #当前用户加入的组的id数组
        for join_group_record in join_group_records:
            group = Group.objects.get(group_id=join_group_record.group_id_id)
            user_join_groups.add(group) #获取当前用户加入的组集合

        calculate_users = set() #需计算相似度的用户

        for user_join_group in user_join_groups:
            user_join_groups_id.append(user_join_group.group_id)
            simple_join_records = GroupMember.objects.filter(group_id_id=user_join_group.group_id)
            for simple_join_record in simple_join_records:
                calculate_users.add(simple_join_record.group_user_id_id) #获取需计算相似度的用户

        calculate_users.remove(user.id)  #排除用户自身
        sim_dict = {} #用户相似度dict

        for calculate_user in calculate_users: #相似度计算
            cal_user = User.objects.get(id=calculate_user)
            cal_user_join_group = []
            cal_user_join_records = GroupMember.objects.filter(group_user_id_id=cal_user.id)
            for cal_user_join_record in cal_user_join_records:
                temp_group = Group.objects.get(group_id=cal_user_join_record.group_id_id)
                cal_user_join_group.append(temp_group)
            intersection_group = user_join_groups.intersection(cal_user_join_group)
            sim_value = float(len(intersection_group)) / (len(user_join_groups) + len(cal_user_join_group) - len(intersection_group))
            sim_dict[calculate_user] = sim_value

        print("相似用户相似度:")
        for key in sim_dict:
            print("用户: " + User.objects.get(id=key).username + " 相似度： " + str(sim_dict[key]))

        sorted_sim_dict = dict(sorted(sim_dict.items(), key=lambda item: item[1], reverse=True)) #排序

        sim_users = set() #相似度最高的5个用户集合
        required_cnt = 5
        cnt = 0
        for key, value in sorted_sim_dict.items(): #获取相似度最高的5个用户
            cnt += 1
            if cnt > required_cnt:
                break
            sim_users.add(key)


        group_score = {} #小组推荐值dict
        for sim_user in sim_users: #计算小组推荐值
            sim_user_groups_records = GroupMember.objects.filter(group_user_id_id=sim_user)
            for sim_user_group_record in sim_user_groups_records:
                sim_user_group = Group.objects.get(group_id=sim_user_group_record.group_id_id)
                if sim_user_group.group_id not in user_join_groups_id:
                    if sim_user_group in group_score.keys():
                        group_score[sim_user_group.group_id] = group_score[sim_user_group.group_id] + sim_dict[sim_user]
                    else:
                        group_score[sim_user_group.group_id] = sim_dict[sim_user]
        print("小组推荐值：")
        for key in group_score:
            print("小组: " + Group.objects.get(group_id=key).group_name + " 推荐值： " + str(group_score[key]))

        sorted_sim_dict = dict(sorted(sim_dict.items(), key=lambda item: item[1], reverse=True))  # 排序

        sorted_group_score = dict(sorted(group_score.items(), key=lambda item: item[1], reverse=True)) #按推荐值排序
        rec_groups_id = []
        required_groups_cnt = 8
        groups_cnt = 0
        for key, value in sorted_group_score.items(): #取推荐值最高的前八个小组
            groups_cnt += 1
            if groups_cnt > required_groups_cnt:
                break
            rec_groups_id.append(key)

        if len(rec_groups_id) == 0:
            groups = Group.objects.all().order_by("group_id")[:5]
            for group in groups:
                if (GroupMember.objects.filter(group_id=group.group_id, group_user_id=user.id).exists() == False):
                    temp = {}
                    temp["id"] = group.group_id
                    temp["name"] = group.group_name
                    result.append(temp)
            return JsonResponse({"status": 0, "data": result})

        for rec_group_id in rec_groups_id:
            rec_group = Group.objects.get(group_id=rec_group_id)
            temp = {}
            temp["id"] = rec_group.group_id
            temp["name"] = rec_group.group_name
            result.append(temp)


        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def add_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.user.username
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 4,
                "message": "请先登录哦"
            })
        user_id = user.id
        receive_username = data.get("receive_username")
        try:
            receive_user = User.objects.get(username=receive_username)
        except:
            return JsonResponse({
                "status": 6,
                "message": "找不到该用户，请检查输入的用户名"
            })
        message_content = data.get("message_content")
        if user.user_credit < 20 and user.type == 'S':
            return JsonResponse({
                "status": 5,
                "message": "贡献度不足，请提高贡献度到20以上"
            })

        if message_content is None or message_content.strip() == '':
            return JsonResponse({
                "status": 3,
                "message": "内容不能为空"
            })
        if message_content is not None:
            try:
                cursor.execute("insert into forum_message(message_send_user_id,message_receive_user_id,\
                    message_related_type,message_content,message_read,message_time) \
                        values (%s,%s,%s,%s,'f',now());",(user.id,receive_user.id,0,message_content))
                #new_message = Message.objects.create(message_send_user_id=user.id, message_receive_user_id=receive_user.id,
                #                                     message_content=message_content)
                return JsonResponse({
                    "status": 0,
                    "message": "发送成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "发送失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def user_message(request):
    if request.method == "GET":
        username = request.user.username
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 4,
                "message": "请先登录哦"
            })
        result = {}
        result['user_id'] = user.id
        result['username'] = user.username
        message_result = []
        if(Message.objects.filter(message_receive_user=user.id).count() != 0):
            message_set = Message.objects.filter(message_receive_user=user.id).order_by("-message_id")
            for message in message_set:
                send_user = User.objects.get(id=message.message_send_user_id)
                temp = {}
                temp['message_id'] = message.message_id
                temp['message_send_user'] = send_user.username
                temp['message_receive_user'] = user.username
                temp['message_read'] = message.message_read
                temp['message_content'] = message.message_content
                temp['message_time'] = message.message_time
                temp['message_related_type'] = message.message_related_type
                temp['message_related_id'] = message.message_related_id
                message_result.append(temp)

        result['message'] = message_result

        return JsonResponse({"status": 0, "data": result})
    else:
        return JsonResponse({"status": 1, "message": "请求方法错误！"})


def delete_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.user.username
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 4,
                "message": "请先登录哦"
            })
        message_id = data.get("message_id")
        message = Message.objects.get(message_id=message_id)
        if message is None or message.message_receive_user_id != user.id:
            return JsonResponse({
                "status": 3,
                "message": "无权限"
            })
        if message is not None:
            try:
                Message.objects.filter(message_id=message_id).delete()

                return JsonResponse({
                    "status": 0,
                    "message": "删除消息成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "删除消息失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def read_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.user.username
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 4,
                "message": "请先登录哦"
            })
        message_id = data.get("message_id")
        message = Message.objects.get(message_id=message_id)
        if message is None or message.message_receive_user_id != user.id:
            return JsonResponse({
                "status": 3,
                "message": "无权限"
            })
        if message is not None:
            try:
                if message.message_read is False:
                    message.message_read = True
                    message.save()
                return JsonResponse({
                    "status": 0,
                    "message": "消息标记成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "消息标记失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def user_rank(request):
    if request.method == "GET":
        user_set = User.objects.all().order_by("-user_credit")[:10]
        result = []
        for user in user_set:
            temp = {}
            temp['user_id'] = user.id
            temp['username'] = user.username
            temp['user_credit'] = user.user_credit
            result.append(temp)
        return JsonResponse({"status": 0, "data": result})


    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def topic_rank(request):
    if request.method == "GET":
        section = int(request.GET.get('section', default=1))
        topic_set = Topic.objects.filter(section_id_id=section).order_by("-topic_hot_num")[:10]
        result = []
        for topic in topic_set:
            temp = {}
            temp['topic_id'] = topic.topic_id
            temp['topic_title'] = topic.topic_title
            temp['topic_hot_num'] = topic.topic_hot_num
            result.append(temp)
        return JsonResponse({"status": 0, "data": result})


    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def update_user_info(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = request.user.username
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 4,
                "message": "请先登录哦"
            })
        user_edu = data.get("user_edu")
        user_addr = data.get("user_addr")
        user_tel = data.get("user_tel")
        try:
            user.user_edu = user_edu
            user.user_addr = user_addr
            user.user_tel = user_tel
            user.save()
            return JsonResponse({
                "status": 0,
                "message": "更新成功"
            })
        except:
            return JsonResponse({
                "status": 2,
                "message": "更新失败"
            })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def update_user_avatar(request):
    if request.method == "POST":
        username = request.user.username
        image = request.FILES.get('file')
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 4,
                "message": "请先登录哦"
            })
        if image is not None:
            try:
                # image_name = str(user.username) + "_avatar_" + str(int(time.time()))
                # f = open(os.path.join('media/avatar', image_name), 'wb')
                # for i in image.chunks():
                #     f.write(i)
                # f.close()
                user.user_avatar = image
                user.save()
                return JsonResponse({
                    "status": 0,
                    "message": "头像更换成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "头像更换失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def edit_discuss(request):
    if request.method == "POST":
        username = request.user.username
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 3,
                "message": "请先登录哦"
            })

        user_id = user.id
        discuss_id = request.POST.get("discuss_id")
        discuss_title = request.POST.get("discuss_title")
        discuss_content = request.POST.get("discuss_content")
        if discuss_title.strip() == '':
            return JsonResponse({
                "status": 5,
                "message": "标题不能为空"
            })
        elif user_id is not None and discuss_title is not None and discuss_content is not None :
            try:
                discuss = Discuss.objects.get(discuss_id=discuss_id)
                if (discuss.user_id_id != user.id):
                    return JsonResponse({
                        "status": 4,
                        "message": "无权限"
                    })
                discuss.discuss_title = discuss_title
                discuss.discuss_content = discuss_content
                discuss.save()
                return JsonResponse({
                    "discuss_id": discuss_id,
                    "status": 0,
                    "message": "编辑成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "编辑失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def edit_topic(request):
    if request.method == "POST":
        username = request.user.username
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({
                "status": 3,
                "message": "请先登录哦"
            })

        user_id = user.id
        topic_id = request.POST.get("topic_id")
        topic_title = request.POST.get("topic_title")
        topic_content = request.POST.get("topic_content")
        if topic_title.strip() == '':
            return JsonResponse({
                "status": 5,
                "message": "标题不能为空"
            })
        elif user_id is not None and topic_title is not None and topic_content is not None :
            try:
                topic = Topic.objects.get(topic_id=topic_id)
                if (topic.user_id_id != user.id):
                    return JsonResponse({
                        "status": 4,
                        "message": "无权限"
                    })
                topic.topic_title = topic_title
                topic.topic_content = topic_content
                topic.save()
                return JsonResponse({
                    "topic_id": topic_id,
                    "status": 0,
                    "message": "编辑成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "编辑失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })

def add_question_topic(request):
    if request.method == "POST":
        user = User.objects.get(username='admin')
        user_id = user.id
        section_id = 2
        data = json.loads(request.body)
        topic_title = data.get("question_title")
        topic_content = data.get("question_content")
        question_id = data.get("question_id")
        topic_time = datetime.now()
        if topic_title.strip() == '':
            return JsonResponse({
                "status": 3,
                "message": "标题不能为空"
            })
        elif user_id is not None and section_id is not None and topic_title is not None:
            try:
                with transaction.atomic():
                    cursor.execute("insert into forum_topic(section_id_id,user_id_id,topic_title,\
                    topic_time,topic_reply_time,topic_click_num,topic_reply_num,topic_collect_num,\
                        topic_like_num,topic_content,topic_content_file_check,topic_hot_num) values \
                            (%s,%s,%s,%s,%s,0,0,0,0,'','f',0); ",(section_id,user_id,topic_title,topic_time,topic_time))
                    cursor.execute("select currval('forum_topic_topic_id_seq') as id;")
                    topic_id = cursor.fetchone()[0]
                    cursor.execute("insert into forum_question(topic_id_id,question_id) values \
                        (%s,%s);",(topic_id,question_id))
                #new_topic = Topic.objects.create(section_id_id=section_id, user_id_id=user_id, topic_title=topic_title,
                #                                 topic_time=topic_time, topic_reply_time=topic_time)
                #new_question_topic = QuestionToTopic.objects.create(topic_id_id=new_topic.topic_id, question_id=question_id)
                return JsonResponse({
                    "status": 0,
                    "message": "发布成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "发布失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


def add_recommend_answer(request):
    if request.method == "POST":
        user = User.objects.get(username='admin')
        data = json.loads(request.body)
        user_id = user.id
        topic_id = data.get("topic_id")
        try:
            qtt = QuestionToTopic.objects.get(topic_id=topic_id)
        except:
            return JsonResponse({
                "status": 3,
                "message": "这个问题不是问答系统发布的"
            })
        question_id = qtt.question_id

        reply_content = data.get("reply_content")
        reply_time = datetime.now()
        question = Question.objects.get(question_id=question_id)
        if question.status == 3:
            return JsonResponse({
                "status": 4,
                "message": "这个问题有了最佳回复了哦"
            })
        if reply_content is not None:
            try:
                cursor.execute("insert into answer(context,time,score,status,from_forum,question_id,user_id)\
                    values(%s,%s,%s,%s,%s,%s,%s);",(reply_content,reply_time,0,1,True,question_id,user.id))
                #new_answer = Answer.objects.create(context=reply_content, time=reply_time, score=0,
                #                                   status=1, from_forum=true,question_id=question_id, user_id=user.id)
                question.number = question.number + 1
                question.save()
                return JsonResponse({
                    "status": 0,
                    "message": "推荐成功"
                })
            except:
                return JsonResponse({
                    "status": 2,
                    "message": "推荐失败"
                })

    else:
        return JsonResponse({
            "status": 1,
            "message": "请求方法错误！"
        })


