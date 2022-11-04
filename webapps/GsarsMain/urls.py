from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('Admin/',views.admindashboard, name="admin"),
    path('Admin/addstu',views.signupaction, name="signup"),
    path('Admin/addfocal', views.addfocal, name="addfocal"),
    path('participants',views.participants, name="participants"),
    path('fparticipants',views.f_participants, name="focalp"),
    path('focal/',views.focaldashboard),
    path('createactivity/',views.createActivity,),
    path('activity/',views.activities),
    path('student/', views.s_dashboard),
    path('addrecord',views.add_records,),
    path('logout/', views.logout_view,name="logout")

]