"""OnlineEducation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView, RedirectView
# 新加的 -zxl
import notifications.urls
from rest_framework import routers
from notes import views as notes_views
from note_question.views import  WorkErrorBookAPIView, ExamErrorBookAPIView,ExamGoodAnswerAPIView, WorkGoodAnswerAPIView
from user import views as user_views
from notice import views as notice_views
from note_question import views as question_views
from django.views.decorators.csrf import csrf_exempt
router = routers.DefaultRouter()

router.register(r'note', notes_views.NoteViewSet)
router.register(r'notebook', notes_views.NoteBookViewSet)
router.register(r'user',user_views.UserViewSet)
router.register(r'tag',notes_views.TagViewSet)
router.register(r'team',user_views.TeamViewSet)
router.register(r'notice',notice_views.NoticeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include("backend.urls")),
    url(r'^iasystem/',include("IAsystem.urls")),
    url(r'^exam/', include("exam.urls")),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('forum/', include("forum.urls")),
    
    url(r'^api/', include("work.urls")),
    path('Question/<path>',serve,{'document_root':'Question'}),
    path('static/<path>',serve,{'document_root':'static'}),
    path('workFile/<path>',serve,{'document_root':'workFile'}),
    path('Share/<path>',serve,{'document_root':'Share'}),
# 新加的 -zxl
    path('api/', include(router.urls)),
    path('api/img_upload/', notes_views.ImageUploadCreateAPIView.as_view()),
    path('api/errorbook/exam/', ExamErrorBookAPIView.as_view()),
    path('api/errorbook/work/', WorkErrorBookAPIView.as_view()),
    path('api/goodanswer/exam/', ExamGoodAnswerAPIView.as_view()),
    path('api/goodanswer/work/', WorkGoodAnswerAPIView.as_view()),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('api/checkUsername/',user_views.checkUsername),
    path('api/validator/',user_views.validator),
    #path(r'^$',
    #RedirectView.as_view(url='http://127.0.0.1:8888/#/Login')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
]
