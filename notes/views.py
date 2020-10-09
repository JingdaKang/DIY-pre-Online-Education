import json
from .aescrypt import AESUtil
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from backend.models import User, Team
from backend.models import Image,Note, NoteBook,Tag,NoteTag
from notes.serializers import ImageUploadSerializer,NoteSerializer, NoteBookSerializer, NoteBookSerializerBase,TagSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.db import connection, transaction

cursor = connection.cursor()

# Create your views here.
class myPagination(PageNumberPagination):
    """自定义分页"""
    # 每页显示多少条数据
    page_size = 8
    # url/?page=1&size=5, 改变默认每页显示的个数
    page_size_query_param = "size"
    # 最大个数不超过15条
    max_page_size = 10
    # 获取页码数
    page_query_param = "page"

class teamNotebookPagination(PageNumberPagination):
    """自定义分页"""
    # 每页显示多少条数据
    page_size = 6
    # url/?page=1&size=5, 改变默认每页显示的个数
    page_size_query_param = "size"
    # 最大个数不超过15条
    max_page_size = 8
    # 获取页码数
    page_query_param = "page"

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('-id')#具体返回的数据 queryset 指明该视图集在查询数据时使用的查询集
    serializer_class = NoteSerializer# serializer_class 指明该视图在进行序列化或反序列化时使用的序列化器。
    pagination_class = myPagination

    def create(self, request, *args, **kwargs):
        '''
        新建笔记
        '''
        print(request.data)
        data = request.data
        notebook_obj = NoteBook.objects.get(id = data['folder_id'])
        vi = b'HjRP7LlXuSsFMisz'  # 偏移量
        mode = 'CBC' #加密模式 使用CBC模式安全性更高
        encode_ = 'utf-8'
        print(request.user.id)
        if data.get('team_id',False):
            team_obj = Team.objects.get(id=data['team_id'])
            #加密密钥
            key = 'myteamnote'
            # 设置加密器
            cipher = AESUtil(key, mode, vi, encode_)
            note_text = cipher.aesencrypt(data['mkValue'])
            with transaction.atomic():
                cursor.execute("insert into tb_note(note_title,note_text,writer_id,modifier_id,notebook_id,team_id,\
                    note_type,note_create,note_modify,is_delete) values (%s,%s,%s,%s,%s,%s,'markdown',\
                        now(),now(),'f');",(data['title'],note_text,request.user.id,request.user.id,notebook_obj.id,
                        team_obj.id))
                note_obj = Note.objects.latest('id')
            #note_obj = Note.objects.create(note_title=data['title'], note_text=note_text, writer_id=request.user,
            #                               modifier_id=request.user, notebook_id=notebook_obj, team_id=team_obj)
            #修改团队笔记本的更新时间和更新人
            NoteBook.objects.filter(id=note_obj.notebook_id_id).update(notebook_modify=note_obj.note_modify,
                                                                        modifier_id=note_obj.modifier_id)
            #修改团队的更新时间和更新人
            Team.objects.filter(id=note_obj.team_id_id).update(team_modify=note_obj.note_modify,
                                                               modifier_id=note_obj.modifier_id)
        else:
            #加密密钥
            key = 'mycloudnote'
            # 设置加密器
            cipher = AESUtil(key, mode, vi, encode_)
            note_text = cipher.aesencrypt(data['mkValue'])
            with transaction.atomic():
                cursor.execute("insert into tb_note(note_title,note_text,writer_id,modifier_id,notebook_id,\
                    note_type,note_create,note_modify,is_delete) values (%s,%s,%s,%s,%s,'markdown',\
                        now(),now(),'f');",(data['title'],note_text,request.user.id,request.user.id,notebook_obj.id))
                note_obj = Note.objects.latest('id')
            #note_obj = Note.objects.create(note_title=data['title'], note_text=note_text, writer_id=request.user,
            #                           modifier_id=request.user, notebook_id=notebook_obj)
        #反序列化
        note = {
            'tags':json.loads(data['tags'])
        }
        serializer = self.get_serializer(note_obj, data=note, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def retrieve(self, request, *args, **kwargs):
        '''查看笔记详情'''
        instance = self.get_object()
        #获取密文
        en_text = instance.note_text
        #获取解密密钥
        if instance.team_id == None:
            key = "mycloudnote"
        else:
            key = "myteamnote"
        vi = b'HjRP7LlXuSsFMisz'  # 偏移量
        mode = 'CBC' #模式
        encode_ = 'utf-8'
        #设置密码器 使用CBC模式安全性更高
        cipher = AESUtil(key,mode,vi,encode_)
        #笔记内容解密
        note_text = cipher.aesdecrypt(en_text)
        instance.note_text = note_text
        serializer = self.get_serializer(instance)
        #instance.note_text = en_text
        return Response(serializer.data)
    
    @action(methods=['post'], detail=False)
    def isLock(self, request, *args, **kwargs):
        data = request.data
        note = Note.objects.filter(id=data['note_id'])
        if note.first().locked_by != None :
            return JsonResponse({"code":"no","msg":"有成员正在编辑，请稍后再试"})
        else:
            note.update(locked_by = request.user)
            return JsonResponse({"code":"yes","msg":"可以编辑"})
    
    @action(methods=['post'], detail=False)
    def cancelLock(self, request, *args, **kwargs):
        data = request.data
        note = Note.objects.filter(id=data['note_id'])
        note.update(locked_by = None)
        return JsonResponse({"code":"yes","msg":"可以编辑"})
    
    def update(self, request, *args, **kwargs):
        '''修改笔记内容'''
        instance = self.get_object()
        data = request.data
        note_obj = Note.objects.filter(id = instance.id)
        if note_obj[0].locked_by != request.user and note_obj[0].locked_by != None:
            return JsonResponse({"msg":"error"})
        #设置加密密钥
        if data.get('team_id',False):
            key = "myteamnote"

        else:
            key = "mycloudnote"
        vi = b'HjRP7LlXuSsFMisz'  # 偏移量
        mode = 'CBC' #加密模式
        encode_ = 'utf-8'
        #设置加密器 使用CBC模式安全性更高
        cipher = AESUtil(key,mode,vi,encode_)
        note_text = cipher.aesencrypt(data['mkValue'])
        note_obj.update(team_id = data.get('team_id',None),modifier_id = request.user)
        new = {'note_title': data['title'], 'note_text': note_text, 'notebook_id': data['folder_id'],
               'writer_id': request.user.id, 'note_modify': datetime.now(),'tags':json.loads(data['tags'])}
        serializer = self.get_serializer(note_obj.first(), data=new, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        note_obj[0].locked_by = None
        if data.get('team_id',False):
            team_obj = Team.objects.get(id=data['team_id'])
            #修改团队笔记本的更新时间和更新人
            NoteBook.objects.filter(id=note_obj[0].notebook_id_id).update(notebook_modify=note_obj[0].note_modify,
                                                                        modifier_id=note_obj[0].modifier_id)
            #修改团队的更新时间和更新人
            Team.objects.filter(id=note_obj[0].team_id_id).update(team_modify=note_obj[0].note_modify,
                                                               modifier_id=note_obj[0].modifier_id)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get'], detail=False)
    def delete(self, request, *args, **kwargs):
        """ 逻辑删除笔记 """
        note_id =  request.query_params.get('id', None)
        noteqs = Note.objects.filter(id = note_id)
        noteqs.update(is_delete = True,note_delete = datetime.now())
        serializer = self.get_serializer(noteqs.first())
        return JsonResponse(serializer.data)

    @action(methods=['get'], detail=False)
    def recover(self, request, *args, **kwargs):
        """ 逻辑恢复笔记 """
        note_id =  request.query_params.get('id', None)
        noteqs = Note.objects.filter(id = note_id)
        noteqs.update(is_delete = False,note_delete = None)
        serializer = self.get_serializer(noteqs.first())
        return JsonResponse(serializer.data)

    @action(methods=['get'], detail=False)
    def getRubbish(self, request, *args, **kwargs):
        '''获取废纸篓里的笔记列表'''
        self.queryset = Note.objects.filter(writer_id=request.user.id, is_delete=True).order_by('-note_delete')
        queryset = self.filter_queryset(self.get_queryset())
        # 获取解密密钥
        key = "mycloudnote"
        vi = b'HjRP7LlXuSsFMisz'  # 偏移量
        mode = 'CBC'  # 模式
        encode_ = 'utf-8'

        for instance in queryset:
            # 获取密文
            en_text = instance.note_text
            # 设置密码器 使用CBC模式安全性更高
            cipher = AESUtil(key, mode, vi, encode_)
            # 笔记内容解密
            note_text = cipher.aesdecrypt(en_text)
            instance.note_text = note_text

        # 在数据库中获取分页的数据
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            ret = self.get_paginated_response(serializer.data)
            return ret

        serializer = self.get_serializer(queryset, many=True)
        ret = JsonResponse(serializer.data,safe=False)
        return ret



    @action(methods=['get','post'],detail=False)
    def listByNotebook(self, request, *args, **kwargs):
        """ 根据笔记本id获取对应笔记本下的笔记列表 """
        notebook_id = request.query_params.get('notebook_id', None)
        self.queryset = Note.objects.filter(notebook_id=notebook_id,is_delete=False).order_by('-note_modify')
        queryset = self.filter_queryset(self.get_queryset())
        # 在数据库中获取分页的数据
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            ret = self.get_paginated_response(serializer.data)
            return ret

        serializer = self.get_serializer(queryset, many=True)
        ret = JsonResponse(serializer.data,safe=False)
        return ret

    @action(methods=['get','post'],detail=False)
    def listByKeyword(self, request, *args, **kwargs):
        """ 根据关键词获取对应的笔记列表 """
        notebook_id = request.query_params.get('notebook_id',None)
        keyword = request.query_params.get('keyword', None)
        if keyword is not None:
            self.queryset = Note.objects.filter(notebook_id = notebook_id,note_title__contains=keyword,is_delete=False).order_by('-note_modify')
        else:
            self.queryset = Note.objects.filter(notebook_id = notebook_id,is_delete=False).order_by('-note_modify')
        queryset = self.filter_queryset(self.get_queryset())
        # 在数据库中获取分页的数据
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            ret = self.get_paginated_response(serializer.data)
            return ret

        serializer = self.get_serializer(queryset, many=True)
        ret = JsonResponse(serializer.data,safe=False)
        return ret



class NoteBookViewSet(viewsets.ModelViewSet):
    queryset = NoteBook.objects.all()
    serializer_class = NoteBookSerializer
    pagination_class = myPagination

    @action(methods=['get'], detail=False)
    def delete(self, request, *args, **kwargs):
        """ 逻辑删除笔记本 """
        notebook_id =  request.query_params.get('id', None)
        notebookqs = NoteBook.objects.get(id = notebook_id)
        noteqs = notebookqs.notebook_note.all()
        noteqs.update(is_delete = True,note_delete = datetime.now(),notebook_id = 1)
        notebookqs.delete()
        serializer = self.get_serializer(noteqs.first())
        return JsonResponse(serializer.data)

    def list(self, request, *args, **kwargs):
        '''
        获取笔记本列表
        '''
        type = request.query_params.get('type', None)
        print(type)
        if type == 'base':
            self.serializer_class = NoteBookSerializerBase
        self.queryset = NoteBook.objects.filter(creator_id=request.user.id,team_id=None).order_by('notebook_create')
        #self.queryset = NoteBook.objects.filter(creator_id=2)
        queryset = self.filter_queryset(self.get_queryset())
        # 在数据库中获取分页的数据
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            ret = self.get_paginated_response(serializer.data)
            return ret

        serializer = self.get_serializer(queryset, many=True)
        ret = JsonResponse(serializer.data,safe=False)
        return ret

    @action(methods=['get', 'post'], detail=False)
    def listNotebookName(self,request,*args,**kwargs):
        '''
        获取笔记本列表名称作为笔记编辑页面展示
        '''
        type = request.query_params.get('type', None)
        print(type)
        if type == 'base':
            self.serializer_class = NoteBookSerializerBase
        self.queryset = NoteBook.objects.filter(creator_id=request.user.id,team_id=None).order_by('notebook_create')
        #self.queryset = NoteBook.objects.filter(creator_id=2)
        queryset = self.filter_queryset(self.get_queryset())
        # 不分页

        serializer = self.get_serializer(queryset, many=True)
        ret = JsonResponse(serializer.data,safe=False)
        return ret
    @action(methods=['get', 'post'], detail=False)
    def listTeamNotebook(self, request, *args, **kwargs):
        '''
        获取团队笔记本列表
        '''

        type = request.query_params.get('type', None)
        if type == 'base':
            self.serializer_class = NoteBookSerializerBase
        team_id = request.query_params.get("team_id")
        self.queryset = NoteBook.objects.filter(team_id=team_id).order_by('id')
        #self.queryset = NoteBook.objects.filter(creator_id=2)
        queryset = self.filter_queryset(self.get_queryset())
        # 在数据库中获取分页的数据
        self.pagination_class=teamNotebookPagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            ret = self.get_paginated_response(serializer.data)
            return ret

        serializer = self.get_serializer(queryset, many=True)
        ret = JsonResponse(serializer.data,safe=False)
        return ret

    @action(methods=['get', 'post'], detail=False)
    def listTeamNotebookName(self, request, *args, **kwargs):
        '''
        获取团队笔记本列表名称作为笔记编辑页面的展示
        '''
        type = request.query_params.get('type', None)
        if type == 'base':
            self.serializer_class = NoteBookSerializerBase
        team_id = request.query_params.get("team_id")
        self.queryset = NoteBook.objects.filter(team_id=team_id).order_by('id')
        # self.queryset = NoteBook.objects.filter(creator_id=2)
        queryset = self.filter_queryset(self.get_queryset())
        # 不分页

        serializer = self.get_serializer(queryset, many=True)
        ret = JsonResponse(serializer.data, safe=False)
        return ret

    def retrieve(self, request, pk=None):
        """ 笔记本详情 """
        # 获取实例
        user = self.get_object()
        # 序列化
        serializer = self.get_serializer(user)
        return JsonResponse(serializer.data)

    def create(self, request, *args, **kwargs):
        """ 新建笔记本 """
        creator = request.user
        notebook_name = request.data['notebook_name']
        with transaction.atomic():
            cursor.execute("insert into tb_notebook(notebook_name,creator_id,modifier_id,\
                notebook_create,notebook_modify) values (%s,%s,%s,now(),now());",
                (notebook_name,creator.id,creator.id))
            notebook_obj = NoteBook.objects.latest('id')
        '''notebook_obj = NoteBook.objects.create(
            notebook_name=notebook_name,
            creator_id=creator,
            modifier_id=creator,
        )'''

        serializer = self.get_serializer(notebook_obj)

        return JsonResponse(serializer.data)

    @action(methods=['post'], detail=False)
    def createTeamNotebook(self, request, *args, **kwargs):
        """ 新建团队笔记本 """
        creator = request.user
        team_notebook_name = request.data['team_notebook_name']
        team_id = request.data['team_id']
        team = Team.objects.get(id = team_id)
        with transaction.atomic():
            cursor.execute("insert into tb_notebook(notebook_name,creator_id,modifier_id,\
                team_id,notebook_create,notebook_modify) values (%s,%s,%s,%s,now(),now());",
                (team_notebook_name,creator.id,creator.id,team.id))
            team_notebook_obj = NoteBook.objects.latest('id')
        '''team_notebook_obj = NoteBook.objects.create(
            notebook_name=team_notebook_name,
            creator_id= creator,
            modifier_id=creator,
            team_id = team
        )'''
        Team.objects.filter(id=team_notebook_obj.team_id_id).update(team_modify=team_notebook_obj.notebook_modify,
                                                                  modifier_id=team_notebook_obj.modifier_id)
        serializer = self.get_serializer(team_notebook_obj)

        return JsonResponse(serializer.data)

    @action(methods=['post'], detail=False)
    def isLock(self, request, *args, **kwargs):
        data = request.data
        notebook = NoteBook.objects.filter(id=data['notebook_id'])
        if notebook.first().locked_by != None :
            return JsonResponse({"code":"no","msg":"有成员正在编辑，请稍后再试"})
        else:
            notebook.update(locked_by = request.user)
            return JsonResponse({"code":"yes","msg":"可以编辑"})

    @action(methods=['post'], detail=False)
    def cancelLock(self, request, *args, **kwargs):
        data = request.data
        notebook = NoteBook.objects.filter(id=data['notebook_id'])
        notebook.update(locked_by = None)
        return JsonResponse({"code":"yes","msg":"可以编辑"})

    @action(methods=['post'], detail=False)
    def updateTeamNotebookName(self, request, *args, **kwargs):
        '''修改团队笔记本名称'''
        data = request.data
        notebook = NoteBook.objects.get(id=data['notebook_id'])
        if notebook.locked_by != request.user :
            return JsonResponse({"msg":"error"})
        notebook.notebook_name = data['notebook_name']
        notebook.modifier_id = request.user
        notebook.locked_by = None
        notebook.save()
        team = Team.objects.filter(id = notebook.team_id_id).update(team_modify = notebook.notebook_modify,modifier_id = notebook.modifier_id)
        serializer = self.get_serializer(notebook)

        return JsonResponse(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """ 删除笔记本 """

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all();
    serializer_class = TagSerializer# serializer_class 指明该视图在进行序列化或反序列化时使用的序列化器。
    pagination_class = myPagination

    @action(methods=['post'], detail=False)
    def addToNote(self,request,*args,**kwargs):
        '''给笔记添加标签'''
        tags = json.loads(request.data['tags'])
        note_id = request.data['note_id']
        noteobj = Note.objects.get(id = note_id)
        for tag in tags:
            tagobj = Tag.objects.filter(tag_name=tag)
            if tagobj.count()<=0 :
                with transaction.atomic():
                    cursor.execute("insert into tb_tag(tag_name,creator_id) values \
                        (%s,%s);",(tag,request.user.id))
                    tabobj = Tag.objects.latest('id')
                #tagobj = Tag.objects.create(tag_name=tag,creator_id=request.user)
            else:
                tagobj = tagobj.first()
            try:
                relation = NoteTag(note = noteobj,t = tagobj)
                relation.save()
            except Exception as e:
                pass
            continue
        #note.tags.add(tag) 自定义中间表不可以使用add()
        return JsonResponse({'msg':'ok'})

    @action(methods=['get','post'], detail=False)
    def listNoteByTag(self,request,*args,**kwargs):
        tag_id = request.query_params.get('tag_id', None)
        user = request.query_params.get('user_id', None)
        tagobj = Tag.objects.get(id=tag_id)
        tag_name = tagobj.tag_name
        self.queryset = tagobj.note_set.all()
        self.queryset= self.queryset.filter(is_delete=False,writer_id = user).order_by('-note_create')
        self.serializer_class = NoteSerializer
        queryset = self.filter_queryset(self.get_queryset())
        # 在数据库中获取分页的数据
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            ret = self.get_paginated_response(serializer.data)
            ret.data['tag_name'] = tag_name
            return ret

        serializer = self.get_serializer(queryset, many=True)
        ret = JsonResponse(serializer.data,safe=False)
        ret.data['tag_name'] = tag_name
        return ret

    def list(self, request, *args, **kwargs):
        self.queryset = Tag.objects.filter(creator_id=request.user)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
'''def upload(request):
    if request.method =='POST':
        data = request.FILES
        img = data.get('img')
        Image.objects.create(img=img)
        return'''

class ImageUploadCreateAPIView(CreateAPIView):
    """后台定义前段上传图片到服务端的接口"""
    queryset = Image.objects.all()
    serializer_class = ImageUploadSerializer
