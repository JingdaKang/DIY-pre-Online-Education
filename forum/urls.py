"""forum URL Configuration

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
from django.contrib import admin
from django.urls import path
from forum import views

urlpatterns = [
    path('topics/', views.topics),
    path('login', views.login_user),
    path('register', views.register),
    path('logout', views.logout_user),
    path('topic/<topic_id>/', views.topic_detail),
    path('userPost/', views.user_post_detail),
    path('sections/', views.section_name),
    path('section/<topic_id>/', views.topic_detail),
    path('search/', views.search),
    path('userinfo/', views.user_info_detail),
    path('addReply', views.add_reply),
    path('deleteReply', views.delete_reply),
    path('addTopic', views.add_topic),
    path('group/', views.group_name),
    path('userGroup/', views.user_group_name),
    path('userNotInGroup/', views.user_not_in_group_name),
    path('discuss/', views.group_discuss),
    path('addGroup', views.add_group),
    path('discuss/<discuss_id>/', views.discuss_detail),
    path('addDiscussReply', views.add_discuss_reply),
    path('addGroupDiscuss', views.add_discuss),
    path('userDiscuss', views.user_discuss_detail),
    path('deleteDiscussReply', views.delete_discuss_reply),
    path('praise', views.praise),
    path('collect', views.collect),
    path('userCollect', views.user_collect),
    path('deleteCollect', views.delete_collect),
    path('follow', views.follow),
    path('unfollow', views.unfollow),
    path('userFollowing', views.user_following),
    path('userFollower', views.user_follower),
    path('focusDiscuss', views.focus_discuss),
    path('userFocus', views.user_focus),
    path('applyGroup', views.apply_join_group),
    path('receiveApply', views.user_receive_apply),
    path('handleApply', views.handle_apply),
    path('recommendGroup', views.recommend_group),
    path('addMessage', views.add_message),
    path('message', views.user_message),
    path('deleteMessage', views.delete_message),
    path('readMessage', views.read_message),
    path('userRank', views.user_rank),
    path('topicRank', views.topic_rank),
    path('updateUserInfo', views.update_user_info),
    path('updateUserAvatar', views.update_user_avatar),
    path('editGroupDiscuss', views.edit_discuss),
    path('editTopic', views.edit_topic),
    path('addQuestion', views.add_question_topic),
    path('addRecommendAnswer', views.add_recommend_answer)

]
