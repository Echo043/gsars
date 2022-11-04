from django.shortcuts import render,redirect
import mysql.connector as sql
from django.contrib import messages

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
            messages.success(request, "Invalid Credentials")
        else:
            if role=="Admin":
                m=sql.connect(host="localhost", user="root", password="teko", database="gsars")
                cursor = m.cursor()
                c="select count(*) from students;"
                cursor.execute(c)
                count= (cursor.fetchall)
                return redirect('/Admin')

            if role=="Student":
                return redirect('/student')

            if role=="Focal Person":
                return redirect('/focal')

    return render(request,"login.html")

