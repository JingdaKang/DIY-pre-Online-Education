from django.contrib import admin
from django.conf.urls import url, include
from IAsystem import views

urlpatterns = [
    url(r'user/', views.get_user),# N
    url(r'subjects/', views.get_subject), # N
    url(r'majors/', views.get_major), # N
    url(r'login/', views.post_login), # N
    url(r'register/', views.register), # N
    url(r'search/', views.search), # N
    url(r'update_info/', views.update_info), #ignore
    url(r'password/', views.change_password),#ignore
    url(r'avatar/', views.get_avatar), # N
    url(r'release_request/', views.release_request),#done
    url(r'get_requests/', views.get_requests),#N
    url(r'get_hot_requests/', views.get_hot_requests),#N
    url(r'get_question/', views.get_question),#N
    url(r'get_request/', views.get_request),#N
    url(r'submit_answer/', views.submit_answer),#done
    url(r'rate_answer/', views.rate_answer),
    url(r'rate_resource/', views.rate_resource),
    url(r'uploadFiles/', views.upload_files),
    url(r'download/(?P<resource_id>.*)/(?P<filename>.*)', views.download),
    url(r'resources/', views.get_resources),
    url(r'answers/', views.get_answers),
    url(r'search_by_condition/', views.search_by_condition),
    url(r'activate_question/', views.activate_question),
    url(r'activate_request/', views.activate_request),
    url(r'end_question/', views.end_question),
    url(r'accept_answer/', views.accept_answer),
    url(r'submit_base/', views.submit_base),
    url(r'get_store_questions/', views.get_store_questions),
    url(r'batch_download/', views.batch_download),
    url(r'download_zip/', views.download_zip),
    url(r'send_to_note/',views.send_to_note)# TODO

]
