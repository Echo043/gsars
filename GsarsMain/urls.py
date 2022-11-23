from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginaction, name="login"),
    path('about/',views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('Admin/',views.admindashboard, name="admin"),
    path('Admin/addstu',views.signupaction, name="signup"),
    path('Admin/bulkupload', views.upload, name='bulk'),
    path('Admin/addfocal', views.addfocal, name="addfocal"),
    path('Admin/participants',views.participants, name="participants"),
    path('Admin/fparticipants',views.f_participants, name="focalp"),
    path('Admin/view', views.view_records, name='view'),
    path('focal/',views.focaldashboard, name="focal"),
    path('focal/createactivity/',views.createActivity,name='createactivity'),
    path('focal/activity/',views.activities, name='activity'),
    path('focal/requests/', views.frequest, name='frequests'),
    path('student/', views.s_dashboard, name="student" ),
    path('student/addrecord/',views.add_records,name="addrecord"),
    path('student/request/',views.requests,name="request"),
    path('focal/view',views.focal_view_records, name="fview"),
    path('student/achievement', views.achievements, name="achievements"),
    path('logout/', views.logout,name="logout"),
    path('approve/', views.button, name="approve"),
    path('delete/',views.deleteButton,name='delete'),
    path('bulk_delete/', views.bulk_delete, name='bulkdelete'),
    path('profile', views.profile, name="profile"),
    path('update', views.updateProfile, name="update"),
    path('fprofile', views.fprofile, name="fprofile"),
    path('updatefocal', views.updateProfile_focal, name="update_focal"),
    path('password_reset/',views.forgot, name='password_reset'),
    path('password_reset_form/', views.forgotform, name='password_reset_form'),
    path('programme/', views.addprogramme, name='programme')
    
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)