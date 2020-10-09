from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from notifications.models import Notification
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from notice.serializers import NotificationSerializer



class NoticeViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    @action(methods=['get'], detail=False)
    def getUnreadNotice(self,request,*args,**kwargs):
        user = request.user
        unread = user.notifications.unread()
        serializer = self.get_serializer(unread, many=True)
        return JsonResponse(serializer.data,safe=False)

    @action(methods=['get'], detail=False)
    def getReadNotice(self,request,*args,**kwargs):
        user = request.user
        read = user.notifications.read()
        serializer = self.get_serializer(read, many=True)
        return JsonResponse(serializer.data,safe=False)

    @action(methods=['get','post'], detail=False)
    def readAll(self,request,*args,**kwargs):
        user = request.user
        unread = user.notifications.unread()
        unread.mark_all_as_read()
        serializer = self.get_serializer(user.notifications.unread(), many=True)
        return JsonResponse(serializer.data,safe=False)

    @action(methods=['get','post'], detail=False)
    def readNotice(self,request,*args,**kwargs):
        data = request.data
        notice_id = data['noticeId']
        notice = request.user.notifications.get(id=notice_id)
        notice.mark_as_read()
        unread = request.user.notifications.unread()
        count = len(unread)
        serializer = self.get_serializer(notice)
        return JsonResponse({"unreadCount":count})