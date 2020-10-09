from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from exam import views

urlpatterns = [
    url(r'selectquestion', views.selectQuestion),
    path('getavatar', views.getAvatar),  # 查询用户头像 deprecated
    path('findcourse', views.findCourse),  # 教师课程列表查询 no need to change
    path('addquestion', views.addQuestion),  # 教师试题添加 done(not checked)
    path('selectquestion', views.selectQuestion),  # 教师查询试题列表 no need to change
    path('findquestion', views.findQuestion),  # 教师查看试题信息 no need to change
    path('changequestion', views.changeQuestion),  # 教师修改试题信息  done
    path('choosequestion', views.chooseQuestion),  # 教师手动组卷选择试题 no need to change
    path('addPaper', views.addPaper),  # 教师试卷添加 done
    path('findpaper', views.findPaper),  # 教师试卷名称列表查询 no need to change
    path('getpaper', views.findPaper),  # 教师试卷信息查询 duplicated
    path('addexam', views.addExam),  # 教师考试发布 done
    path('selectexam', views.selectExam),  # 学生考试信息查询 no need to change
    path('selectpaper', views.selectPaper),  # 学生试卷查询 no need to change
    path('changeexam', views.changeExam),  # 教师修改考试 done
    path('getquestion', views.getQuestion),  # 获取题目具体信息 no need to change
    path('updateanswer', views.updateAnswer),  # 学生答案更新 done
    path('checkanswer', views.checkAnswer),  # 自动批改客观题 done
    path('findexam', views.findExam),  # 教师查询考试信息 no need to change
    path('getscore', views.getScore),  # 教师客观题成绩查询 no need to change
    path('addscore', views.addScore),  # 教师主观题成绩添加 done
    path('addallscore', views.addAllScore),  # 教师总成绩添加 done
    path('getanswer', views.getAnswer),  # 教师查询学生主观题答案 no need to change
    path('teachercloud', views.teacherCloud),  # 教师上传学生答案至云笔记 done
    path('gettotalscore', views.getTotalScore),  # 教师查询学生成绩 no need to change
    path('addcourse', views.addCourse),  # 教师课程添加 done
    path('addscc', views.addSCC),  # 学生选课添加 done
    path('addsection', views.addSection),  # 教师课程章节添加 done
    path('showscore', views.showScore),  # 教师成绩可视化查询 no need
    path('showquestion', views.showQuestion),  # 教师题目错误率可视化查询 no need
    path('showstudentscore', views.showStudentScore),  # 学生成绩可视化查询 no need
    path('getstudentscore', views.getStudentScore),  # 学生成绩查询 no need
    path('findstuexam', views.findStuExam),  # 学生考试名列表查询 no need
    path('getwrong', views.getWrong),  # 学生错题查询 no need
    path('gotocloud', views.goToCloud),  # 错题上传云笔记 done
    path('getsection', views.getSection),  # 自动组卷课程章节列表查询 no need
    path('autopaper', views.autoPaper),  # 自动组卷
    path('findchapter', views.findChapter),  # 课程章查询 no need
    path('findsection', views.findSection),  # 课程节查询 no need
    path('getstucourse', views.getStuCourse),  # 学生课程查询 no need
    path('addtest', views.addTest),  # 学生测验添加
    path('uploaddocx', views.analyseDocx),  # word文件添加试题
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
