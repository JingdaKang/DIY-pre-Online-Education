import os
from random import Random
from django.utils import timezone
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from OnlineEducation.settings import BASE_DIR
from backend.models import *

from django.contrib import auth

import django.db
from django.db import connection
# Create your views here.
# 登录
def post_login(request):
    from django.contrib.auth.hashers import make_password, check_password
    response = {}
    username = request.POST.get('username')
    password = request.POST.get('password')
    type = request.POST.get('type')
    try:
        obj = auth.authenticate(request, username=username, password=password)
        if obj:
            # 登陆成功
            auth.login(request, obj)
            print(request.user.id)
        user1 = User.objects.get(username=username, type=type)
        if check_password(password, user1.password):
            if user1.is_active == False:
                response['code'] = 4
                return JsonResponse(response)
            response['code'] = 1
            response['id'] = user1.id
            response['username'] = user1.username
            response['type'] = user1.type
            return JsonResponse(response)
        response['code'] = 2
    except Exception as e:
        try:
            user2 = User.objects.get(email=username, type=type)
            if check_password(password, user2.password):
                if user2.is_active == False:
                    response['code'] = 4
                    return JsonResponse(response)
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
    cursor = connection.cursor()
    response = {}
    try:
        username = request.POST.get('username')
        email = request.POST.get('email')
        #user1 = User.objects.get(username=username)
        cursor.execute("select * from public.user where username=%s;",(username,))
        user1 = cursor.fetchone()
        cursor.execute("select * from public.user where email=%s;",(email,))
        user2 = cursor.fetchone()  
        print(user1,user2)
        if user1 != None:
            print('user1')
            response['code'] = 2
        elif user2 != None:
            print('user2')
            response['code'] = 3
        else: 
            raw_password = request.POST.get('password')
            password = make_password(raw_password)
            type = request.POST.get('type')
            #user_obj = User.objects.create_user(username=username, user_gender='D', email=email, password=password,
            #                                    type=type)
            cursor.execute("insert into public.user(username, password, email, user_gender, type, is_superuser,\
                            is_staff, is_active, date_joined, user_reg, score, user_status, user_following_num,\
                                user_follower_num, user_credit) values (%s,%s,%s,'D',%s,'f','f','t',current_date,now(),0,'t',0,0,0);",
                                (username,password,email,type))
            print('insert')
            cursor.execute("select id from public.user where username=%s;",(username,))
            userid = cursor.fetchone()
            print(userid)
            #NoteBook.objects.create(note_name='默认笔记本', creator_id=user_obj)
            #NoteBook.objects.create(note_name='优质问答笔记本', creator_id=user_obj)
            cursor.execute("insert into tb_notebook(notebook_name,notebook_create,notebook_modify,\
                        creator_id) values ('默认笔记本',now(),now(),%s)",(userid,))
            cursor.execute("insert into tb_notebook(notebook_name,notebook_create,notebook_modify,\
                        creator_id) values ('优质问答笔记本',now(),now(),%s)",(userid,))     
            if type == 'S':
                cursor.execute("insert into tb_tag(tag_name,tag_create,creator_id) \
                    values('错题本',now(),%s)",(userid,))
                #Tag.objects.create(tag_name='错题本', creator_id=user_obj)
            elif type == 'T':
                cursor.execute("insert into tb_tag(tag_name,tag_create,creator_id) \
                    values('优秀题解',now(),%s)",(userid,))
                #Tag.objects.create(tag_name='优秀题解', creator_id=user_obj)
            response['code'] = 1            
    except Exception as e:
        print(e)
        connection.rollback()
        response['code'] = 0
    finally:
        cursor.close()
    return JsonResponse(response)


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
    response = {}
    try:
        user_id = request.COOKIES.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if user:
            image_path = "media/"+str(user.user_avatar)
            image = open(image_path, "rb")
        return HttpResponse(image, content_type="image/jpeg;image/png")
    except Exception as e:
        image = open("media/avatar/default.png", "rb")
    return HttpResponse(image, content_type="image/jpeg;image/png")


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
            result = User.objects.filter(id=user_id).update(username=username, user_gender=gender,
                                                            user_edu=education,
                                                            user_addr=address, email=email,
                                                            user_tel=telephone)
        else:
            result = User.objects.filter(id=user_id).update(username=username, user_gender=gender,
                                                            user_bir=birthday, user_edu=education,
                                                            user_addr=address, email=email,
                                                            user_tel=telephone)
        if result:
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


# 更新头像
def upload_avatar(request):
    response = {}
    try:
        user_id = request.COOKIES.get('user_id')
        file = request.FILES.get("file", None)
        if not file:
            response['code'] = 0
            response['msg'] = '上传失败'
            return JsonResponse(response)
        dest_path = BASE_DIR + '/media/avatar/' + user_id + '/'

        if os.path.exists(dest_path):
            filepath = os.path.join(dest_path, file.name)
        else:
            os.mkdir(dest_path)
            filepath = os.path.join(dest_path, file.name)
        with open(filepath, 'wb') as fp:
            for part in file.chunks():
                fp.write(part)
        imgUrl = 'avatar/' + user_id + '/' + file.name
        User.objects.filter(id=user_id).update(user_avatar=imgUrl)
        response['code'] = 1
        response['msg'] = '上传成功'
    except Exception as e:
        response['code'] = 0
        response['msg'] = '上传失败'
    return JsonResponse(response)


def random_str(randomlength=6):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def reset_password(request):
    from OnlineEducation.settings import EMAIL_FROM
    response = {}
    username = request.POST.get("username")
    email = request.POST.get("email")
    try:
        user = User.objects.get(username=username, email=email)
        if user:
            new_pass = random_str()
            user.set_password(new_pass)
            user.save()
            email_title = "找回密码"
            # 随机生成的验证码
            email_body = "你好，{0}\n".format(username) + "新密码为：{0}".format(new_pass)
            send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
            response['code'] = 1
        else:
            response['code'] = 0
    except Exception as e:
        print(str(e))
        response['code'] = 0
    return JsonResponse(response)


def get_account(request):
    response = {}
    try:
        user_obj = User.objects.all().values()
        users = list(user_obj)
        response['accounts'] = users
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def contain(origin, keyword):
    if origin.find(keyword, 0, len(origin)) > -1:
        return True
    else:
        return False


def get_account_by_condition(request):
    response = {}
    condition_accounts = []
    name = request.POST.get('name')
    type = request.POST.get('type')
    status = request.POST.get('status')
    if status == 'True':
        status = True
    if status == 'False':
        status = False
    user_obj = User.objects.all().values()
    users = list(user_obj)
    try:
        if not name == '' and not type == '0' and not status == '0':
            for user in users:
                if contain(user['username'], name) and user['type'] == type and user['is_active'] == status:
                    condition_accounts.append(user)
        elif not name == '' and not type == '0':
            for user in users:
                if contain(user['username'], name) and user['type'] == type:
                    condition_accounts.append(user)
        elif not name == '' and not status == '0':
            for user in users:
                if contain(user['username'], name) and user['is_active'] == status:
                    condition_accounts.append(user)
        elif not type == '0' and not status == '0':
            for user in users:
                if user['type'] == type and user['is_active'] == status:
                    condition_accounts.append(user)
        elif not name == '':
            for user in users:
                if contain(user['username'], name):
                    condition_accounts.append(user)
        elif not type == '0':
            for user in users:
                if user['type'] == type:
                    condition_accounts.append(user)
        elif not status == '0':
            for user in users:
                if user['is_active'] == status:
                    condition_accounts.append(user)
        else:
            condition_accounts = users
        response['condition_accounts'] = condition_accounts
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def change_status(request):
    response = {}
    id = request.POST.get('id')
    try:
        user = User.objects.get(id=id)
        if user.is_active == True:
            User.objects.filter(id=id).update(is_active=False)
        else:
            User.objects.filter(id=id).update(is_active=True)
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def apply_class(request):
    response = {}
    user_id = request.POST.get('user_id')
    name = request.POST.get('name')
    stime = request.POST.get('stime')
    time = request.POST.get('time')
    maxnum = request.POST.get('maxnum')
    reason = request.POST.get('reason')
    try:
        user = User.objects.get(id=user_id)
        course_obj = user.examcourse_set.all().values()
        courses = list(course_obj)
        for course in courses:
            if course['name'] == name:
                response['code'] = 2
                response['msg'] = '你已创建该课程'
                return JsonResponse(response)
        apply_item = Apply_Class(tid=user, name=name, stime=stime, time=time, maxnum=maxnum, reason=reason)
        apply_item.save()
        response['code'] = 1
    except Exception as e:
        print(e)
        response['code'] = 0
    return JsonResponse(response)


def get_apply_classes(request):
    response = {}
    try:
        apply_obj = Apply_Class.objects.all().values()
        applies = list(apply_obj)
        for apply in applies:
            user = User.objects.get(id=apply['tid_id'])
            apply['teacher'] = user.username
        response['classes'] = applies
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def get_apply_class_by_condition(request):
    response = {}
    condition_apply = []
    name = request.POST.get('name')
    teacher = request.POST.get('teacher')
    status = request.POST.get('status')
    print(teacher)
    try:
        apply_obj = Apply_Class.objects.all().values()
        applies = list(apply_obj)
        for apply in applies:
            user = User.objects.get(id=apply['tid_id'])
            apply['teacher'] = user.username
        if not name == '' and not teacher == '0' and not status == '':
            for apply in applies:
                if contain(apply['name'], name) and str(apply['tid_id']) == teacher and str(apply['status']) == status:
                    condition_apply.append(apply)
        elif not name == '' and not teacher == '0':
            for apply in applies:
                if contain(apply['name'], name) and str(apply['tid_id']) == teacher:
                    condition_apply.append(apply)
        elif not name == '' and not status == '':
            for apply in applies:
                if contain(apply['name'], name) and str(apply['status']) == status:
                    condition_apply.append(apply)
        elif not teacher == '0' and not status == '':
            for apply in applies:
                if str(apply['tid_id']) == teacher and str(apply['status']) == status:
                    condition_apply.append(apply)
        elif not name == '':
            for apply in applies:
                if contain(apply['name'], name):
                    condition_apply.append(apply)
        elif not teacher == '0':
            for apply in applies:
                if str(apply['tid_id']) == teacher:
                    condition_apply.append(apply)
        elif not status == '':
            for apply in applies:
                if str(apply['status']) == status:
                    condition_apply.append(apply)
        else:
            condition_apply = applies
        response['condition_apply'] = condition_apply
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def get_teacher(request):
    response = {}
    try:
        teacher_obj = User.objects.filter(type='T').values()
        teachers = list(teacher_obj)
        response['teacherList'] = teachers
        response['code'] = 1
    except Exception as e:
        print(e)
        response['code'] = 0
    return JsonResponse(response)


def get_my_class(request):
    response = {}
    id = request.POST.get('user_id')
    try:
        teacher = User.objects.get(id=id)
        course_obj = teacher.examcourse_set.all().values()
        courseList = list(course_obj)
        response['classes'] = courseList
        response['code'] = 1
    except Exception as e:
        print(e)
        response['code'] = 0
    return JsonResponse(response)


def get_my_class_by_condition(request):
    response = {}
    condition_class = []
    id = request.POST.get('user_id')
    name = request.POST.get('name')
    status = request.POST.get('status')
    try:
        teacher = User.objects.get(id=id)
        course_obj = teacher.examcourse_set.all().values()
        courses = list(course_obj)
        if not name == '' and not status == '':
            for course in courses:
                if contain(course['name'], name) and str(course['status']) == status:
                    condition_class.append(course)
        elif not name == '':
            for course in courses:
                if contain(course['name'], name):
                    condition_class.append(course)
        elif not status == '':
            for course in courses:
                if str(course['status']) == status:
                    condition_class.append(course)
        else:
            condition_class = courses
        response['condition_class'] = condition_class
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def get_all_class(request):
    response = {}
    user_id = request.POST.get('user_id')
    try:
        course_obj = ExamCourse.objects.all().values()
        courses = list(course_obj)
        for course in courses:
            teacher = User.objects.get(id=course['tid_id'])
            course_obj = ExamCourse.objects.get(id=course['id'])
            course['teacher'] = teacher.username
            student = User.objects.get(id=user_id)
            record = StudentChooseCourse.objects.filter(uid=student, cid=course_obj)
            apply = Operate_Class.objects.filter(user_id=student, class_id=course_obj, type='J')
            if record:
                record_item = StudentChooseCourse.objects.get(uid=student, cid=course_obj)
                if record_item.status == 1:
                    course['choose'] = 1
                else:
                    course['choose'] = 0
            else:
                course['choose'] = 0
            if apply:
                apply_item = Operate_Class.objects.get(user_id=student, class_id=course_obj, type='J')
                if apply_item.status == 1:
                    course['operate'] = 1
            else:
                course['operate'] = 0
        response['classes'] = courses
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def get_all_class_by_condition(request):
    response = {}
    condition_class = []
    user_id = request.POST.get('user_id')
    name = request.POST.get('name')
    tid = request.POST.get('teacher')
    status = request.POST.get('status')
    try:
        course_obj = ExamCourse.objects.all().values()
        courses = list(course_obj)
        for course in courses:
            teacher = User.objects.get(id=course['tid_id'])
            course_obj = ExamCourse.objects.get(id=course['id'])
            course['teacher'] = teacher.username
            student = User.objects.get(id=user_id)
            record = StudentChooseCourse.objects.filter(uid=student, cid=course_obj)
            apply = Operate_Class.objects.filter(user_id=student, class_id=course_obj, type='J')
            if record:
                record_item = StudentChooseCourse.objects.get(uid=student, cid=course_obj)
                if record_item.status == 1:
                    course['choose'] = 1
                else:
                    course['choose'] = 0
            else:
                course['choose'] = 0
            if apply:
                apply_item = Operate_Class.objects.get(user_id=student, class_id=course_obj, type='J')
                if apply_item.status == 1:
                    course['operate'] = 1
                else:
                    course['operate'] = 0
        if not name == '' and not tid == '0' and not status == '':
            for course in courses:
                if contain(course['name'], name) and str(course['tid_id']) == tid and str(
                        course['status']) == status:
                    condition_class.append(course)
        elif not name == '' and not tid == '0':
            for course in courses:
                if contain(course['name'], name) and str(course['tid_id']) == tid:
                    condition_class.append(course)
        elif not name == '' and not status == '':
            for course in courses:
                if contain(course['name'], name) and str(course['status']) == status:
                    condition_class.append(course)
        elif not tid == '0' and not status == '':
            for course in courses:
                if str(course['tid_id']) == tid and str(course['status']) == status:
                    condition_class.append(course)
        elif not name == '':
            for course in courses:
                if contain(course['name'], name):
                    condition_class.append(course)
        elif not tid == '0':
            for course in courses:
                if str(course['tid_id']) == tid:
                    condition_class.append(course)
        elif not status == '':
            for course in courses:
                if str(course['status']) == status:
                    condition_class.append(course)
        else:
            condition_class = courses
        response['condition_class'] = condition_class
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def get_selected_class(request):
    response = {}
    user_id = request.POST.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        choose_obj = user.studentchoosecourse_set.filter(status=1).values()
        choose_list = list(choose_obj)
        for choose in choose_list:
            course = ExamCourse.objects.get(id=choose['cid_id'])
            teacher = User.objects.get(id=course.tid_id)
            choose['name'] = course.name
            choose['teacher'] = teacher.username
            choose['number'] = course.number
            choose['time'] = course.time
            choose['status'] = course.status
            apply = Operate_Class.objects.filter(user_id=user, class_id=course, type='O')
            if apply:
                apply_item = Operate_Class.objects.get(user_id=user, class_id=course, type='O')
                if apply_item.status == 1:
                    choose['operate'] = 1
        response['classes'] = choose_list
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def get_selected_class_by_condition(request):
    response = {}
    condition_class = []
    user_id = request.POST.get('user_id')
    name = request.POST.get('name')
    tid = request.POST.get('teacher')
    status = request.POST.get('status')
    try:
        user = User.objects.get(id=user_id)
        choose_obj = user.studentchoosecourse_set.filter(status=1).values()
        choose_list = list(choose_obj)
        for choose in choose_list:
            course = ExamCourse.objects.get(id=choose['cid_id'])
            teacher = User.objects.get(id=course.tid_id)
            choose['name'] = course.name
            choose['tid'] = teacher.id
            choose['teacher'] = teacher.username
            choose['number'] = course.number
            choose['time'] = course.time
            choose['status'] = course.status
            apply = Operate_Class.objects.filter(user_id=user, class_id=course, type='O')
            if apply:
                apply_item = Operate_Class.objects.get(user_id=user, class_id=course, type='O')
                if apply_item.status == 1:
                    choose['operate'] = 1
        if not name == '' and not tid == '0' and not status == '':
            for choose in choose_list:
                if contain(choose['name'], name) and str(choose['tid']) == tid and str(
                        choose['status']) == status:
                    condition_class.append(choose)
        elif not name == '' and not tid == '0':
            for choose in choose_list:
                if contain(choose['name'], name) and str(choose['tid']) == tid:
                    condition_class.append(choose)
        elif not name == '' and not status == '':
            for choose in choose_list:
                if contain(choose['name'], name) and str(choose['status']) == status:
                    condition_class.append(choose)
        elif not tid == '0' and not status == '':
            for choose in choose_list:
                if str(choose['tid']) == tid and str(choose['status']) == status:
                    condition_class.append(choose)
        elif not name == '':
            for choose in choose_list:
                if contain(choose['name'], name):
                    condition_class.append(choose)
        elif not tid == '0':
            for choose in choose_list:
                if str(choose['tid']) == tid:
                    condition_class.append(choose)
        elif not status == '':
            for choose in choose_list:
                if str(choose['status']) == status:
                    condition_class.append(choose)
        else:
            condition_class = choose_list
        response['condition_class'] = condition_class
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def out_class(request):
    response = {}
    class_id = request.POST.get('class_id')
    user_id = request.POST.get('user_id')
    type = request.POST.get('type')
    stime = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
    try:
        course = ExamCourse.objects.get(id=class_id)
        user = User.objects.get(id=user_id)
        check = Operate_Class.objects.filter(type=type, class_id=course, user_id=user)
        if check:
            Operate_Class.objects.filter(type=type, class_id=course, user_id=user).update(time=stime, etime=None,
                                                                                          status=1)
        else:
            choose = Operate_Class(time=stime, type=type, class_id=course, user_id=user)
            choose.save()
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def select_class(request):
    response = {}
    class_id = request.POST.get('class_id')
    user_id = request.POST.get('user_id')
    type = request.POST.get('type')
    stime = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
    try:
        course = ExamCourse.objects.get(id=class_id)
        user = User.objects.get(id=user_id)
        check = Operate_Class.objects.filter(type=type, class_id=course, user_id=user)
        if check:
            Operate_Class.objects.filter(type=type, class_id=course, user_id=user).update(time=stime, etime=None,
                                                                                          status=1)
        else:
            choose = Operate_Class(time=stime, type=type, class_id=course, user_id=user)
            choose.save()
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def accept_apply(request):
    response = {}
    apply_id = request.POST.get('apply_id')
    try:
        Apply_Class.objects.filter(id=apply_id).update(status=2)
        apply = Apply_Class.objects.get(id=apply_id)
        teacher = User.objects.get(id=apply.tid_id)
        course = ExamCourse(tid=teacher, name=apply.name, time=apply.time, stime=apply.stime, maxnum=apply.maxnum)
        course.save()
        response['code'] = 1
    except Exception as e:
        print(e)
        response['code'] = 0
    return JsonResponse(response)


def refuse_apply(request):
    response = {}
    apply_id = request.POST.get('apply_id')
    try:
        Apply_Class.objects.filter(id=apply_id).update(status=0)
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def get_class_detail(request):
    response = {}
    class_id = request.POST.get('class_id')
    try:
        course = ExamCourse.objects.filter(id=class_id).values()
        response['code'] = 1
        response['course'] = list(course)
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def get_student_apply(request):
    response = {}
    class_id = request.POST.get('class_id')
    try:
        course = ExamCourse.objects.get(id=class_id)
        apply = Operate_Class.objects.filter(class_id=course).values()
        student_apply = list(apply)
        for item in student_apply:
            user = User.objects.get(id=item['user_id_id'])
            item['username'] = user.username
        response['student_apply'] = student_apply
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def get_student_apply_by_condition(request):
    response = {}
    condition_apply = []
    class_id = request.POST.get('class_id')
    type = request.POST.get('type')
    status = request.POST.get('status')
    try:
        course = ExamCourse.objects.get(id=class_id)
        apply_obj = Operate_Class.objects.filter(class_id=course).values()
        student_apply = list(apply_obj)
        for item in student_apply:
            user = User.objects.get(id=item['user_id_id'])
            item['username'] = user.username
        if not type == '' and not status == '':
            for apply in student_apply:
                if apply['type'] == type and str(apply['status']) == status:
                    condition_apply.append(apply)
        elif not type == '':
            for apply in student_apply:
                if apply['type'] == type:
                    condition_apply.append(apply)
        elif not status == '':
            for apply in student_apply:
                if str(apply['status']) == status:
                    condition_apply.append(apply)
        else:
            condition_apply = student_apply
        response['condition_apply'] = condition_apply
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def accept_student_apply(request):
    response = {}
    apply_id = request.POST.get('apply_id')
    try:
        time = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
        apply = Operate_Class.objects.get(id=apply_id)
        course = ExamCourse.objects.get(id=apply.class_id_id)
        number = course.number
        student = User.objects.get(id=apply.user_id_id)
        Operate_Class.objects.filter(id=apply_id).update(status=2, etime=time)
        if apply.type == 'J':
            check = StudentChooseCourse.objects.filter(cid=course, uid=student)
            if check:
                StudentChooseCourse.objects.filter(cid=course, uid=student).update(status=1)
            else:
                choose = StudentChooseCourse(cid=course, uid=student)
                choose.save()
            ExamCourse.objects.filter(id=apply.class_id_id).update(number=number + 1)
        elif apply.type == 'O':
            choose = StudentChooseCourse.objects.filter(cid=course, uid=student)
            StudentChooseCourse.objects.filter(cid=course, uid=student).update(status=0)
            ExamCourse.objects.filter(id=apply.class_id_id).update(number=number - 1)
        response['code'] = 1
    except Exception as e:
        print(e)
        response['code'] = 0
    return JsonResponse(response)


def refuse_student_apply(request):
    response = {}
    apply_id = request.POST.get('apply_id')
    try:
        time = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
        Operate_Class.objects.filter(id=apply_id).update(status=0, etime=time)
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def modify_course(request):
    response = {}
    class_id = request.POST.get('class_id')
    name = request.POST.get('name')
    maxnum = request.POST.get('maxnum')
    time = request.POST.get('time')
    try:
        course = ExamCourse.objects.get(id=class_id)
        teacher = User.objects.get(id=course.tid_id)
        course_obj = ExamCourse.objects.filter(tid=teacher).exclude(id=class_id).values()
        courses = list(course_obj)
        for course_item in courses:
            if name == course_item['name']:
                response['code'] = 2
        ExamCourse.objects.filter(id=class_id).update(name=name, maxnum=maxnum, time=time)
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def end_class(request):
    response = {}
    class_id = request.POST.get('id')
    try:
        ExamCourse.objects.filter(id=class_id).update(status=0)
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def get_teacher_apply(request):
    response = {}
    user_id = request.POST.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        apply_obj = Apply_Class.objects.filter(tid=user).values()
        apply_list = list(apply_obj)
        response['apply_list'] = apply_list
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)


def get_teacher_apply_by_condition(request):
    response = {}
    user_id = request.POST.get('user_id')
    status = request.POST.get('status')
    try:
        user = User.objects.get(id=user_id)
        if status == '':
            apply_obj = Apply_Class.objects.filter(tid=user).values()
            apply_list = list(apply_obj)
            response['apply_list'] = apply_list
        else:
            apply_obj = Apply_Class.objects.filter(tid=user, status=status).values()
            apply_list = list(apply_obj)
        response['condition_apply'] = apply_list
        response['code'] = 1
    except Exception as e:
        response['code'] = 0
    return JsonResponse(response)
