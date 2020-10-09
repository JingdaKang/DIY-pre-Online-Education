from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from backend.models import User, Team
from backend.models import NoteBook, Tag
from notifications.signals import notify

from django.contrib import auth
from django.db import connection, transaction

cursor = connection.cursor()

# Create your views here.
from user.serializers import TeamSerializer


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class UserViewSet(ModelViewSet):

    # queryset 和 serializer_class  必须指定
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def retrieve(self, request, pk=None):
        """ 用户详情 """
        # 获取实例
        user = self.get_object()
        # 序列化
        serializer = self.get_serializer(user)
        return JsonResponse(serializer.data)

    def create(self, request, *args, **kwargs):
        """ 创建用户 """

        serializer = self.get_serializer(data=request.data)
        # save 前必须先调用 is_valid()
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        """ 删除用户 """


    def list(self, request, *args, **kwargs):
        """ 获取用户列表 """

def login(request):

    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        obj = auth.authenticate(request,username=username, password=password)
        if obj:
            # 登陆成功
            auth.login(request,user=obj)
            print(request.user.id)
            #return
            ret = JsonResponse({'code': 'ok', 'message': '账号密码验证成功','user_name':request.user.username,'user_id':request.user.id})
            return ret
    # 登录失败
    return JsonResponse({'code':'no','message':'验证失败'})

# 注册
def register(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        obj = User.objects.create_user(username=username,password=password)
        #新建默认笔记本
        NoteBook.objects.create(
            notebook_name="默认笔记本",
            creator_id= obj
        )
        #新建错题本标签
        Tag.objects.create(
            tag_name="错题本",
            creator_id=obj
        )
        return JsonResponse({'code': 'ok', 'message': '注册成功，请登录'})
    # 注册失败，重新注册
    return JsonResponse({'code':'no','message':'注册失败'})

#判断用户名是否存在
def checkUsername(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get("username")
        count = User.objects.filter(username=username).count()
        if count == 0:
            return JsonResponse({'code':'ok','message':'用户不存在'})
        return JsonResponse({'code': 'no', 'message': '用户已存在'})

#验证用户是否登录
def validator(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return JsonResponse({'code':'ok','message':'用户已登录'})
        return JsonResponse({'code': 'no', 'message': '用户未登录'})
    return JsonResponse({'code': 'no', 'message': 'error'})

#注销登录
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return JsonResponse({'code': 'ok', 'message': '成功注销登录'})
    return JsonResponse({'code': 'no', 'message': 'error'})

class myPagination(PageNumberPagination):
    """自定义分页"""
    # 每页显示多少条数据
    page_size = 6
    # url/?page=1&size=5, 改变默认每页显示的个数
    page_size_query_param = "size"
    # 最大个数不超过15条
    max_page_size = 8
    # 获取页码数
    page_query_param = "page"

class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    pagination_class = myPagination

    @action(methods=['post'], detail=False)
    def isLock(self, request, *args, **kwargs):
        '''判断是否有成员正在编辑'''
        data = request.data
        team = Team.objects.filter(id=data['team_id'])
        if team.first().locked_by != None :
            return JsonResponse({"code":"no","msg":"有成员正在编辑，请稍后再试"})
        else:
            team.update(locked_by = request.user)
            return JsonResponse({"code":"yes","msg":"可以编辑"})

    @action(methods=['post'], detail=False)
    def cancelLock(self, request, *args, **kwargs):
        '''取消对编辑内容的锁定'''
        data = request.data
        team = Team.objects.filter(id=data['team_id'])
        team.update(locked_by = None)
        return JsonResponse({"code":"yes","msg":"可以编辑"})

    @action(methods=['post'], detail=False)
    def updateName(self, request, *args, **kwargs):
        '''修改团队名称'''

        data = request.data
        team = Team.objects.get(id=data['team_id'])
        if team.locked_by != request.user :
            return JsonResponse({"msg":"error"})
        team.team_name = data['team_name']
        team.modifier_id = request.user
        team.locked_by = None
        team.save()
        serializer = self.get_serializer(team)

        return JsonResponse(serializer.data)

    def create(self, request, *args, **kwargs):
        '''新建一个团队'''
        leader = request.user
        team_name = request.data['team_name']
        with transaction.atomic():
            cursor.execute("insert into tb_team(team_name,leader_id,modifier_id,team_create) values \
                (%s,%s,%s,now());",(team_name,leader.id,leader.id))
            team_obj = Team.objects.latest('id')
        #team_obj = Team.objects.create(team_name = team_name,leader_id = leader,modifier_id=leader)
        team_obj.members.add(leader)
        #新建默认笔记本
        cursor.execute("insert into tb_notebook(notebook_name,creator_id,modifier_id,team_id,notebook_create,\
            notebook_modify) values (%s,%s,%s,%s,now(),now());",("默认团队笔记本",leader.id,leader.id,team_obj.id))
        '''NoteBook.objects.create(
            notebook_name="默认团队笔记本",
            creator_id= leader,
            modifier_id=leader,
            team_id = team_obj
        )'''
        serializers = self.get_serializer(team_obj)
        return JsonResponse(serializers.data)

    @action(methods=['get'], detail=False)
    def listByUser(self,request,*args,**kwargs):
        '''展示所属团队'''
        self.queryset = request.user.member_team.all().order_by('-id')
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            ret = self.get_paginated_response(serializer.data)
            return ret

        serializer = self.get_serializer(queryset, many=True)
        ret = JsonResponse(serializer.data,safe=False)
        return ret

    @action(methods=['post'], detail=False)
    def invite(self,request,*args,**kwargs):
        '''邀请成员加入团队'''
        data = request.data
        team_id = data['team_id']
        member_name = data['member_name']
        member = User.objects.get(username = member_name)
        team = Team.objects.get(id = team_id)
        notify.send(request.user,
                    recipient = member,
                    verb = '邀请你加入',
                    target = team)
        return JsonResponse({"msg":"成功发送邀请"})

    @action(methods=['post','get'], detail=False)
    def refuseInvitation(self,request,*args,**kwargs):
        '''拒绝加入团队邀请'''
        data = request.data
        team_id = data['targetId']
        recipient_id = data['actorId']

        recipient = User.objects.get(id = recipient_id)
        team = Team.objects.get(id = team_id)

        notify.send(request.user,
                    recipient = recipient,
                    verb = '拒绝加入',
                    target = team)
        return JsonResponse({"msg":"成功拒绝邀请"})

    @action(methods=['post','get'], detail=False)
    def acceptInvitation(self,request,*args,**kwargs):
        '''接受加入团队邀请'''
        data = request.data
        team_id = data['targetId']
        recipient_id = data['actorId']

        recipient = User.objects.get(id = recipient_id)
        team = Team.objects.get(id = team_id)
        team.members.add(request.user)

        notify.send(request.user,
                    recipient = recipient,
                    verb = '同意加入',
                    target = team)
        return JsonResponse({"msg":"成功接受邀请"})

    '''@action(methods=['post'], detail=False)
    def invite(self, request, *args, **kwargs):
        data = request.data
        team_id = data['team_id']
        member_name = data['member_name']
        member = User.objects.get(username = member_name)
        team = Team.objects.get(id=team_id)
        team.members.add(member)
        return JsonResponse({"member":member_name})'''



