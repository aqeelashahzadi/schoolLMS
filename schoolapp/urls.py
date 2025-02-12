from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name='homen'),
    path('class/',views.classes,name='classn'),
    path('contact/',views.contact,name='contactn'),
    path('courses/',views.courses,name='coursesn'),
    path('login_logic/',views.login_logic,name='login_n'),
    path('logout_logic/',views.logout_logic,name='logoutn'),
    path('mycourses/',views.mycourses,name='mycoursesn'),
    path('payment/',views.payment,name='paymentn'),
    path('register/',views.register,name='registern'),
    path('results/',views.result,name='resultsn'),
    path('student_teacher/',views.student_teacher,name='student-teachern'),
    path('subject/',views.subject,name='subjectn'),
    path('teacherhome/',views.teacherhome,name='teacherhomen'),
    path('teacherclas/',views.teacherclasses,name='teacherclassn'),
    path('handlerequest/',views.handlederequest,name='handlerequestn'),
    #API to post a comment
    path('postcomment/',views.postcomment,name='postcomment'),
]
