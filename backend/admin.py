from django.contrib import admin

# Register your models here.
from backend.models import *


class user_Admin(admin.ModelAdmin):
    list_display = ['username', 'password', 'email', 'user_avatar', 'user_gender', 'user_bir', 'user_edu', 'user_addr',
                    'user_tel', 'type', 'user_reg', 'score', 'user_status',
                    'user_following_num', 'user_follower_num', 'user_credit']
    search_fields = ['username']  # 搜索栏
    list_filter = ['user_bir', 'user_status', 'type']  # 过滤器


# 论坛系统
class section_Admin(admin.ModelAdmin):
    list_display = ['section_id', 'section_name']
    search_fields = ['section_name']


class forumFile_Admin(admin.ModelAdmin):
    list_display = ['file_id', 'user_id', 'file_name', 'file_url']
    search_fields = ['file_name']
    list_filter = ['user_id']


class topic_Admin(admin.ModelAdmin):
    list_display = ['topic_id', 'section_id', 'user_id', 'topic_title',
                    'topic_time', 'topic_reply_time', 'topic_click_num', 'topic_reply_num',
                    'topic_collect_num', 'topic_like_num', 'topic_hot_num']
    search_fields = ['topic_title']
    list_filter = ['topic_id', 'section_id', 'user_id']


class reply_Admin(admin.ModelAdmin):
    list_display = ['reply_id', 'user_id', 'reply_topic_id',
                    'reply_time', 'reply_like_num', 'reply_content']
    list_filter = ['reply_id', 'user_id', 'reply_topic_id']


# class collect_Admin(admin.ModelAdmin):
#     list_display = ['collect_id','user_id','topic_id']
#     search_fields = []
#     list_filter = []
#
#
# class follow_Admin(admin.ModelAdmin):
#     list_display = ['follow_id', 'follow_by_user', 'follow_on_user']
#     search_fields = []
#     list_filter = []
#
#
# class like_Admin(admin.ModelAdmin):
#     list_display = ['like_id', 'like_type','like_user_id','like_content_id']
#     search_fields = []
#     list_filter = []
#
#
# class message_Admin(admin.ModelAdmin):
#     list_display = ['message_id' ,'message_send_user' ,'message_receive_user'
#     ,'message_read','message_related_type' ,'message_related_id' ,'message_content'
#     ,'message_time']
#     search_fields = []
#     list_filter = []


class group_Admin(admin.ModelAdmin):
    list_display = ['group_id', 'group_name', 'group_owner_id']
    search_fields = ['group_name']
    list_filter = ['group_id', 'group_owner_id']


class discuss_Admin(admin.ModelAdmin):
    list_display = ['discuss_id', 'group_id', 'user_id', 'discuss_title',
                    'discuss_click_num', 'discuss_reply_num', 'discuss_hot_num',
                    'discuss_time']
    search_fields = ['discuss_title']
    list_filter = ['discuss_id', 'group_id', 'user_id']


class discussReply_Admin(admin.ModelAdmin):
    list_display = ['discuss_reply_id', 'discuss_user_id', 'discuss_reply_discuss_id',
                    'discuss_reply_time']
    list_filter = ['discuss_reply_id', 'discuss_user_id', 'discuss_reply_discuss_id']


class groupMember_Admin(admin.ModelAdmin):
    list_display = ['group_menber_id', 'group_id', 'group_user_id']
    list_filter = ['group_menber_id', 'group_id', 'group_user_id']


# class groupApply_Admin(admin.ModelAdmin):
#     list_display = ['group_apply_id' ,'group_id' ,'group_user_id','group_apply_message']
#     search_fields = []
#     list_filter = []


# class focusDiscuss_Admin(admin.ModelAdmin):
#     list_display = ['focus_id','focus_user','focus_discuss']
#     search_fields = []
#     list_filter = []


# class questionToTopic_Admin(admin.ModelAdmin):
#     list_display = ['question_topic_id','topic_id','question_id']
#     search_fields = []
#     list_filter = []


# 智能问答系统
class resource_Admin(admin.ModelAdmin):
    list_display = ['resource_id', 'time', 'location', 'score', 'number', 'request', 'user']
    list_filter = ['number', 'time', 'number', 'request', 'user']


class request_Admin(admin.ModelAdmin):
    list_display = ['request_id', 'context', 'status', 'number', 'stime', 'etime', 'score', 'subject', 'user']
    search_fields = ['context']
    list_filter = ['status', 'number', 'subject', 'user']


class subject_Admin(admin.ModelAdmin):
    list_display = ['subject_id', 'subject_name', 'major']
    search_fields = ['subject_name']
    list_filter = ['major']


class answer_Admin(admin.ModelAdmin):
    list_display = ['answer_id', 'context', 'time', 'upload_time', 'status','from_forum', 'score', 'question', 'user']
    list_filter = ['time', 'score', 'status','from_forum', 'question', 'user']


class question_Admin(admin.ModelAdmin):
    list_display = ['question_id', 'context', 'status', 'number', 'stime', 'etime', 'score', 'subject', 'user']
    search_fields = ['context']
    list_filter = ['status', 'number', 'subject', 'user']


class base_question_Admin(admin.ModelAdmin):
    list_display = ['base_question_id', 'description', 'answer', 'subject']
    search_fields = ['description']
    list_filter = ['subject']


class major_Admin(admin.ModelAdmin):
    list_display = ['major_id', 'major_name']
    search_fields = ['major_name']


# 考试系统
class examCourse_Admin(admin.ModelAdmin):
    list_display = ['name', 'tid']
    search_fields = ['name']
    list_filter = ['tid']


class examQuestion_Admin(admin.ModelAdmin):
    list_display = ['type', 'tid', 'cid', 'chapter', 'section', 'count']
    list_filter = ['type', 'tid', 'cid', 'count']


class examSimple_Admin(admin.ModelAdmin):
    list_display = ['content', 'choice1', 'choice2', 'choice3', 'choice4'
        , 'answer', 'qid', 'picture']
    search_fields = ['content']
    list_filter = ['qid']


class examMultiple_Admin(admin.ModelAdmin):
    list_display = ['content', 'choice1', 'choice2', 'choice3', 'choice4'
        , 'answer', 'qid', 'picture']
    search_fields = ['content']
    list_filter = ['qid']


class examBlank_Admin(admin.ModelAdmin):
    list_display = ['content', 'answer', 'qid', 'picture']
    search_fields = ['content']
    list_filter = ['qid']


class examJudge_Admin(admin.ModelAdmin):
    list_display = ['content', 'answer', 'qid', 'picture']
    search_fields = ['content']
    list_filter = ['qid']


class examSubjective_Admin(admin.ModelAdmin):
    list_display = ['content', 'answer', 'qid', 'picture']
    search_fields = ['content']
    list_filter = ['qid']


class exam_Admin(admin.ModelAdmin):
    list_display = ['tid', 'cid', 'name', 'pid', 'start_time', 'end_time', 'status']
    search_fields = ['name']
    list_filter = ['tid', 'cid', 'start_time', 'end_time', 'status']


class examPaper_Admin(admin.ModelAdmin):
    list_display = ['name', 'tid', 'cid', 'qidlist']
    search_fields = ['name']
    list_filter = ['tid', 'cid']


class studentChooseCourse_Admin(admin.ModelAdmin):
    list_display = ['uid', 'cid']
    list_filter = ['uid', 'cid']


class examAnswer_Admin(admin.ModelAdmin):
    list_display = ['uid', 'eid', 'qid', 'answer', 'score', 'is_right'
        , 'cloud', 'update_time', 'is_read']
    list_filter = ['uid', 'eid', 'score', 'is_right'
        , 'cloud', 'update_time', 'is_read']


class examScore_Admin(admin.ModelAdmin):
    list_display = ['eid', 'uid', 'obj_score', 'sub_score', 'total_score']
    list_filter = ['eid', 'uid']


class examSection_Admin(admin.ModelAdmin):
    list_display = ['cid', 'chapter_count', 'chapter', 'section_count', 'section']
    search_fields = ['chapter', 'section']
    list_filter = ['cid']


class examTeacherCloud_Admin(admin.ModelAdmin):
    list_display = ['tid', 'sid', 'aid', 'cloud', 'update_time', 'is_read']
    list_filter = ['tid', 'sid', 'cloud', 'is_read']


# 云笔记
class tag_Admin(admin.ModelAdmin):
    list_display = ['tag_name', 'tag_create', 'creator_id']
    search_fields = ['tag_name']
    list_filter = ['creator_id']


class team_Admin(admin.ModelAdmin):
    list_display = ['team_name', 'team_desc', 'team_create', 'team_modify'
        , 'modifier_id', 'leader_id', 'locked_by']
    search_fields = ['team_name']
    list_filter = ['modifier_id', 'leader_id', 'locked_by']


class note_Admin(admin.ModelAdmin):
    list_display = ['note_title', 'note_text', 'note_type', 'note_create'
        , 'note_modify', 'note_delete', 'writer_id', 'team_id', 'modifier_id'
        , 'notebook_id', 'locked_by', 'is_delete']
    search_fields = ['note_title']
    list_filter = ['note_type', 'writer_id', 'team_id', 'modifier_id'
        , 'notebook_id', 'locked_by']


# class noteTag_Admin(admin.ModelAdmin):
#     list_display = ['note','t']
#     search_fields = []
#     list_filter = []


class noteBook_Admin(admin.ModelAdmin):
    list_display = ['notebook_name', 'notebook_create', 'notebook_modify'
        , 'creator_id', 'team_id', 'modifier_id', 'locked_by']
    search_fields = ['notebook_name']
    list_filter = ['creator_id', 'team_id', 'modifier_id', 'locked_by']


# 作业系统
class course_Admin(admin.ModelAdmin):
    list_display = ['id', 'name',  'number', 'maxnum'
        , 'tid','stime','time','status']
    search_fields = ['name']
    list_filter = ['name',  'number', 'maxnum'
        , 'tid','stime','time','status']


class user_course_Admin(admin.ModelAdmin):
    list_display = ['id', 'sname', 'cid']
    search_fields = ['sname']
    list_filter = ['cid']


class work_Admin(admin.ModelAdmin):
    list_display = ['id', 'cid', 'ctime', 'chapter', 'deadline', 'release'
        , 'finishnum', 'qnum']
    list_filter = ['cid', 'release']


class simple_Admin(admin.ModelAdmin):
    list_display = ['id', 'content', 'choice1', 'choice2', 'choice3'
        , 'choice4', 'answer', 'wid', 'picture', 'explain']
    list_filter = ['wid']


class multiple_Admin(admin.ModelAdmin):
    list_display = ['id', 'content', 'choice1', 'choice2', 'choice3'
        , 'choice4', 'answer', 'wid', 'picture', 'explain']
    list_filter = ['wid']


class subjective_Admin(admin.ModelAdmin):
    list_display = ['id', 'content', 'answer', 'wid', 'picture', 'explain']
    search_fields = ['content']
    list_filter = ['wid']


class blank_Admin(admin.ModelAdmin):
    list_display = ['id', 'content', 'answer', 'wid', 'picture', 'explain']
    list_filter = ['wid']


class judge_Admin(admin.ModelAdmin):
    list_display = ['id', 'content', 'answer', 'wid', 'picture', 'explain']
    list_filter = ['wid']


# class user_work_Admin(admin.ModelAdmin):
#     list_display = ['id','wid','sid','update' ,'file' ,'comment'
#     ,'score','good' ,'finish' ,'ifscore']
#     search_fields = []
#     list_filter = []
#
#
# class user_question_Admin(admin.ModelAdmin):
#     list_display = ['id' ,'sid' ,'wid','qid' ,'number','answer' ,'ischeck'
#     ,'judge' ,'cloud' ,'type' ,'upload_time' ,'is_read']
#     search_fields = []
#     list_filter = []
#
#
# class work_question_Admin(admin.ModelAdmin):
#     list_display = ['id','wid','qid','number','type']
#     search_fields = []
#     list_filter = []
#
#
# class sharedArea_Admin(admin.ModelAdmin):
#     list_display = ['id','cid','admin_id']
#     search_fields = []
#     list_filter = []
#
#
# class shared_file_Admin(admin.ModelAdmin):
#     list_display = ['id','data_name','data_file','upload_id','update_time','aid']
#     search_fields = []
#     list_filter = []
#
#
# class work_message_Admin(admin.ModelAdmin):
#     list_display = ['id','tid','sid','tittle','message','read']
#     search_fields = []
#     list_filter = []
#
#
# class goodWork_Admin(admin.ModelAdmin):
#     list_display = ['id','wid','cid','qid','tid','sid','answer','upload_time','is_read']
#     search_fields = []
#     list_filter = []


admin.site.register(User, user_Admin)
# 论坛系统
admin.site.register(Section, section_Admin)
admin.site.register(ForumFile, forumFile_Admin)
admin.site.register(Topic, topic_Admin)
admin.site.register(Reply, reply_Admin)
admin.site.register(Group, group_Admin)
admin.site.register(Discuss, discuss_Admin)
admin.site.register(DiscussReply, discussReply_Admin)
admin.site.register(GroupMember, groupMember_Admin)
# admin.site.register(Collect, collect_Admin)
# admin.site.register(Follow, follow_Admin)
# admin.site.register(Like, like_Admin)
# admin.site.register(Message, message_Admin)

# 智能问答系统
admin.site.register(Resource, resource_Admin)
admin.site.register(Request, request_Admin)
admin.site.register(Subject, subject_Admin)
admin.site.register(Answer, answer_Admin)
admin.site.register(Question, question_Admin)
admin.site.register(Base_question, base_question_Admin)
admin.site.register(Major, major_Admin)

# 考试系统
admin.site.register(ExamCourse, examCourse_Admin)
admin.site.register(ExamQuestion, examQuestion_Admin)
admin.site.register(ExamSimple, examSimple_Admin)
admin.site.register(ExamMultiple, examMultiple_Admin)
admin.site.register(ExamBlank, examBlank_Admin)
admin.site.register(ExamJudge, examJudge_Admin)
admin.site.register(ExamSubjective, examSubjective_Admin)
admin.site.register(Exam, exam_Admin)
admin.site.register(ExamPaper, examPaper_Admin)
admin.site.register(StudentChooseCourse, studentChooseCourse_Admin)
admin.site.register(ExamAnswer, examAnswer_Admin)
admin.site.register(ExamScore, examScore_Admin)
admin.site.register(ExamSection, examSection_Admin)
admin.site.register(ExamTeacherCloud, examTeacherCloud_Admin)

# 云笔记
admin.site.register(Tag, tag_Admin)
admin.site.register(Team, team_Admin)
admin.site.register(Note, note_Admin)
# admin.site.register(NoteTag,noteTag_Admin)
admin.site.register(NoteBook, noteBook_Admin)

# 作业系统
admin.site.register(Course, course_Admin)
admin.site.register(User_Course, user_course_Admin)
admin.site.register(Work, work_Admin)
admin.site.register(Simple, simple_Admin)
admin.site.register(Multiple, multiple_Admin)
admin.site.register(Subjective, subjective_Admin)
admin.site.register(Blank, blank_Admin)
admin.site.register(Judge, judge_Admin)
# admin.site.register(User_Work, user_work_Admin)
# admin.site.register(User_Question, user_question_Admin)
# admin.site.register(Work_Question, work_question_Admin)
# admin.site.register(SharedArea, sharedArea_Admin)
# admin.site.register(Share_File, shared_file_Admin)
# admin.site.register(Work_Message, work_message_Admin)
# admin.site.register(GoodWork, goodWork_Admin)
