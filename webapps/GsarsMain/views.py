from django.shortcuts import render,redirect
import mysql.connector as sql
from django.contrib import messages
from django.contrib.auth import logout


# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")


def contact(request):
    return render(request,"contact.html")

def admindashboard(request):
    m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
    cursor = m.cursor()
    c=" select count(*) Count from students union all select count(*) from focal;"
    cursor.execute(c)
    count=cursor.fetchall()
    cursor.execute(c)
    count1=cursor.fetchall()
    count2=count[0][0]+count1[1][0]
    return render(request, 'admin/a_dashboard.html', {"count":count, "count1":count1, 'count2':count2})


sid = ""
fn = ""
mn = ""
ln = ""
em = ""
pwd = ""
prg = ""
year = ""
sem = ""
role = ""

# Create your views here.
def signupaction(request):
    global sid,fn,mn,ln,em,pwd,prg,year,sem,role
    if request.method == "POST":
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        d=request.POST
        role = "Student"
        for key,value in d.items():
            if key=="sid":
                sid=value
            if key=="f_name":
                fn = value
            if key=="m_name":
                mn = value
            if key=="l_name":
                ln = value
            if key=="email":
                em=value
            if key=="password":
                pwd=value
            if key=="programme":
                prg=value
            if key=="year":
                year=value
            if key=="semester":
                sem=value
        c = "insert into students(SID,F_name,M_name,L_name,Email,Password,Programme,Year,Semester,role) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(sid,fn,mn,ln,em,pwd,prg,year,sem,role)
        cursor.execute(c)
        m.commit() 
        messages.success(request, "User added successfully")
    return render(request, 'admin/addstu.html')

firstname = ''
middlename = ''
lastname = ''
f_email = ''
f_password = ''
designation = ""

def addfocal(request):
    global fn,mn,ln,em,pwd,designation
    if request.method == "POST":
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        d=request.POST  
        for key,value in d.items():
            if key=="firstname":
                fn = value
            if key=="middlename":
                mn = value
            if key=="lastname":
                ln = value
            if key=="f_email":
                em=value
            if key=="f_password":
                pwd=value
            if key=="designation":
                designation=value
            role = "Focal"
        c = "insert into focal(f_name,m_name,l_name,email,password,designation,role) values('{}','{}','{}','{}','{}','{}','{}')".format(fn,mn,ln,em,pwd,designation,role)
        cursor.execute(c)
        m.commit()   
    return render(request,'admin/addfocal.html')


def participants(request):
    m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
    cursor = m.cursor()
    c="select F_name,M_name,L_name,Email,role from students;"
    cursor.execute(c)
    table = cursor.fetchall()
    return render(request, 'admin/participants.html', {'records':table})


def f_participants(request):
    m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
    cursor = m.cursor()
    c="select f_name,m_name,l_name,email,designation from focal;"
    cursor.execute(c)
    table = cursor.fetchall()
    return render(request, 'admin/f_participants.html', {'records':table})

# Focal person 
def focaldashboard(request):
    return render(request,'focal/f_dashboard.html')


an = ''
catergory = ''
year = ''
semester = ''
date= ''

def createActivity(request):
    global an,catergory,year,semester,date
    if request.method == "POST":
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        d=request.POST  
        for key,value in d.items():
            if key=="activity":
                an = value
            if key=="category":
                category = value
            if key=="year":
                year = value
            if key=="semester":
                semester=value
            if key=="date":
                date=value
        c = "insert into activity(A_name,Category,Year,Semester,Date) values('{}','{}','{}','{}','{}')".format(an,category,year,semester,date)
        cursor.execute(c)
        m.commit()   
    return render(request, 'focal/create activities.html')

def activities(request):
    m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
    cursor = m.cursor()
    c="select A_name,Category,Year,Semester,Date from activity;"
    cursor.execute(c)
    table = cursor.fetchall()
    return render(request, 'focal/activity.html', {'records':table})

def add_records(request):
    return render(request,"student/add_records.html")



# Student
def s_dashboard(request):
    return render(request, "student/student_dashboard.html")
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')


   
