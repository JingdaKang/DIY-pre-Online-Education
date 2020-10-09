from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'GetCourse$',views.GetCourse,),#check
    url(r'GetMyCourse$',views.GetMyCourse,),#check
    url(r'GetTeacherCourse$',views.GetTeacherCourse,),#check
    url(r'EditWork$',views.EditWork,),#done(not checked)
    url(r'GetWorkTime$',views.GetWorkTime,),#check
    url(r'GetMyWork$',views.GetMyWork,),#check
    url(r'GetTeacherWork$',views.GetTeacherWork,),# done(insertion not checked)
    url(r'CreateQuestion$',views.CreateQuestion,),# done(not checked)
    url(r'UploadAvatar$',views.UploadAvatar,),#deprecated
    url(r'GetMyAvatar$',views.GetMyAvatar,),#deprecated
    url(r'Comment$',views.Comment,),#checked
    url(r'GetQuestionNumber$',views.GetQuestionNumber,),#checked
    url(r'GetQuestion$',views.GetQuestion,),#done
    url(r'UpdateAnswer$',views.UpdateAnswer,),#done
    url(r'CheckAnswer$',views.CheckAnswer,),#done
    url(r'GetWrongQuestion$',views.GetWrongQuestion,),#done
    url(r'UploadFile$',views.UploadFile,),#done
    url(r'GetStudentQuestion$',views.GetStudentQuestion,),#done
    url(r'UpdateResult$',views.UpdateResult,),#done
    url(r'GetC$',views.GetC,),#done
    url(r'UpTo$',views.UpTo,),#done
    url(r'AddCourse$',views.AddCourse,),#done
    url(r'Recommend$',views.Recommend,),
    url(r'GetGood$',views.GetGood,),#done
    url(r'UploadMaterial$',views.UploadMaterial,),#done
    url(r'ShareArea$',views.ShareArea,),#done
    url(r'GetMaterial$',views.GetMaterial,),
    url(r'GetAnyWork$',views.GetAnyWork,),
    url(r'Message$',views.Message,),
    url(r'GetInfo$',views.GetInfo,),
]
