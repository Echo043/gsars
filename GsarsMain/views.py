from django.shortcuts import render,redirect,reverse
import mysql.connector as sql
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from webapps import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from .models import Students
from .resources import PersonResource
from tablib import Dataset




# Create your views here.
em = ''
pwd = ''
role = ''

# Create your views here.

def loginaction(request):
    global em, pwd, role
    if request.method=="POST":
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        d=request.POST
        table = ""   
        for key,value in d.items():
            if key=="email":
                em=value
            if key=="password":
                pwd=value   
            if key=="role":
                role=value
                if role == "Admin":
                    table="admin"
                if role == "Student":
                    table="students"
                if role == "Focal Person":
                    table = "focal"

        c="select role from {} where email='{}' and password='{}'".format(table,em,pwd)
        cursor.execute(c)
        t=tuple(cursor.fetchall())
        if t==():
            messages.error(request, "Invalid Credentials")
        else:
            if role=="Admin":
                m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
                cursor = m.cursor()
                c="select Sl_no from admin;"
                cursor.execute(c)
                t=tuple(cursor.fetchall())
                adminID = t[0][0]
                request.session['admin'] = adminID
                print(adminID)
                return redirect('admin')
                
            if role=="Student":  
                m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
                cursor = m.cursor()
                d=request.POST
                c ="select SID,f_name,m_name,l_name from students where email='{}' and password='{}';".format(em,pwd)
                cursor.execute(c)
                t=tuple(cursor.fetchall())
                name = t[0][1] + " " + " " + t[0][3]
                sid = t[0][0]
                request.session['name'] = name
                request.session['sid'] = sid   
                request.session['studentemail'] = em
                return redirect('student')

            if role=="Focal Person":
                m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
                cursor = m.cursor()
                d=request.POST
                c ="select FID,f_name,m_name,l_name from focal where email='{}' and password='{}';".format(em,pwd)
                cursor.execute(c)
                t=tuple(cursor.fetchall()) 
                FID = t[0][0]
                name = t[0][1] + " " + t[0][2] + " " + t[0][3]
                request.session['FID'] = FID
                request.session['fname'] = name
                request.session['email'] = em
                return redirect('focal')
    return render(request, 'login.html')




def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def admindashboard(request):
    if 'admin' in request.session:
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        c=" select count(*) Count from students union all select count(*) from focal;"
        cursor.execute(c)
        count=cursor.fetchall()
        cursor.execute(c)
        count1=cursor.fetchall()
        count2=count[0][0]+count1[1][0]
        cursor.execute("select count(*) from students where Programme='Bsc. Computer Science'")
        programme = cursor.fetchall()
        cursor.execute("select count(*) from students where Programme='AI'")
        AI = cursor.fetchall()
        cursor.execute("select count(*) from students where Programme='Bsc. IT'")
        IT = cursor.fetchall()
        cursor.execute("select count(*) from students where Programme='BlockChain'")
        blockchain = cursor.fetchall()
        cursor.execute("select count(*) from students where Programme='Digital Media'")
        digital = cursor.fetchall()

        major = [programme[0],IT[0],AI[0],blockchain[0],digital[0]]
        
        context={
            'count':count,
            'count1':count1,
            'count2':count2,
            'major':major
        }
        return render(request, 'admin/a_dashboard.html', context)
    else:
        return render(request, 'login.html')

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
file = ""

# Create your views here.

def addprogramme(request):
    if request.method == "POST":
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="programmeadd":
                cursor.execute("insert into programme values('{}')".format(value))
                m.commit() 
    return redirect('signup')
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def signupaction(request):
    if 'admin' in request.session:
       
        p = ''
        global sid,fn,mn,ln,em,pwd,prg,year,sem,role,file
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
                
            try:
                c = "insert into students(SID,F_name,M_name,L_name,Email,Password,Programme,Year,Semester,role) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(sid,fn,mn,ln,em,pwd,prg,year,sem,role)
                cursor.execute(c)
                m.commit() 
                messages.success(request, "User added successfully")
            except sql.Error as e:
                messages.error(request, "Error occured while adding user")



            

            # Welcome email
            subject = "welcome to GSARS!!!"
            message = "Hello" + fn + mn + ln + "!!\n" + "Welcome to GSARS \n We have sent you a confirmation email \n Please login to your account using your email and password:"+ pwd
            from_email = settings.EMAIL_HOST_USER
            to_list = [em]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        cursor.execute("select distinct(pname) from programme")
        p = cursor.fetchall()
        return render(request,'admin/addstu.html', {"p":p})
    else:
        return redirect('login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def upload(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            person_resource = PersonResource()
            dataset = Dataset()
            new_person = request.FILES['myfile']

            if not new_person.name.endswith('xlsx'):
                messages.info(request, 'Wrong Format')
                return render(request, 'admin/addstu.html')

            imported_data = dataset.load(new_person.read(),format='xlsx')
            for data in imported_data:
                value = Students(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    data[7],
                    data[8],
                    data[9]

                )
                value.save()
            m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
            cursor = m.cursor()
            cursor.execute("insert into students select * from gsarsmain_students;")
            m.commit()

            cursor.execute("select Email,Password from students;")
            emails = cursor.fetchall()
            for email in emails:
                subject = "welcome to GSARS!!!"
                message = "Hello" + fn + mn + ln + "!!\n" + "Welcome to GSARS \n We have sent you a confirmation email \n Please login to your account using your email and password:"+ email[1]
                from_email = settings.EMAIL_HOST_USER
                to_list = [email[0]]
                send_mail(subject, message, from_email, to_list, fail_silently=True)
            try:
                messages.success(request,"Successfully added")
                cursor.execute("delete from gsarsmain_students;")
                m.commit()
            except sql.Error as e:
                 messages.error(request,"Error Occured while adding")

            
        return render(request, 'admin/addstu.html', {'emails':emails})
    else:
        return redirect('login')
        

firstname = ''
middlename = ''
lastname = ''
f_email = ''
f_password = ''
designation = ""

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def addfocal(request):
    if 'admin' in request.session:
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
            
            # Welcome email
            subject = "welcome to GSARS!!!"
            message = "Hello" + fn + mn + ln + "!!\n" + "Welcome to GSARS \n We have sent you a confirmation email \n Please login to your account using your email and password:"+ pwd
            from_email = settings.EMAIL_HOST_USER
            to_list = [em]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
        return render(request,'admin/addfocal.html')
    else:
        return redirect('login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def participants(request):
    if 'admin' in request.session:
        programme=''
        year=''
        table=''
        p=''
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        if request.method == "POST":
            d = request.POST
            for key,value in d.items():
                if key=="all":
                    c="select SID,F_name,M_name,L_name,Email from students"
                    cursor.execute(c)
                    table = cursor.fetchall() 
                    return render(request, 'admin/participants.html', {'records':table})
                if key=="programme":
                    programme=value
                if key=="year":
                    year=value
                try:
                    c="select SID,F_name,M_name,L_name,Email from students where Programme='{}' and Year={};".format(programme,year)
                    cursor.execute(c)
                    table=cursor.fetchall()  
                    return render(request, 'admin/participants.html', {'records':table})
                except sql.Error as e:
                    return render(request, 'admin/participants.html', {'records':table})
                   
           
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        c="select SID,F_name,M_name,L_name,Email from students"
        cursor.execute(c)
        table = cursor.fetchall() 
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        cursor.execute("select distinct(pname) from programme")
        p = cursor.fetchall()
        return render(request, 'admin/participants.html', {'records':table, 'p':p})
    else:
        return redirect('login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def f_participants(request):
    if 'admin' in request.session:
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        c="select FID,f_name,m_name,l_name,email,designation from focal;"
        cursor.execute(c)
        table = cursor.fetchall()
        return render(request, 'admin/f_participants.html', {'records':table})
    else:
        return redirect('login')
    
######View Records#######
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def view_records(request):
     if 'admin' in request.session:
        programme = ''
        year=''
        category = ''
        semester = ''
        achieve = ''
        p='p'
        A = ''
        Y = ''
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        if request.method == "POST":
            d=request.POST
            for key,value in d.items():
                if key == 'all':
                    cursor.execute("select students.SID,students.F_name,students.M_name,students.L_name,students.Email,activity.A_name from students, activity, record where activity.AID = record.AID and students.SID=record.SID;")
                    achieve = cursor.fetchall()
                    return render(request,'admin/view_records.html',{'achieve':achieve})
                if key == 'category':
                    category=value
                if key=='programme':
                    programme = value
                if key=='year':
                    year = value
                if key == 'semester':
                    semester= value   
            cursor.execute("select students.SID,students.F_name,students.M_name,students.L_name,students.Email,activity.A_name from students, activity, record where activity.AID = record.AID and students.SID=record.SID and students.Programme='{}' and activity.Year={} and activity.Category='{}' and activity.Semester='{}';".format(programme,year,category,semester))
            achieve = cursor.fetchall()
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        cursor.execute("select distinct(pname) from programme")
        p = cursor.fetchall()

        cursor.execute("select distinct(A_name) from activity")
        A = cursor.fetchall()

        cursor.execute("select distinct(Year) from activity")
        Y = cursor.fetchall()



        return render(request, 'admin/view_records.html',{'achieve':achieve, 'programme':programme,'category':category, 'year':year,'semester':semester, 'p':p, 'A':A, 'Y':Y})
     else:
         return redirect('login')

# Focal person 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def focaldashboard(request):
    if 'FID' in request.session and 'fname' in request.session:
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        c=" select count(*) from activity;"
        cursor.execute(c)
        count=cursor.fetchall()
        cursor.execute("select count(record.SID) from record,students where students.SID=record.SID and students.Year=1;")
        year1 = tuple(cursor.fetchall())
        cursor.execute("select count(record.SID) from record,students where students.SID=record.SID and students.Year=2;")
        year2 = tuple(cursor.fetchall())
        cursor.execute("select count(record.SID) from record,students where students.SID=record.SID and students.Year=3;")
        year3 = tuple(cursor.fetchall())
        cursor.execute("select count(record.SID) from record,students where students.SID=record.SID and students.Year=4;")
        year4 = tuple(cursor.fetchall())
        year = [year1[0][0],year2[0][0],year3[0][0],year4[0][0]]
        context = {
            "count":count[0][0],
            'year':year,
        }
        return render(request,'focal/f_dashboard.html',context)
    else:
        return redirect('login')


an = ''
catergory = ''
year = ''
semester = ''
date= ''
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createActivity(request):
    if 'FID' in request.session and 'fname' in request.session:
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
                    semester = value
                if key=="date":
                    date=value
            c = "insert into activity(A_name,Category,Year,Semester,Date) values('{}','{}','{}','{}','{}')".format(an,category,year,semester,date)
            cursor.execute(c)
            m.commit() 
        try:  
            messages.success(request, "Successfully created")
        except sql.Error as e:
            messages.error(request, "Error Occured")

        return render(request, 'focal/create activities.html')
    else:
        return redirect('login')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def activities(request):
    if 'FID' in request.session and 'fname' in request.session:
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        c="select AID,A_name,Category,Year,Semester,Date from activity;"
        cursor.execute(c)
        table = cursor.fetchall()
        if request.method == "POST":
            d = request.POST
            id =''
            aname = ''
            category = ''
            year = ''
            semester =''
            date = ''
            for key,value in d.items():
                if key=='aid':
                    id = value
                if key == 'aname':
                    aname = value
                    if aname == '':
                        pass
                    else:
                        cursor.execute("update activity set A_name='{}' where AID={}".format(aname,id))
                        m.commit()
                if key == 'category':
                    category = value
                    if category == '':
                        pass
                    else:
                        cursor.execute("update activity set Category='{}' where AID={}".format(category,id))
                        m.commit()
                    
                if key == 'year':
                    year = value
                    if year == '':
                        pass
                    else:
                        cursor.execute("update activity set Year='{}' where AID={}".format(year,id))
                        m.commit()
                if key == 'semester':
                    semester = value
                    if semester == '':
                        pass
                    else:
                        cursor.execute("update activity set Semester='{}' where AID={}".format(semester,id))
                        m.commit()
                if key == 'date':
                    date = value  
                    if date == '':
                        pass
                    else:
                        cursor.execute("update activity set Date='{}' where AID={}".format(date,id))
                        m.commit()
            
            return redirect('activity')
                    
        return render(request, 'focal/activity.html', {'records':table})
    else:
        return redirect('login')

        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def frequest(request):
    if 'FID' in request.session and 'fname' in request.session:
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        c="select students.SID,activity.A_name, activity.Category, activity.Year,activity.Semester, record.RID from activity join record on activity.AID = record.AID join students on students.SID=record.SID;"
        cursor.execute(c)
        table = cursor.fetchall()
        return render(request,'focal/requests.html', {"requests":table[::-1]})
    else:
        return redirect('login')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def focal_view_records(request):
     if 'FID' in request.session and 'fname' in request.session:
        programme = ''
        year=''
        category = ''
        semester = ''
        achieve = ''
        p = ''
        A = ''
        Y = ''
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        if request.method == "POST":
            d=request.POST
            for key,value in d.items():
                if key == 'all':
                    cursor.execute("select students.SID,students.F_name,students.M_name,students.L_name,students.Email,activity.A_name from students, activity, record where activity.AID = record.AID and students.SID=record.SID;")
                    achieve = cursor.fetchall()
                    return render(request,'focal/view_records.html',{'achieve':achieve})
                if key == 'category':
                    category=value
                if key=='programme':
                    programme = value
                if key=='year':
                    year = value
                if key == 'semester':
                    semester= value   
            cursor.execute("select students.SID,students.F_name,students.M_name,students.L_name,students.Email,activity.A_name from students, activity, record where activity.AID = record.AID and students.SID=record.SID and students.Programme='{}' and activity.Year={} and activity.Category='{}' and activity.Semester='{}';".format(programme,year,category,semester))
            achieve = cursor.fetchall()
        cursor.execute("select distinct(pname) from programme")
        p = cursor.fetchall()

        cursor.execute("select distinct(A_name) from activity")
        A = cursor.fetchall()

        cursor.execute("select distinct(Year) from activity")
        Y = cursor.fetchall()
        return render(request, 'focal/view_records.html',{'achieve':achieve, 'programme':programme,'category':category, 'year':year,'semester':semester, 'p':p, 'A':A, 'Y':Y})
     else:
         return redirect('login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def fprofile(request):
    if 'FID' in request.session and 'fname' in request.session:
        name = request.session.get('fname')
        email = request.session.get('email')
        return render(request, 'focal/profile.html', {'fname':name, 'mail':email}) 
    else:
        return redirect('login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)      
def updateProfile_focal(request):
    if 'FID' in request.session and 'fname' in request.session:
        id = request.session.get('FID')
        password = ''
        confirm = ''
        image = ''
        if request.method == "POST":
            m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
            cursor = m.cursor()
            cursor.execute("select image from focalpicture where FID={}".format(id))
            image = tuple(cursor.fetchall())
            d = request.POST
            for key, value in d.items():
                if key == 'password':
                    password = value
                if key == 'confirmPassword':
                    confirm = value
            if password=="":
                messages.error(request, "Please provide password")
            else:
                if password == confirm:
                    cursor.execute("update focal set password='{}' where FID = {}".format(password,id))
                    m.commit()
                    messages.success(request, "Password changed successfully")
                else:
                    messages.error(request, "The passwords dont match")
        return redirect('fprofile')    
    else:
        return redirect('login') 




# Student
# @login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def s_dashboard(request):
    if 'sid' in request.session and 'name' in request.session:
        sid=request.session.get('sid')
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()

        cursor.execute("select distinct(A_name) from activity where Category='Games and Sports'")
        Gname = cursor.fetchall()

        cursor.execute("select distinct(A_name) from activity where Category='Cultural'")
        Cname = cursor.fetchall()

        cursor.execute("select distinct(A_name) from activity where Category='Academic'")
        Aname = cursor.fetchall()

        programming = ''
        cultural = ''
        academic = ''
        try:

            for i in Gname[0]:
                cursor.execute("select count(record.AID) from record,activity,students where activity.AID = record.AID and students.SID=record.SID and activity.A_name='{}' and students.SID = {};".format(i,sid))
                programming = cursor.fetchall()
            for i in Cname[0]:
                cursor.execute("select count(record.AID) from record,activity,students where activity.AID = record.AID and students.SID=record.SID and activity.A_name='{}' and students.SID = {};".format(i,sid))
                cultural = cursor.fetchall()
            for i in Aname[0]:
                cursor.execute("select count(record.AID) from record,activity,students where activity.AID = record.AID and students.SID=record.SID and activity.A_name='{}' and students.SID = {};".format(i,sid))
                academic = cursor.fetchall()
              
        except:
            pass
        context = {
            'programming':programming,
            'cultural':cultural,
            'academic': academic,
            'gname':Gname,
            'cname':Cname,
            'aname':Aname} 

        return render(request, "student/student_dashboard.html",context)

            
        
       
    else:
        return redirect('login')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def add_records(request):
    if 'sid' in request.session and 'name' in request.session:
        aid = []
        sid=request.session.get('sid')
        status = "Pending"
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
   
        cursor.execute("select distinct(A_name) from activity;")
        A_name = cursor.fetchall()
  
        cursor.execute("select distinct(Category) from activity;")
        Category = cursor.fetchall()

        cursor.execute("select distinct(Year) from activity;")
        Year = cursor.fetchall()

        cursor.execute("select distinct(Semester) from activity;")
        Semester = cursor.fetchall()

        
        if request.method == "POST":
            d=request.POST
            for key,value in d.items():
                if key=="aname":
                    an = value
                if key=="category":
                    category = value
                if key=="year":
                    year = value
                if key=="semester":
                    semester=value
            c = "select AID from activity where A_name='{}' and Category='{}' and Year={} and Semester='{}';".format(an,category,year,semester)
            cursor.execute(c)
            aid = cursor.fetchall()
            if aid==[]:
                messages.error(request,"No such activities")
            else:
                c = "insert into record(SID,AID,status) values({},{},'{}')".format(sid,aid[0][0],status) 
                cursor.execute(c)
                m.commit()
                messages.success(request,"Request succesfully sent")
        return render(request,"student/add_records.html" ,{"A_name":A_name, 'Category':Category, 'Year':Year, 'Semester':Semester, "aid":aid})
    else:
        return redirect('login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
def requests(request):
    if 'sid' in request.session and 'name' in request.session:
        sid=request.session.get('sid')
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        c="select activity.A_name, activity.Year,activity.Semester,record.status from activity join record on activity.AID = record.AID join students on students.SID=record.SID where students.SID={};".format(sid)
        cursor.execute(c)
        table = cursor.fetchall()
        return render(request, "student/request.html", {'table':table[::-1]})
    else:
        return redirect('login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def achievements(request):
    if 'sid' in request.session and 'name' in request.session:
        sid=request.session.get('sid')
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        cursor.execute("select activity.A_name,activity.Category,activity.Year, activity.Semester from record,activity,students where activity.AID = record.AID and students.SID=record.SID and students.SID = {} and status='Approved';".format(sid))
        achieve = cursor.fetchall()
        return render(request, "student/achievement.html", {"achieve":achieve})
    else:
        return redirect('login')
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def profile(request):
    if 'sid' in request.session and 'name' in request.session:
        name = request.session.get('name')
        email = request.session.get('studentemail')
        return render(request, 'student/profile.html', {'name':name, 'studentmail':email}) 
    else:
        return redirect('login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)      
def updateProfile(request):
    if 'sid' in request.session and 'name' in request.session:
        sid = request.session.get('sid')
        password = ''
        confirm = ''
        if request.method == "POST":
            m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
            cursor = m.cursor()
            d = request.POST
            for key, value in d.items():
                if key == 'password':
                    password = value
                if key == 'confirmPassword':
                    confirm = value
            if password=="":
                messages.error(request, "Please provide password")
            else:
                if password == confirm:
                    cursor.execute("update students set Password='{}' where SID = {}".format(password,sid))
                    m.commit()
                    messages.success(request, "Password changed successfully")
                else:
                    messages.error(request, "The passwords dont match")
        return redirect('profile')  
    else:
        return redirect('login') 

#forgot passord
def forgot(request):
    if request.method == "POST":
        d = request.POST
        for key,value in d.items():
            if key == 'forgotpassword':
                subject = "Forgot Password!!!"
                message = 'You are receiving because you request a password reset for your user account \n Click on the link: http://127.0.0.1:8000/password_reset_form/'
                from_email = settings.EMAIL_HOST_USER
                to_list = [value]
                send_mail(subject, message, from_email, to_list, fail_silently=True)
                messages.success(request, " Reset password form Sent successfully. \n Please Check you email!! ")
                request.session['emailforgot'] = value
    return render(request,'password_reset.html')

def forgotform(request):
    if request.method == "POST":
        d = request.POST
        password = ''
        confirm = '' 
        em = request.session.get('emailforgot')
        for key, value in d.items():
            if key == 'passwordChange':
                password = value
            if key == 'confirmPasswordChange':
                confirm = value
        if password == confirm:
            m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
            cursor = m.cursor()
            cursor.execute("update students set Password='{}' where Email = '{}'".format(password,em))   
            m.commit()    
            cursor.execute("update focal set password='{}' where email = '{}'".format(password,em))   
            m.commit()   
            cursor.execute("update admin set password='{}' where email = '{}'".format(password,em))   
            m.commit()   
            messages.success(request, "Password reset successfully")
        else:
            messages.error(request, "The passwords did not match")
    return render(request,'password_reset_form.html')

    
#####Logout######
def logout(request):
    request.session.clear()
    return redirect('index')


#########Accept and reject#######
def button(request):
    if request.method == "POST":
        val=0
        d=request.POST
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        for key,value in d.items():
            if key=='approve':
                val = value
                cursor.execute("update record set status='Approved' where RID={};".format(val))
                m.commit()
            if key=='reject':
                val = value
                cursor.execute("update record set status='Rejected' where RID={};".format(val))
                m.commit()
        return redirect('frequests')

#########Delete#######
def deleteButton(request):
    if request.method == "POST":
        val=0
        d=request.POST
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        for key,value in d.items():
            if key=='deletesingle':
                val = value
                cursor.execute("delete from record where SID={};".format(val))
                cursor.execute("delete from students where SID={};".format(val))
                m.commit()
                return redirect('participants')
            if key=='deleteFocal':
                val = value
                cursor.execute("delete from focal where FID={};".format(val))
                m.commit()
                return redirect('focalp')
            if key=='deleteActivity':
                val = value
                cursor.execute("delete from activity where AID={};".format(val))
                m.commit()
                return redirect('activity')
            


     
    

def bulk_delete(request):
    if request.method == "POST":
        m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
        cursor = m.cursor()
        d=request.POST
        li = ''
        users = ''
        for key, value in d.items():
            if key == "checkuser":
                li = value.split(',')
                users = li[0:-1]
                for i in users:
                    cursor.execute("delete from students where sid={}".format(int(i)))
                    m.commit()
                messages.success(request, "Users deleted successfully")
            if key=='deleteall':
                cursor.execute("delete from students")
                m.commit()
                messages.success(request, "All users deleted successfully")

                
        
    return redirect('participants')
        

                
    



    






   
