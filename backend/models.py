from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
import datetime


# Create your models here.

# 用户表
class User(AbstractUser):
    user_avatar = models.ImageField(upload_to="avatar/", null=True, blank=True, default="avatar/default.png",
                                    verbose_name="头像")
    user_gender = models.CharField(max_length=20, choices=(('M', '男'), ('F', '女'), ('D', '未知')), default='D',
                                   verbose_name="性别")
    user_bir = models.DateField(verbose_name="出生日期", null=True, blank=True)
    user_edu = models.TextField(verbose_name="学历信息", null=True, blank=True)
    user_addr = models.TextField(verbose_name="籍贯", null=True, blank=True)
    user_tel = models.CharField(max_length=20, verbose_name="手机号", null=True, blank=True)
    type = models.CharField(max_length=20, choices=(('T', '教师'), ('S', '学生'), ('A', '管理员')), default='S',
                            verbose_name="账户类型")
    user_reg = models.DateField(verbose_name="用户注册时间", default=datetime.date.today)
    score = models.IntegerField(verbose_name="积分", default=0)
    user_status = models.BooleanField(verbose_name="发帖", default=True)
    user_following_num = models.IntegerField(verbose_name="关注数", default=0)
    user_follower_num = models.IntegerField(verbose_name="粉丝数", default=0)
    user_credit = models.IntegerField(verbose_name="贡献度", default=0)

    class Meta:
        db_table = "user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


###########################################################################################################
# 论坛系统
# 分区表
class Section(models.Model):
    section_id = models.AutoField(primary_key=True, max_length=20, verbose_name="分区id")
    section_name = models.CharField(max_length=100, verbose_name="分区名", unique=True)

    class Meta:
        db_table = "forum_section"
        verbose_name = "论坛分区"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.section_name


# 文件表
class ForumFile(models.Model):
    file_id = models.AutoField(primary_key=True, max_length=20, verbose_name="文件id")
    user_id = models.ForeignKey(User, verbose_name="上传用户id", on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100, verbose_name="文件名")
    file_url = models.FileField(upload_to="file/", default="file/null.txt", verbose_name="地址")

    class Meta:
        db_table = "forum_file"
        verbose_name = "论坛文件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.file_name


# 主题表
class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True, max_length=20, verbose_name="主题id")
    section_id = models.ForeignKey(Section, verbose_name="归属分区", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name="发帖用户", on_delete=models.CASCADE)
    topic_title = models.CharField(max_length=100, verbose_name="贴子标题")
    topic_click_num = models.IntegerField(verbose_name="点击数", default=0)
    topic_reply_num = models.IntegerField(verbose_name="回复数", default=0)
    topic_collect_num = models.IntegerField(verbose_name="收藏数", default=0)
    topic_like_num = models.IntegerField(verbose_name="点赞数", default=0)
    topic_hot_num = models.IntegerField(verbose_name="热度", default=0)
    topic_time = models.DateTimeField(verbose_name="发帖时间")
    topic_reply_time = models.DateTimeField(verbose_name="最后回帖时间")
    topic_content = models.TextField(verbose_name="内容", default="")
    topic_content_file_check = models.BooleanField(verbose_name="是否包含附件", default=False)
    file_id = models.ForeignKey(ForumFile, verbose_name="附件id", null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "forum_topic"
        verbose_name = "论坛主题"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.topic_title


# 回复表
class Reply(models.Model):
    reply_id = models.AutoField(primary_key=True, max_length=20, verbose_name="回复id")
    user_id = models.ForeignKey(User, verbose_name="回复用户", on_delete=models.CASCADE)
    reply_topic_id = models.ForeignKey(Topic, verbose_name="回复主贴", on_delete=models.CASCADE)
    reply_content = models.TextField(verbose_name="回复内容")
    reply_time = models.DateTimeField(verbose_name="回帖时间")
    reply_like_num = models.IntegerField(verbose_name="点赞数", default=0)

    class Meta:
        db_table = "forum_reply"
        verbose_name = "论坛回复"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.reply_id)


# 收藏表
class Collect(models.Model):
    collect_id = models.AutoField(primary_key=True, max_length=20, verbose_name="收藏记录ID")
    user_id = models.ForeignKey(User, verbose_name="收藏用户ID", on_delete=models.CASCADE)
    topic_id = models.ForeignKey(Topic, verbose_name="收藏主贴ID", on_delete=models.CASCADE)

    class Meta:
        db_table = "forum_collect"
        verbose_name = "论坛收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.collect_id)


# 关注表
class Follow(models.Model):
    follow_id = models.AutoField(primary_key=True, max_length=20, verbose_name="关注记录ID")
    follow_by_user = models.ForeignKey(User, related_name='following', verbose_name="粉丝用户ID", on_delete=models.CASCADE)
    follow_on_user = models.ForeignKey(User, related_name='followed', verbose_name="被关注用户ID", on_delete=models.CASCADE)

    class Meta:
        db_table = "forum_follow"
        verbose_name = "论坛关注"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.follow_id)


# 点赞表
class Like(models.Model):
    like_id = models.AutoField(primary_key=True, max_length=20, verbose_name="点赞记录ID")
    like_type = models.IntegerField(verbose_name="类型，主贴为1，回帖为2")
    like_user_id = models.ForeignKey(User, verbose_name="用户ID", on_delete=models.CASCADE)
    like_content_id = models.IntegerField(verbose_name="点赞对象ID")

    class Meta:
        db_table = "forum_like"
        verbose_name = "论坛点赞"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.like_id)


# 消息表
class Message(models.Model):
    message_id = models.AutoField(primary_key=True, max_length=20, verbose_name="消息ID")
    message_send_user = models.ForeignKey(User, verbose_name="发送用户ID", related_name='send_user',
                                          on_delete=models.CASCADE)
    message_receive_user = models.ForeignKey(User, verbose_name="接收用户ID", related_name='receive_user',
                                             on_delete=models.CASCADE)
    message_read = models.BooleanField(verbose_name="是否已读", default=False)
    message_related_type = models.IntegerField(verbose_name="相关类型，帖子为1，小组讨论为2", default=0)
    message_related_id = models.IntegerField(verbose_name="对应帖子或讨论id", null=True, blank=True)
    message_content = models.TextField(verbose_name="内容")
    message_time = models.DateTimeField(verbose_name="消息发送时间", default=datetime.datetime.now())

    class Meta:
        db_table = "forum_message"
        verbose_name = "论坛消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.message_id)


# 小组表
class Group(models.Model):
    group_id = models.AutoField(primary_key=True, max_length=20, verbose_name="小组id")
    group_name = models.CharField(max_length=100, verbose_name="小组名", unique=True)
    group_owner_id = models.ForeignKey(User, verbose_name="小组长", on_delete=models.CASCADE)

    class Meta:
        db_table = "forum_group"
        verbose_name = "论坛小组"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group_name


# 小组讨论表
class Discuss(models.Model):
    discuss_id = models.AutoField(primary_key=True, max_length=20, verbose_name="小组讨论id")
    group_id = models.ForeignKey(Group, verbose_name="归属小组", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name="发布用户", on_delete=models.CASCADE)
    discuss_title = models.CharField(max_length=100, verbose_name="讨论贴标题")
    discuss_click_num = models.IntegerField(verbose_name="点击数", default=0)
    discuss_reply_num = models.IntegerField(verbose_name="回复数", default=0)
    discuss_hot_num = models.IntegerField(verbose_name="热度", default=0)
    discuss_time = models.DateTimeField(verbose_name="发布时间")
    discuss_reply_time = models.DateTimeField(verbose_name="最后回复时间")
    discuss_content = models.TextField(verbose_name="内容", default="")
    discuss_content_file_check = models.BooleanField(verbose_name="是否包含附件", default=False)
    discuss_file_id = models.ForeignKey(ForumFile, verbose_name="附件id", null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "forum_discuss"
        verbose_name = "论坛小组讨论贴"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.discuss_title


# 小组讨论回复表
class DiscussReply(models.Model):
    discuss_reply_id = models.AutoField(primary_key=True, max_length=20, verbose_name="回复id")
    discuss_user_id = models.ForeignKey(User, verbose_name="回复用户", on_delete=models.CASCADE)
    discuss_reply_discuss_id = models.ForeignKey(Discuss, verbose_name="回复讨论帖", on_delete=models.CASCADE)
    discuss_reply_content = models.TextField(verbose_name="回复内容")
    discuss_reply_time = models.DateTimeField(verbose_name="回帖时间")

    class Meta:
        db_table = "forum_discuss_reply"
        verbose_name = "论坛小组回复"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.discuss_reply_id)


# 小组成员表
class GroupMember(models.Model):
    group_menber_id = models.AutoField(primary_key=True, max_length=20, verbose_name="成员记录id")
    group_id = models.ForeignKey(Group, verbose_name="小组", on_delete=models.CASCADE)
    group_user_id = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)

    class Meta:
        db_table = "forum_group_member"
        verbose_name = "论坛小组成员"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.group_menber_id)


# 小组申请表
class GroupApply(models.Model):
    group_apply_id = models.AutoField(primary_key=True, max_length=20, verbose_name="申请id")
    group_id = models.ForeignKey(Group, verbose_name="申请小组", on_delete=models.CASCADE)
    group_user_id = models.ForeignKey(User, verbose_name="申请用户", on_delete=models.CASCADE)
    group_apply_message = models.CharField(max_length=500, verbose_name="附言")

    class Meta:
        db_table = "forum_group_apply"
        verbose_name = "论坛小组申请"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.group_apply_id)


# 讨论贴关注表
class FocusDiscuss(models.Model):
    focus_id = models.AutoField(primary_key=True, max_length=20, verbose_name="记录ID")
    focus_user = models.ForeignKey(User, verbose_name="用户ID", on_delete=models.CASCADE)
    focus_discuss = models.ForeignKey(Discuss, verbose_name="被关注讨论帖ID", on_delete=models.CASCADE)

    class Meta:
        db_table = "forum_focus_discuss"
        verbose_name = "论坛讨论贴关注"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.focus_id)


# 问题贴对应表
class QuestionToTopic(models.Model):
    question_topic_id = models.AutoField(primary_key=True, max_length=20, verbose_name="问题对应帖子记录ID")
    topic_id = models.ForeignKey(Topic, verbose_name="对应帖子ID", on_delete=models.CASCADE)
    question_id = models.IntegerField(verbose_name="对应问题ID")

    class Meta:
        db_table = "forum_question"
        verbose_name = "论坛问题贴对应表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.question_topic_id)


###########################################################################################################
# 智能问答系统
# 回答表
class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True, verbose_name='回答编号')
    context = models.TextField(verbose_name='回答内容')
    time = models.DateTimeField(verbose_name='回答时间')
    score = models.IntegerField(verbose_name='评分')
    status = models.IntegerField(verbose_name='是否上星')
    from_forum = models.BooleanField(verbose_name='来自论坛',default=False)
    upload_time = models.DateTimeField(null=True, verbose_name='上传时间')
    question = models.ForeignKey(to='Question', on_delete=models.CASCADE, verbose_name='问题')
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, verbose_name='用户')

    class Meta:
        db_table = "answer"
        verbose_name = "智能问答回答"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.answer_id)


# 资源表
class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True, verbose_name='资源编号')
    time = models.DateTimeField(verbose_name='上传时间')
    location = models.CharField(max_length=60, verbose_name='地址')
    score = models.IntegerField(verbose_name='评分')
    number = models.IntegerField(verbose_name='下载次数')
    request = models.ForeignKey(to='Request', on_delete=models.CASCADE, verbose_name='需求')
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, verbose_name='用户')

    class Meta:
        db_table = "resource"
        verbose_name = "智能问答资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.resource_id)


# 类型表
class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True, verbose_name='课程编号')
    subject_name = models.CharField(max_length=15, verbose_name='课程类型')
    major = models.ForeignKey(to='Major', on_delete=models.CASCADE, verbose_name='专业')

    class Meta:
        db_table = "subject"
        verbose_name = "智能问答课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.subject_id)


# 类型表
class Major(models.Model):
    major_id = models.AutoField(primary_key=True, verbose_name='专业编号')
    major_name = models.CharField(max_length=15, verbose_name='专业类型')

    class Meta:
        db_table = "major"
        verbose_name = "智能问答专业"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.major_id)


# 需求表
class Request(models.Model):
    request_id = models.AutoField(primary_key=True, verbose_name='需求编号')
    context = models.CharField(max_length=60, verbose_name='需求内容')
    status = models.IntegerField(verbose_name='状态')
    number = models.IntegerField(verbose_name='回答数', default=0)
    stime = models.DateTimeField(verbose_name='发布时间')
    etime = models.DateTimeField(null=True, verbose_name='截止时间')
    score = models.IntegerField(verbose_name='悬赏积分')
    subject = models.ForeignKey(to='Subject', on_delete=models.CASCADE, verbose_name='科目')
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, verbose_name='用户')

    class Meta:
        db_table = "request"
        verbose_name = "智能问答需求"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.request_id)


# 问题表
class Question(models.Model):
    question_id = models.AutoField(primary_key=True, verbose_name='问题编号')
    context = models.CharField(max_length=60, verbose_name='问题内容')
    status = models.IntegerField(verbose_name='状态')
    number = models.IntegerField(verbose_name='回答数', default=0)
    stime = models.DateTimeField(verbose_name='发布时间')
    etime = models.DateTimeField(null=True, verbose_name='截止时间')
    score = models.IntegerField(verbose_name='悬赏积分')
    subject = models.ForeignKey(to='Subject', on_delete=models.CASCADE, verbose_name='科目')
    user = models.ForeignKey(to='User', on_delete=models.CASCADE, verbose_name='用户')

    class Meta:
        db_table = "question"
        verbose_name = "智能问答问题"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.question_id)


# 基本问题表
class Base_question(models.Model):
    base_question_id = models.AutoField(primary_key=True, verbose_name='问题编号')
    description = models.CharField(max_length=60, verbose_name='问题描述')
    answer = models.TextField(verbose_name='参考答案')
    subject = models.ForeignKey(to='Subject', on_delete=models.CASCADE, verbose_name='类型')

    class Meta:
        db_table = "base_question"
        verbose_name = "智能问答基本问题"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.base_question_id)


#########################################################
# 考试系统
# 课程模型
class ExamCourse(models.Model):
    name = models.CharField(verbose_name="课程名", max_length=30, unique=True)
    tid = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, db_column='tid')  # 任课教师
    stime = models.DateField(verbose_name='开始日期', null=True)
    time = models.IntegerField(verbose_name='课时', default=0)
    maxnum = models.IntegerField(verbose_name='最大人数', default=20)
    number = models.IntegerField(verbose_name='当前人数', default=0)
    status = models.IntegerField(verbose_name='状态', default=1)


    class Meta:
        db_table = "exam_course"
        verbose_name = "考试课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 题目模型
class ExamQuestion(models.Model):
    type = models.CharField(verbose_name="题目类型",
                            choices=(('1', '单选'), ('2', '多选'), ('3', '填空'), ('4', '判断'), ('5', '主观')),
                            max_length=10)
    tid = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, db_column='tid')  # 出题人
    cid = models.ForeignKey('ExamCourse', to_field='id', on_delete=models.CASCADE, db_column='cid')  # 对应课程编号
    chapter = models.CharField(verbose_name="章", max_length=2)
    section = models.CharField(verbose_name="节", max_length=2)
    count = models.IntegerField(verbose_name="难度系数")

    class Meta:
        db_table = "exam_question"
        verbose_name = "考试题目"
        verbose_name_plural = verbose_name


# 单项选择题模型
class ExamSimple(models.Model):
    content = models.TextField(verbose_name="题干")
    choice1 = models.CharField(verbose_name="选项1", max_length=30)
    choice2 = models.CharField(verbose_name="选项2", max_length=30)
    choice3 = models.CharField(verbose_name="选项3", max_length=30)
    choice4 = models.CharField(verbose_name="选项4", max_length=30)
    answer = models.CharField(verbose_name="参考答案", max_length=1)
    qid = models.ForeignKey('ExamQuestion', to_field='id', on_delete=models.CASCADE, db_column='qid')  # 题目编号
    picture = models.ImageField(verbose_name="图片", upload_to="question/simple/", null=True, blank=True)

    class Meta:
        db_table = "exam_simple"
        verbose_name = "考试单项选择题"
        verbose_name_plural = verbose_name


# 多项选择题模型
class ExamMultiple(models.Model):
    content = models.TextField(verbose_name="题干")
    choice1 = models.CharField(verbose_name="选项1", max_length=30)
    choice2 = models.CharField(verbose_name="选项2", max_length=30)
    choice3 = models.CharField(verbose_name="选项3", max_length=30)
    choice4 = models.CharField(verbose_name="选项4", max_length=30)
    answer = ArrayField(models.CharField(max_length=10, blank=False), verbose_name="参考答案")
    qid = models.ForeignKey('ExamQuestion', to_field='id', on_delete=models.CASCADE, db_column='qid')  # 题目编号
    picture = models.ImageField(verbose_name="图片", upload_to="question/multiple/", null=True, blank=True)

    class Meta:
        db_table = "exam_multiple"
        verbose_name = "考试多项选择题"
        verbose_name_plural = verbose_name


# 填空题模型
class ExamBlank(models.Model):
    content = models.TextField(verbose_name="题干")
    answer = models.CharField(verbose_name="参考答案", max_length=10)
    qid = models.ForeignKey('ExamQuestion', to_field='id', on_delete=models.CASCADE, db_column='qid')  # 题目编号
    picture = models.ImageField(verbose_name="图片", upload_to="question/blank/", null=True, blank=True)

    class Meta:
        db_table = "exam_blank"
        verbose_name = "考试填空题"
        verbose_name_plural = verbose_name


# 判断题模型
class ExamJudge(models.Model):
    content = models.TextField(verbose_name="题干")
    answer = models.BooleanField(verbose_name="参考答案")
    qid = models.ForeignKey('ExamQuestion', to_field='id', on_delete=models.CASCADE, db_column='qid')  # 题目编号
    picture = models.ImageField(verbose_name="图片", upload_to="question/judge/", null=True, blank=True)

    class Meta:
        db_table = "exam_judge"
        verbose_name = "考试判断题"
        verbose_name_plural = verbose_name


# 主观题模型
class ExamSubjective(models.Model):
    content = models.TextField(verbose_name="题干")
    answer = models.TextField(verbose_name="参考答案")
    qid = models.ForeignKey('ExamQuestion', to_field='id', on_delete=models.CASCADE, db_column='qid')  # 题目编号
    picture = models.ImageField(verbose_name="图片", upload_to="question/subjective/", null=True, blank=True)

    class Meta:
        db_table = "exam_subjective"
        verbose_name = "考试主观题"
        verbose_name_plural = verbose_name


# 考试模型
class Exam(models.Model):
    tid = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, db_column='tid')  # 发布考试的教师编号
    cid = models.ForeignKey('ExamCourse', to_field='id', on_delete=models.CASCADE, db_column='cid')  # 相关课程编号
    name = models.CharField(verbose_name='考试名称', max_length=50, default='1')
    pid = models.ForeignKey('ExamPaper', to_field='id', on_delete=models.CASCADE, db_column='pid')  # 试卷编号
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='截止时间')
    status = models.CharField(verbose_name='考试状态', max_length=10, default='0',
                              choices=(('0', '未开始'), ('1', '进行中'), ('2', '已结束')))

    class Meta:
        db_table = "exam"
        verbose_name = "考试信息"
        verbose_name_plural = verbose_name


# 试卷模型
class ExamPaper(models.Model):
    name = models.CharField(verbose_name='标题', max_length=30)
    tid = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, db_column='tid')  # 出卷教师编号
    cid = models.ForeignKey('ExamCourse', to_field='id', on_delete=models.CASCADE, db_column='cid')  # 课程编号
    qidlist = ArrayField(models.CharField(max_length=10, blank=False), verbose_name="试题列表")

    class Meta:
        db_table = "exam_paper"
        verbose_name = "考试试卷信息"
        verbose_name_plural = verbose_name


# 学生选课模型
class StudentChooseCourse(models.Model):
    uid = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, db_column='uid')  # 学生编号
    cid = models.ForeignKey('ExamCourse', to_field='id', on_delete=models.CASCADE, db_column='cid')  # 课程编号
    status = models.IntegerField(verbose_name='选课状态', default=1)

    class Meta:
        db_table = "student_c_course"
        verbose_name = "考试学生选课"
        verbose_name_plural = verbose_name


# 学生答案模型
class ExamAnswer(models.Model):
    uid = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, db_column='uid')  # 学生编号
    eid = models.ForeignKey('Exam', to_field='id', on_delete=models.CASCADE, db_column='eid')  # 考试编号
    qid = models.ForeignKey('ExamQuestion', to_field='id', on_delete=models.CASCADE, db_column='qid')  # 题目编号
    answer = models.TextField(verbose_name='答案')
    score = models.IntegerField(verbose_name='得分', default=0)
    is_right = models.BooleanField(verbose_name='正确与否', null=True, blank=True)
    cloud = models.BooleanField(verbose_name='是否上传云笔记', default=False)
    update_time = models.DateField(verbose_name='云笔记上传时间', null=True, blank=True)
    is_read = models.BooleanField(verbose_name='是否被读取', default=False)

    class Meta:
        db_table = "exam_answer"
        verbose_name = "考试学生答案"
        verbose_name_plural = verbose_name


# 学生成绩模型
class ExamScore(models.Model):
    eid = models.ForeignKey('Exam', to_field='id', on_delete=models.CASCADE, db_column='eid')  # 考试编号
    uid = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, db_column='uid',
                            related_name='stu_score')  # 学生编号
    obj_score = models.IntegerField(verbose_name='客观题成绩', default=0)
    sub_score = models.IntegerField(verbose_name='主观题成绩', default=0)
    total_score = models.IntegerField(verbose_name='总成绩', default=0)

    class Meta:
        db_table = "exam_score"
        verbose_name = "考试学生成绩"
        verbose_name_plural = verbose_name


# 课程章节模型
class ExamSection(models.Model):
    cid = models.ForeignKey('ExamCourse', to_field='id', on_delete=models.CASCADE, db_column='cid')  # 课程编号
    chapter_count = models.IntegerField(verbose_name='章数')
    chapter = models.CharField(verbose_name='章名', max_length=30)
    section_count = models.IntegerField(verbose_name='节数')
    section = models.CharField(verbose_name='节名', max_length=30)

    class Meta:
        db_table = "exam_section"
        verbose_name = "考试课程章节"
        verbose_name_plural = verbose_name


# 教师题目上传云笔记
class ExamTeacherCloud(models.Model):
    tid = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, db_column='tid')  # 教师编号
    sid = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE, db_column='sid',
                            related_name='stu_id')  # 学生编号
    aid = models.ForeignKey('ExamQuestion', to_field='id', on_delete=models.CASCADE, db_column='aid')  # 题目编号
    cloud = models.BooleanField(verbose_name='是否上传云笔记', default=False)
    update_time = models.DateField(verbose_name='云笔记上传时间', null=True, blank=True)
    is_read = models.BooleanField(verbose_name='是否被读取', default=False)

    class Meta:
        db_table = "exam_teacher_cloud"
        verbose_name = "教师上传云笔记"
        verbose_name_plural = verbose_name


# 试卷题目分值模型
class ExamPaperScore(models.Model):
    pid = models.ForeignKey('ExamPaper', to_field='id', on_delete=models.CASCADE, db_column='pid')  # 试卷编号
    qid = models.ForeignKey('ExamQuestion', to_field='id', on_delete=models.CASCADE, db_column='qid')  # 题目编号
    score = models.IntegerField(verbose_name='题目分值')

    class Meta:
        db_table = "exam_paper_score"
        verbose_name = "试卷题目分值"
        verbose_name_plural = verbose_name


#########################################################33
# 云笔记
# 标签
class Tag(models.Model):
    tag_name = models.CharField(max_length=20)
    tag_create = models.DateTimeField(auto_now_add=True)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='creator_id')

    class Meta:
        db_table = "tb_tag"
        verbose_name = "云笔记标签"
        unique_together = ('tag_name', 'creator_id')

    def __str__(self):
        return self.tag_name


# 团队
class Team(models.Model):
    team_name = models.CharField(max_length=30)
    team_desc = models.TextField(null=True, blank=True)
    team_create = models.DateTimeField(auto_now_add=True)
    team_modify = models.DateTimeField(auto_now=True)
    modifier_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='modifier_id',
                                    related_name="modifier_team")
    leader_id = models.ForeignKey('User', on_delete=models.CASCADE, db_column='leader_id', related_name='leader_team')
    members = models.ManyToManyField(User, related_name='member_team')
    locked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='locked_by')

    class Meta:
        db_table = "tb_team"
        verbose_name = "云笔记团队"

    def __str__(self):
        return self.team_name


# 笔记
class Note(models.Model):
    note_title = models.CharField(max_length=30)
    note_text = models.TextField()
    note_type = models.CharField(max_length=10, default='markdown')
    note_create = models.DateTimeField(auto_now_add=True)
    note_modify = models.DateTimeField(auto_now=True)
    note_delete = models.DateTimeField(null=True, blank=True)
    writer_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='writer_id', related_name='creator_note')
    team_id = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, db_column='team_id',
                                related_name='notes')
    modifier_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='modifier_id',
                                    related_name='modifier_note')
    notebook_id = models.ForeignKey('NoteBook', on_delete=models.CASCADE, db_column='notebook_id',
                                    related_name="notebook_note")
    tags = models.ManyToManyField('Tag', through='NoteTag')
    locked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='locked_by')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除', help_text='逻辑删除')

    class Meta:
        db_table = "tb_note"
        verbose_name = "云笔记笔记"

    def __str__(self):
        return self.note_title + '-' + self.writer_id.username + '-' + self.note_type + '-' + self.notebook_id.notebook_name


# 标签笔记关联
class NoteTag(models.Model):
    note = models.ForeignKey('Note', on_delete=models.CASCADE, db_column='note')
    t = models.ForeignKey('Tag', on_delete=models.CASCADE, db_column='tag')

    class Meta:
        db_table = "note_tag_relationship"
        verbose_name = "云笔记标签笔记关联"
        unique_together = ('note', 't',)


# 笔记本
class NoteBook(models.Model):
    notebook_name = models.CharField(max_length=50)
    notebook_create = models.DateTimeField(auto_now_add=True)
    notebook_modify = models.DateTimeField(auto_now=True)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='creator_id',
                                   related_name='creator_notebook')
    team_id = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, db_column='team_id',
                                related_name='notebooks')
    modifier_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='modifier_id',
                                    related_name='modifier_notebook')
    locked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='locked_by')

    class Meta:
        db_table = "tb_notebook"
        verbose_name = "云笔记笔记本"

    def __str__(self):
        return self.notebook_name + '-' + self.creator_id.username

# 云笔记图片
class Image(models.Model):
    img = models.ImageField(upload_to ='img/',null=True,blank=True)
    class Meta:
        db_table = 'note_image'

###########################################################################
# 作业系统
# 课程表
class Course(models.Model):
    id = models.AutoField(verbose_name="课程编号", primary_key=True)
    name = models.CharField(verbose_name="课程名", max_length=30)
    # credit = models.FloatField(verbose_name="学分")
    number = models.IntegerField(verbose_name="选课人数", default=0)
    maxnum = models.IntegerField(verbose_name="最大人数", default=0)
    # tname = models.CharField(verbose_name="教师姓名", max_length=20)
    # type = models.CharField(verbose_name="课程类型", max_length=20, choices=(('MR','专业必修'),('ME','专业选修'),('PR','公共必修'),('PE','公共选修')), default='MR')
    # year = models.IntegerField(verbose_name="学年", default=2020)
    # semester = models.CharField(verbose_name="学期", max_length=20, choices=(('1','1'),('2','2')), default='1')
    tid = models.IntegerField(verbose_name="教师id")  # 任课教师
    stime = models.DateField(verbose_name='开始日期', null=True)
    time = models.IntegerField(verbose_name='课时', default=0)
    status = models.IntegerField(verbose_name='状态', default=1)

    class Meta:
        db_table = "course"
        verbose_name = "作业课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 学生课程关联表
class User_Course(models.Model):
    id = models.AutoField(verbose_name="流水号", primary_key=True)
    sname = models.CharField(verbose_name="学生用户名", max_length=150)
    cid = models.IntegerField(verbose_name="所属课程编号")

    class Meta:
        db_table = "user_course"
        verbose_name = "作业学生课程关联"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cid


# 作业表
class Work(models.Model):
    id = models.AutoField(verbose_name="流水号", primary_key=True)
    cid = models.IntegerField(verbose_name="所属课程编号")
    ctime = models.IntegerField(verbose_name="作业次数")
    chapter = models.IntegerField(verbose_name="所属章节")
    deadline = models.DateTimeField(verbose_name="截止时间", auto_now_add=True)
    release = models.BooleanField(verbose_name="是否发布", default=False)
    finishnum = models.IntegerField(verbose_name="已完成人数", default=0)
    qnum = models.IntegerField(verbose_name="包含题目数", default=0)

    class Meta:
        db_table = "work"
        verbose_name = "作业"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 单项选择题表
class Simple(models.Model):
    id = models.AutoField(verbose_name="流水号", primary_key=True)
    content = models.TextField(verbose_name="题干")
    choice1 = models.CharField(verbose_name="选项1", max_length=100)
    choice2 = models.CharField(verbose_name="选项2", max_length=100)
    choice3 = models.CharField(verbose_name="选项3", max_length=100)
    choice4 = models.CharField(verbose_name="选项4", max_length=100)
    answer = models.CharField(verbose_name="答案", max_length=1, default='A')
    wid = models.IntegerField(verbose_name="作业编号")
    picture = models.ImageField(upload_to="questionpic/", null=True, blank=True, verbose_name="题目图片")
    explain = models.TextField(verbose_name="解释", null=True, blank=True)

    class Meta:
        db_table = "simple"
        verbose_name = "作业单选"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 多项选择题表
class Multiple(models.Model):
    id = models.AutoField(verbose_name="流水号", primary_key=True)
    content = models.TextField(verbose_name="题干")
    choice1 = models.CharField(verbose_name="选项1", max_length=100)
    choice2 = models.CharField(verbose_name="选项2", max_length=100)
    choice3 = models.CharField(verbose_name="选项3", max_length=100)
    choice4 = models.CharField(verbose_name="选项4", max_length=100)
    answer = models.CharField(verbose_name="答案1", max_length=4, default='A')
    wid = models.IntegerField(verbose_name="作业编号")
    picture = models.ImageField(upload_to="questionpic/", null=True, blank=True, verbose_name="题目图片")
    explain = models.TextField(verbose_name="解释", null=True, blank=True)

    class Meta:
        db_table = "mutiple"
        verbose_name = "作业多选"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 主观题表
class Subjective(models.Model):
    id = models.AutoField(verbose_name="流水号", primary_key=True)
    content = models.TextField(verbose_name="题干")
    answer = models.TextField(verbose_name="答案", null=True, blank=True)
    wid = models.IntegerField(verbose_name="作业编号")
    picture = models.ImageField(upload_to="questionpic/", null=True, blank=True, verbose_name="题目图片")
    explain = models.TextField(verbose_name="解释", null=True, blank=True)

    class Meta:
        db_table = "subjective"
        verbose_name = "作业主观题"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 填空题表
class Blank(models.Model):
    id = models.AutoField(verbose_name="流水号", primary_key=True)
    content = models.TextField(verbose_name="题干")
    answer = models.CharField(verbose_name="答案", max_length=100, null=True, blank=True)
    wid = models.IntegerField(verbose_name="作业编号")
    picture = models.ImageField(upload_to="questionpic/", null=True, blank=True, verbose_name="题目图片")
    explain = models.TextField(verbose_name="解释", null=True, blank=True)

    class Meta:
        db_table = "blank"
        verbose_name = "作业填空"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 判断题表
class Judge(models.Model):
    id = models.AutoField(verbose_name="流水号", primary_key=True)
    content = models.TextField(verbose_name="题干")
    answer = models.BooleanField(verbose_name="答案", default=False)
    wid = models.IntegerField(verbose_name="作业编号")
    picture = models.ImageField(upload_to="questionpic/", null=True, blank=True, verbose_name="题目图片")
    explain = models.TextField(verbose_name="解释", null=True, blank=True)

    class Meta:
        db_table = "judge"
        verbose_name = "作业判断"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 学生作业关联表
class User_Work(models.Model):
    id = models.AutoField(verbose_name="流水号", primary_key=True)
    wid = models.IntegerField(verbose_name="作业编号")
    sid = models.IntegerField(verbose_name="学生编号")
    update = models.DateTimeField(verbose_name="上传时间", auto_now=True)
    file = models.FileField(upload_to="work/", null=True, blank=True, verbose_name="作业")
    comment = models.TextField(verbose_name="评语", null=True, blank=True)
    score = models.IntegerField(verbose_name="评分", default=0)
    good = models.BooleanField(verbose_name="是否优秀作业", default=False)
    finish = models.BooleanField(verbose_name="是否完成", default=False)
    ifscore = models.BooleanField(verbose_name="是否已评分", default=False)

    class Meta:
        db_table = "user_work"
        verbose_name = "学生作业"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 学生题目关联表
class User_Question(models.Model):
    id = models.AutoField(verbose_name="流水号", primary_key=True)
    sid = models.IntegerField(verbose_name="学生编号")
    wid = models.IntegerField(verbose_name="作业编号", default=0)
    qid = models.IntegerField(verbose_name="题目编号", default=0)
    number = models.IntegerField(verbose_name="作业内序号", default=0)
    answer = models.TextField(verbose_name="学生答案", blank=True, null=True)
    ischeck = models.BooleanField(verbose_name="是否已经批改", default=False)
    judge = models.BooleanField(verbose_name="正误", default=False)
    cloud = models.BooleanField(verbose_name="上传云笔记", default=False)
    type = models.CharField(verbose_name="题目类型", max_length=1,
                            choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')))
    upload_time = models.DateField(verbose_name="上传时间", null=True, blank=True)
    is_read = models.BooleanField(verbose_name="是否被读取", default=False)

    class Meta:
        db_table = "user_question"
        verbose_name = "作业学生题目"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 作业题目关联表
class Work_Question(models.Model):
    id = models.AutoField(verbose_name="流水号", primary_key=True)
    wid = models.IntegerField(verbose_name="作业编号")
    qid = models.IntegerField(verbose_name="题目编号")
    number = models.IntegerField(verbose_name="作业内序号", default=0)
    type = models.CharField(verbose_name="题目类型", max_length=1,
                            choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')))

    class Meta:
        db_table = "work_question"
        verbose_name = "作业题目"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 共享区表
class SharedArea(models.Model):
    id = models.AutoField(verbose_name="流水号", primary_key=True)
    cid = models.IntegerField(verbose_name="所属课程编号")
    admin_id = models.IntegerField(verbose_name="管理员id", blank=True, null=True)

    class Meta:
        db_table = "sharedarea"
        verbose_name = "作业共享区"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 共享区资料表
class Share_File(models.Model):
    id = models.AutoField(verbose_name="流水号", primary_key=True)
    data_name = models.CharField(verbose_name="资料名", max_length=30)
    data_file = models.FileField(upload_to="Share/", verbose_name="资料")
    upload_id = models.IntegerField(verbose_name="上传者id")
    update_time = models.DateTimeField(verbose_name="上传时间", null=True, blank=True)
    aid = models.IntegerField(verbose_name="所属共享区编号", default=0)

    class Meta:
        db_table = "share_file"
        verbose_name = "作业共享资料"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 消息表
class Work_Message(models.Model):
    id = models.AutoField(verbose_name="流水号", primary_key=True)
    tid = models.IntegerField(verbose_name="发送人id")
    sid = models.IntegerField(verbose_name="接收人id")
    tittle = models.TextField(verbose_name="消息标题")
    message = models.TextField(verbose_name="消息")
    read = models.BooleanField(verbose_name="已读", default=False)

    class Meta:
        db_table = "work_message"
        verbose_name = "作业消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 优秀题解表
class GoodWork(models.Model):
    id = models.AutoField(verbose_name="流水号", primary_key=True)
    wid = models.IntegerField(verbose_name="作业编号")
    cid = models.IntegerField(verbose_name="课程编号")
    qid = models.IntegerField(verbose_name="主观题目编号")
    tid = models.IntegerField(verbose_name="教师id")
    sid = models.IntegerField(verbose_name="学生id")
    answer = models.TextField(verbose_name="学生解答")
    upload_time = models.DateField(verbose_name="上传时间", null=True, blank=True)
    is_read = models.BooleanField(verbose_name="是否被读取", default=False)

    class Meta:
        db_table = "goodwork"
        verbose_name = "优秀作业"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


class Apply_Class(models.Model):
    tid = models.ForeignKey(User, verbose_name="教师id", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="课程名", max_length=30)
    stime = models.DateField(verbose_name='开始日期', null=True)
    time = models.IntegerField(verbose_name='课时', default=0)
    maxnum = models.IntegerField(verbose_name='最大人数', default=20)
    reason = models.TextField(verbose_name='申请理由')
    status = models.IntegerField(verbose_name='状态', default=1)

    class Meta:
        db_table = "apply_class"
        verbose_name = "开课申请"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Operate_Class(models.Model):
    user_id = models.ForeignKey(User, verbose_name="学生id", on_delete=models.CASCADE)
    class_id = models.ForeignKey(ExamCourse, verbose_name="课程id", on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=(('J', '加入'), ('O', '退出')),
                            verbose_name="申请类型")
    time = models.DateTimeField(verbose_name='申请时间')
    etime = models.DateTimeField(verbose_name='处理时间',null=True)
    status = models.IntegerField(verbose_name='状态', default=1)

    class Meta:
        db_table = "operate_class"
        verbose_name = "课程操作"
        verbose_name_plural = verbose_name