from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from EBSystem.forms import LoginForm, SignUpForm

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# -------------------------Web site static page ----------------------#

def homepage(request):
    return render(request,"FrontEnd_page/homepage.html")

def aboutUS(request):
    return render(request, "FrontEnd_page/about_us.html")

def contactUs(request):
    return render(request, "FrontEnd_page/contact_us.html")

#----------------------Dynamic page ----------------------------------#   

#Create your views here.

def newuser(request):
       # Create your views here.
    suform = SignUpForm()
    return render(request, "registration/signup.html",{"signupform": suform}) 
     
def user_login(request):
    loginForm = LoginForm()
    return render(request,"registration/login.html",{"loginForm":loginForm})


def user_logout(request):
    print("logout here")
    auth_logout(request)
    return render(request,"registration/logout.html")
    
def forgetpassword(request):
        return render(request,"registration/password_reset_form.html")


    # @login_required
    # def profilepage(request):
            
    #         url = f"/admin_page/?username={User.username}"
    #         return render(request,url


# ----------------Admin Dashboard -------------------------# 
@login_required(login_url='login')
def adminDashboard(request):

    if request.method =="GET":
        uname = request.GET.get('username')  
    return render(request,"Admin_page.html",{"username":uname})       

# ----------------Employee Dashboard ----------------------# 
@login_required(login_url='login')
def employeeDashboard(request):
    if request.method =="GET":
        uname = request.GET.get('username')  
    return render(request,"BackEnd_page/Employee_page.html",{"username":uname})

# ----------------Customer Dashboard ----------------------# 
@login_required(login_url='login')
def customerDashboard(request):
    if request.method =="GET":
        uname = request.GET.get('username')  
    return render(request,"BackEnd_page/Customer_page.html",{"username":uname}) 

@login_required(login_url='login')
def find(request):
    return render(request, "BackEnd_page/find_user.html")

@login_required(login_url='login')
def calculateBill(request):
    return render(request,"BackEnd_page/calculate_Bill.html")

@login_required(login_url='login')
def billForm(request):
    return render(request, "BackEnd_page/bill_form.html")