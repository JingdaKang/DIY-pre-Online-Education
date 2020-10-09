import json

import requests
from django.core import serializers
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from notes.aescrypt import AESUtil
from backend.models import Note, NoteBook, Tag, NoteTag
from backend.models import User_Question, Simple, Multiple, Subjective, Blank, Judge, ExamAnswer as Answer, ExamSimple, ExamMultiple, \
    ExamBlank, ExamCourse, ExamJudge, ExamQuestion, ExamSubjective, Course, Work, ExamTeacherCloud, GoodWork

from django.db import connection, transaction

from backend.models import User

def NoteBook_get_or_create(**kwargs):
    created = False
    cursor = connection.cursor()
    try:
        obj = NoteBook.objects.get(**kwargs)
    except:
        with transaction.atomic():
            cursor.execute("insert into tb_notebook(notebook_name,creator_id,\
                notebook_create,notebook_modify) values (%s,%s,now(),now());",
                (kwargs['notebook_name'],kwargs['creator_id'].id))
            obj = NoteBook.objects.latest('id')
        created = True
    cursor.close()
    return obj, created
def Note_update_or_create(defaults, **kwargs):
    cursor = connection.cursor()
    created = False
    try:
        obj = Note.objects.get(**kwargs)
        Note.objects.filter(id=obj.id).update(**defaults)
    except:
        #obj = Note(**kwargs)
        with transaction.atomic():
            cursor.execute("insert into tb_note(note_title,note_text,modifier_id,\
                writer_id,notebook_id,note_type,is_delete,note_create,note_modify) values \
                    (%s,%s,%s,%s,%s,'markdown','f',now(),now());",(defaults['note_title'],
                    defaults['note_text'],defaults['modifier_id'].id,defaults['writer_id'].id,
                    defaults['notebook_id'].id))
            obj = Note.objects.latest('id')
        #Note.objects.filter(id=obj.id).update(**defaults)
        created = True
    cursor.close()
    return obj, created


#学生访问作业系统生成作业错题本
class WorkErrorBookAPIView(APIView):
    # 由于数据库表没有设置外键，这里错题和课程的相关查询比较冗杂
    def get(self,request):
        if request.user.type!='S':
            return JsonResponse({"code": "ok", "msg": "教师无需读取错题"})
        #根据未读取的错题找到所有对应课程
        works = User_Question.objects.filter(cloud=True, is_read=False, sid=request.user.id).values('wid').distinct().order_by('wid')
        course_set = set()
        for work in works:
            course_id = Work.objects.filter(id = work['wid']).values('cid')
            cid = course_id[0]
            course = Course.objects.get(id = cid['cid'])
            course_set.add(course)
        if len(course_set)==0:
            return JsonResponse({"code": "ok", "msg": "无需生成新的错题本"})
            #以课程为分类依据生成错题笔记
        for course in course_set:
            defaults = {'creator_id': request.user}
            course_notebook, cn_create = NoteBook.objects.get_or_create(notebook_name=course.name,
                                                                        creator_id=request.user, defaults=defaults)
            tag_obj = Tag.objects.get(tag_name="错题本", creator_id=request.user)
            #该课程对应的所有作业，作为与错题对应的依据
            course_works = Work.objects.filter(cid = course.id).values('id')
            dates = set()
            wid_set = set()
            for course_work in course_works:
                wid_set.add(course_work['id'])
                date = User_Question.objects.filter(cloud=True, is_read=False, sid=request.user.id,
                                          wid=course_work['id']).values('upload_time')
                for d in date:
                    dates.add(d['upload_time'])
            #在课程分类的基础上按上传日期生成错题笔记
            if len(dates) != 0:
                for date in dates:
                    note_title = date.strftime('%Y-%m-%d') + " 作业错题"
                    note_text = ""
                    qs = User_Question.objects.filter(sid=request.user.id, cloud=True,
                                                     wid__in = wid_set,
                                                     upload_time=date)
                    qs_list = list(qs)
                    for i, question in enumerate(qs_list):
                        if question.type == '1':
                            question_detail = Simple.objects.get(id=question.qid)
                            question_text = "##### 错题" + str(i + 1) + "（单选题）:\n" + \
                                            question_detail.content + "\n" + \
                                            "A、" + question_detail.choice1 + "\n" + \
                                            "B、" + question_detail.choice2 + "\n" + \
                                            "C、" + question_detail.choice3 + "\n" + \
                                            "D、" + question_detail.choice4 + "\n" + \
                                            "##### 参考答案" + str(i + 1) + "\n" + \
                                            question_detail.answer + "\n" + \
                                            "##### 解析" + str(i + 1) + "\n" + \
                                            question_detail.explain + "\n\n" + "---" + "\n"
                            note_text += question_text
                        elif question.type == '2':
                            question_detail = Multiple.objects.get(id=question.qid)
                            question_text = "##### 错题" + str(i + 1) + "（多选题）:\n" + \
                                            question_detail.content + "\n" + \
                                            "A、" + question_detail.choice1 + "\n" + \
                                            "B、" + question_detail.choice2 + "\n" + \
                                            "C、" + question_detail.choice3 + "\n" + \
                                            "D、" + question_detail.choice4 + "\n" + \
                                            "##### 参考答案" + str(i + 1) + "\n" + \
                                            question_detail.answer + "\n" + \
                                            "##### 解析" + str(i + 1) + "\n" + \
                                            question_detail.explain + "\n\n" + "---" + "\n"
                            note_text += question_text
                        elif question.type == '5':
                            question_detail = Subjective.objects.get(id=question.qid)
                            question_text = "##### 错题" + str(i + 1) + "（主观题）:\n" + \
                                            question_detail.content + "\n" + \
                                            "##### 参考答案" + str(i + 1) + "\n" + \
                                            question_detail.answer + "\n" + \
                                            "##### 解析" + str(i + 1) + "\n" + \
                                            question_detail.explain + "\n\n" + "---" + "\n"
                            note_text += question_text
                        elif question.type == '4':
                            question_detail = Blank.objects.get(id=question.qid)
                            question_text = "##### 错题" + str(i + 1) + "（填空题）:\n" + \
                                            question_detail.content + "\n" + \
                                            "##### 参考答案" + str(i + 1) + "\n" + \
                                            question_detail.answer + "\n" + \
                                            "##### 解析" + str(i + 1) + "\n" + \
                                            question_detail.explain + "\n\n" + "---" + "\n"
                            note_text += question_text
                        elif question.type == '3':
                            question_detail = Judge.objects.get(id=question.qid)
                            question_text = "##### 错题" + str(i + 1) + "（判断题）:\n" + \
                                            question_detail.content + "\n" + \
                                            "##### 参考答案" + str(i + 1) + "\n" + \
                                            str(question_detail.answer) + "\n" + \
                                            "##### 解析" + str(i + 1) + "\n" + \
                                            str(question_detail.explain) + "\n\n" + "---" + "\n"
                            note_text += question_text
                    vi = b'HjRP7LlXuSsFMisz'  # 偏移量
                    mode = 'CBC'  # 加密模式 使用CBC模式安全性更高
                    encode_ = 'utf-8'
                    # 加密密钥
                    key = "mycloudnote"
                    # 设置加密器
                    cipher = AESUtil(key, mode, vi, encode_)
                    en_text = cipher.aesencrypt(note_text)
                    new_values = {'note_title': note_title, 'note_text': en_text, 'writer_id': request.user,
                                  'modifier_id': request.user, 'notebook_id': course_notebook}
                    note_obj, created = Note.objects.update_or_create(note_title=note_title,writer_id = request.user,notebook_id = course_notebook, defaults=new_values, )
                    if created:
                        relation = NoteTag(note=note_obj, t=tag_obj)
                        relation.save()
                    qs.update(is_read=True)
        return JsonResponse({"code":"ok","msg":"成功生成错题本"})

#学生访问考试系统生成考试错题本
class ExamErrorBookAPIView(APIView):
    def get(self,request):
        if request.user.type!='S':
            return JsonResponse({"code": "ok", "msg": "教师无需读取错题"})
        courses = Answer.objects.filter(cloud=True, is_read=False, uid=request.user).values(
            'qid__cid__name').distinct().order_by('qid__cid__name')
        if len(courses)!=0:
            for course in courses:
                defaults = {'creator_id':request.user}
                course_notebook, cn_create = NoteBook_get_or_create(notebook_name=course['qid__cid__name'],creator_id=request.user)
                #course_notebook, cn_create = NoteBook.objects.get_or_create(notebook_name=course['qid__cid__name'],creator_id=request.user,defaults = defaults)
                tag_obj = Tag.objects.get(tag_name="错题本", creator_id=request.user)
                dates = Answer.objects.filter(cloud=True, is_read=False, uid=request.user,qid__cid__name=course['qid__cid__name']).values(
                    'update_time').distinct().order_by('update_time')
                if len(dates) != 0:
                    for date in dates:
                        #按上传日期生成笔记名称
                        note_title = date['update_time'].strftime('%Y-%m-%d') + " 考试错题"
                        note_text = ""
                        answerqs = Answer.objects.filter(uid=request.user, cloud=True,qid__cid__name=course['qid__cid__name'],
                                                         update_time=date['update_time']).order_by('qid__type')
                        qs_list = list(answerqs)
                        for i, answer in enumerate(qs_list):
                            if answer.qid.type == '1':
                                question_detail = ExamSimple.objects.get(qid=answer.qid)
                                question_text = "##### 错题" + str(i + 1) + "（单选题）:\n" + \
                                                question_detail.content + "\n" + \
                                                "A、" + question_detail.choice1 + "\n" + \
                                                "B、" + question_detail.choice2 + "\n" + \
                                                "C、" + question_detail.choice3 + "\n" + \
                                                "D、" + question_detail.choice4 + "\n" + \
                                                "##### 参考答案" + str(i + 1) + "\n" + \
                                                question_detail.answer + "\n\n" + "---" + "\n"
                                note_text += question_text
                            elif answer.qid.type == '2':
                                question_detail = ExamMultiple.objects.get(qid=answer.qid)
                                question_text = "##### 错题" + str(i + 1) + "（多选题）:\n" + \
                                                question_detail.content + "\n" + \
                                                "A、" + question_detail.choice1 + "\n" + \
                                                "B、" + question_detail.choice2 + "\n" + \
                                                "C、" + question_detail.choice3 + "\n" + \
                                                "D、" + question_detail.choice4 + "\n" + \
                                                "##### 参考答案" + str(i + 1) + "\n" + \
                                                str(question_detail.answer) + "\n\n" + "---" + "\n"
                                note_text += question_text
                            elif answer.qid.type == '5':
                                question_detail = ExamSubjective.objects.get(qid=answer.qid)
                                question_text = "##### 错题" + str(i + 1) + "（主观题）:\n" + \
                                                question_detail.content + "\n" + \
                                                "##### 参考答案" + str(i + 1) + "\n" + \
                                                question_detail.answer + "\n\n" + "---" + "\n"
                                note_text += question_text
                            elif answer.qid.type == '3':
                                question_detail = ExamBlank.objects.get(qid=answer.qid)
                                question_text = "##### 错题" + str(i + 1) + "（填空题）:\n" + \
                                                question_detail.content + "\n" + \
                                                "##### 参考答案" + str(i + 1) + "\n" + \
                                                question_detail.answer + "\n\n" + "---" + "\n"
                                note_text += question_text
                            elif answer.qid.type == '4':
                                question_detail = ExamJudge.objects.get(qid=answer.qid)
                                question_text = "##### 错题" + str(i + 1) + "（判断题）:\n" + \
                                                question_detail.content + "\n" + \
                                                "##### 参考答案" + str(i + 1) + "\n" + \
                                                str(question_detail.answer) + "\n\n" + "---" + "\n"
                                note_text += question_text
                        vi = b'HjRP7LlXuSsFMisz'  # 偏移量
                        mode = 'CBC'  # 加密模式 使用CBC模式安全性更高
                        encode_ = 'utf-8'
                        # 加密密钥
                        key = "mycloudnote"
                        # 设置加密器
                        cipher = AESUtil(key, mode, vi, encode_)
                        en_text = cipher.aesencrypt(note_text)
                        new_values = {'note_title': note_title, 'note_text': en_text, 'writer_id': request.user,
                                    'modifier_id': request.user, 'notebook_id': course_notebook}
                        #note_obj, created = Note.objects.update_or_create(note_title=note_title,writer_id = request.user,notebook_id = course_notebook, defaults=new_values, )
                        note_obj, created = Note_update_or_create(new_values, note_title=note_title,writer_id = request.user,notebook_id = course_notebook)
                        if created:
                            relation = NoteTag(note=note_obj, t=tag_obj)
                            relation.save()
                        answerqs.update(is_read=True)
            return JsonResponse({"code": "ok", "msg": "成功生成错题本"})
        return JsonResponse({"code": "ok", "msg": "无需生成新的错题本"})

# 教师访问作业系统生成作业优秀题解
class WorkGoodAnswerAPIView(APIView):
    def get(self,request):
        if request.user.type!='T':
            return JsonResponse({"code": "ok", "msg": "学生无需读取优秀题解"})
        courses = GoodWork.objects.filter(is_read=False, tid=request.user.id).values(
            'cid').distinct().order_by('cid')
        if len(courses)!=0:
            for course in courses:
                course_obj = Course.objects.get(id = course['cid'])
                defaults = {'creator_id':request.user}
                course_notebook, cn_create = NoteBook.objects.get_or_create(notebook_name=course_obj.name,creator_id=request.user,defaults = defaults)
                tag_obj = Tag.objects.get(tag_name="优秀题解", creator_id=request.user)
                dates = GoodWork.objects.filter(is_read=False, tid=request.user.id,cid = course_obj.id).values(
                    'upload_time').distinct().order_by('upload_time')
                if len(dates) != 0:
                    for date in dates:
                        #按上传日期生成笔记名称
                        note_title = date['upload_time'].strftime('%Y-%m-%d') + " 作业优秀题解"
                        note_text = ""
                        answerqs = GoodWork.objects.filter(tid=request.user.id,cid=course_obj.id,
                                                         upload_time=date['upload_time'])
                        qs_list = list(answerqs)
                        for i, answer in enumerate(qs_list):
                                question_detail = Subjective.objects.get(id=answer.qid)
                                student_detail = User.objects.get(id = answer.sid)
                                question_text = "##### 错题" + str(i + 1) + "（主观题）:\n" + \
                                                question_detail.content + "\n" + \
                                                "##### 参考答案" + str(i + 1) + "\n" + \
                                                question_detail.answer + "\n" + \
                                                "##### 优秀题解(答题人：" + student_detail.username + ")\n" + \
                                                answer.answer + "\n\n" + "---" + "\n"
                                note_text += question_text
                        vi = b'HjRP7LlXuSsFMisz'  # 偏移量
                        mode = 'CBC'  # 加密模式 使用CBC模式安全性更高
                        encode_ = 'utf-8'
                        # 加密密钥
                        key = "mycloudnote"
                        # 设置加密器
                        cipher = AESUtil(key, mode, vi, encode_)
                        en_text = cipher.aesencrypt(note_text)
                        new_values = {'note_title': note_title, 'note_text': en_text, 'writer_id': request.user,
                                  'modifier_id': request.user, 'notebook_id': course_notebook}
                        note_obj, created = Note.objects.update_or_create(note_title=note_title, writer_id = request.user,notebook_id = course_notebook,defaults=new_values, )
                        if created:
                            relation = NoteTag(note=note_obj, t=tag_obj)
                            relation.save()
                        answerqs.update(is_read=True)
            return JsonResponse({"code": "ok", "msg": "成功生成优秀题解"})
        return JsonResponse({"code": "ok", "msg": "无需生成新的优秀题解"})

# 教师访问考试系统生成考试优秀题解
class ExamGoodAnswerAPIView(APIView):
    def get(self,request):
        if request.user.type!='T':
            return JsonResponse({"code": "ok", "msg": "学生无需读取优秀题解"})
        courses = ExamTeacherCloud.objects.filter(cloud=True, is_read=False, tid=request.user).values(
            'aid__qid__cid__name').distinct().order_by('aid__qid__cid__name')
        if len(courses)!=0:
            for course in courses:
                defaults = {'creator_id':request.user}
                course_notebook, cn_create = NoteBook.objects.get_or_create(notebook_name=course['aid__qid__cid__name'],creator_id=request.user,defaults = defaults)
                tag_obj = Tag.objects.get(tag_name="优秀题解", creator_id=request.user)
                dates = ExamTeacherCloud.objects.filter(cloud=True, is_read=False, tid=request.user,aid__qid__cid__name=course['aid__qid__cid__name']).values(
                    'update_time').distinct().order_by('update_time')
                if len(dates) != 0:
                    for date in dates:
                        #按上传日期生成笔记名称
                        note_title = date['update_time'].strftime('%Y-%m-%d') + " 考试优秀题解"
                        note_text = ""
                        upload_list = ExamTeacherCloud.objects.filter(tid = request.user,cloud = True,aid__qid__cid__name=course['aid__qid__cid__name'],
                                                                     update_time=date['update_time']).order_by('aid__qid__type')
                        for i, upload in enumerate(upload_list):
                            if upload.aid.qid.type == '5':
                                question_detail = ExamSubjective.objects.get(qid=upload.aid.qid)
                                question_text = "##### 错题" + str(i + 1) + "（主观题）:\n" + \
                                                question_detail.content + "\n" + \
                                                "##### 参考答案" + str(i + 1) + "\n" + \
                                                question_detail.answer + "\n" + \
                                                "##### 优秀题解(答题人：" + upload.sid.username + ")\n" + \
                                                upload.aid.answer + "\n\n" + "---" + "\n"
                                note_text += question_text
                            elif upload.aid.qid.type == '3':
                                question_detail = ExamBlank.objects.get(qid=upload.aid.qid)
                                question_text = "##### 错题" + str(i + 1) + "（填空题）:\n" + \
                                                question_detail.content + "\n" + \
                                                "##### 参考答案" + str(i + 1) + "\n" + \
                                                question_detail.answer + "\n" + \
                                                "##### 优秀题解(答题人：" + upload.sid.username + ")\n" + \
                                                upload.aid.answer + "\n\n" + "---" + "\n"
                                note_text += question_text
                        vi = b'HjRP7LlXuSsFMisz'  # 偏移量
                        mode = 'CBC'  # 加密模式 使用CBC模式安全性更高
                        encode_ = 'utf-8'
                        # 加密密钥
                        key = "mycloudnote"
                        # 设置加密器
                        cipher = AESUtil(key, mode, vi, encode_)
                        en_text = cipher.aesencrypt(note_text)
                        new_values = {'note_title': note_title, 'note_text': en_text, 'writer_id': request.user,
                                  'modifier_id': request.user, 'notebook_id': course_notebook}
                        note_obj, created = Note.objects.update_or_create(note_title=note_title,writer_id = request.user,notebook_id = course_notebook, defaults=new_values, )

                        if created:
                            relation = NoteTag(note=note_obj, t=tag_obj)
                            relation.save()
                        upload_list.update(is_read=True)
            return JsonResponse({"code": "ok", "msg": "成功生成优秀题解"})
        return JsonResponse({"code": "ok", "msg": "无需生成新的优秀题解"})