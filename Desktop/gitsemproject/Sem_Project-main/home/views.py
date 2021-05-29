from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Contact, register_table
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from django.core.mail import EmailMessage

def index(request):

    return render(request,"index.html")

def aboutpage(request):

    return render(request,"about.html")

def faqpage(request):

    return render(request,"faq.html")

def contactpage(request):
    thank = False
    if request.method=="POST":
        nm = request.POST.get("name","")
        con = request.POST.get("contact","")
        sub = request.POST.get("subject","")
        msz = request.POST.get("message","")
        email = request.POST.get("email","")

        data = Contact(name=nm,contact_number=con,subject=sub,message=msz, email=email)
        data.save()
        thank = True

    return render(request,"contact.html",{"thank":thank})
        # return HttpResponse("<h1 style='color:green;'>Dear {} Data Saved Successfully!</h1>".format(nm))


def register(request):
    if "user_id"in request.COOKIES:
        uid = request.COOKIES["user_id"]
        usr = get_object_or_404(User,id=uid)
        login(request,usr)
        if usr.is_superuser:
            return HttpResponseRedirect("/admin")
        if usr.is_active:
            return HttpResponseRedirect("/cust_dashboard")
    if request.method=="POST":
        fname = request.POST["first"]
        last = request.POST["last"]
        un = request.POST["uname"]
        pwd = request.POST["password"]
        em = request.POST["email"]
        con = request.POST["contact"]
        tp = request.POST["utype"]
        
        usr = User.objects.create_user(un,em,pwd)
        usr.first_name = fname
        usr.last_name = last
        
        usr.save()

        reg = register_table(user=usr, contact_number=con)
        reg.save()
        return render(request,"signin.html",{"status":"{} your Account created Successfully".format(fname)})
    return render(request,"register.html")

def check_user(request):
    if request.method=="GET":
        un = request.GET["usern"]
        check = User.objects.filter(username=un)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")

def user_login(request):
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["password"]

        user = authenticate(username=un,password=pwd)
        if user:
            login(request,user)
            if user.is_superuser:
                return HttpResponseRedirect("/admin")
            else:
                res = HttpResponseRedirect("/cust_dashboard")
                if "rememberme" in request.POST:
                    res.set_cookie("user_id",user.id)
                    res.set_cookie("date_login",datetime.now())
                return res
            # if user.is_active:
            #     return HttpResponseRedirect("/cust_dashboard")
                
        else:
            return render(request,"signin.html",{"status":"Invalid Username or Password"})

    return render(request,"signin.html")

@login_required
def cust_dashboard(request):
    context = {}
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    return render(request,"cust_dashboard.html",context)
def job(request):
    context = {}
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    return render(request,"job.html",context)

@login_required
def seller_dashboard(request):
    return render(request,"seller_dashboard.html")
    
@login_required
def user_logout(request):
    logout(request)
    res =  HttpResponseRedirect("/")
    res.delete_cookie("user_id")
    res.delete_cookie("date_login")
    return res

def edit_profile(request):
    context = {}
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"]=data    
    if request.method=="POST":
        fn = request.POST["fname"]
        ln = request.POST["lname"]
        em = request.POST["email"]
        con = request.POST["contact"]
        age = request.POST["age"]
        ct = request.POST["city"]
        you = request.POST["youtube"]

        face = request.POST.get("facebook"," ")
        snap = request.POST.get("snapchat"," ")
        cat1 = request.POST.get("cat1"," ")
        cat2 = request.POST.get("cat2", " ")
        cat3 = request.POST.get("cat3", " ")
        abt = request.POST["about"]

        usr = User.objects.get(id=request.user.id)
        usr.first_name = fn
        usr.last_name = ln
        usr.email = em
        usr.save()

        data.contact_number = con
        data.age = age
        data.city = ct
        data.youtube = you

        data.facebook = face
        data.snapchat = snap
        data.cat1 = cat1
        data.cat2 = cat2
        data.cat3 = cat3
        data.about = abt
        data.save()

        if "image" in request.FILES:
            img = request.FILES["image"]
            data.profile_pic = img
            data.save()


        context["status"] = "Changes Saved Successfully"
    return render(request,"edit_profile.html",context)

def change_password(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]
        
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check==True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Password Changed Successfully!!!"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request,user,  backend='django.contrib.auth.backends.ModelBackend')
        else:
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"

    return render(request,"change_password.html",context)


def forgotpass(request):
    context = {}
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["npass"]

        user = get_object_or_404(User,username=un)
        user.set_password(pwd)
        user.save()

        login(request,user)
        if user.is_superuser:
            return HttpResponseRedirect("/admin")
        else:
            return HttpResponseRedirect("/cust_dashboard")
        # context["status"] = "Password Changed Successfully!!!"

    return render(request,"forgot_pass.html",context)

import random

def reset_password(request):
    un = request.GET["username"]
    try:
        user = get_object_or_404(User,username=un)
        otp = random.randint(1000,9999)
        msz = "Dear {} \n{} is your One Time Password (OTP) \nDo not share it with others \nThanks&Regards \nMyWebsite".format(user.username, otp)
        try:
            email = EmailMessage("Account Verification",msz,to=[user.email])
            email.send()
            return JsonResponse({"status":"sent","email":user.email,"rotp":otp})
        except:
            return JsonResponse({"status":"error","email":user.email})
    except:
        return JsonResponse({"status":"failed"})

def sendcompany(request):
    context={}
    if request.method=="POST":
        job_name = request.POST["job_name"]
        job_email = request.POST["job_email"]
        job_desc = request.POST["job_desc"]
        res = register_table.objects.all()
        for i in res:
            
            i.jobname = job_name
            i.jobemail = job_email
            i.jobdesc = job_desc
            i.save()
            context["status"] = "Changes Saved Successfully"
    return render(request,"company.html",context)

def searchbar(request):
    
          Q = request.GET['Query']
        #   pro1=   register_table.objects.all() 
          if Q=="Food"  :
              Q=2
          pro1= register_table.objects .filter(cat1=Q)  
          pro2= register_table.objects .filter(user__username=Q)
          
          pro=pro1|pro2
          print("SQL Query pro = ",pro.query)
          return render(request,"clients.html",  {'profile': pro})