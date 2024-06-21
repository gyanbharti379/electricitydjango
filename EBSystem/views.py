from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# -------------------------Web site static page ----------------------#

def homepage(request):
    return render(request,"homepage.html")

def aboutUS(request):
    return render(request, "about_us.html")

def contactUs(request):
    return render(request, "contact_us.html")

#----------------------Dynamic page ----------------------------------#   

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
    return render(request,"Employee_page.html",{"username":uname})

# ----------------Customer Dashboard ----------------------# 
@login_required(login_url='login')
def customerDashboard(request):
    if request.method =="GET":
        uname = request.GET.get('username')  
    return render(request,"Customer_page.html",{"username":uname}) 

@login_required(login_url='login')
def find(request):
    return render(request, "find_user.html")

@login_required(login_url='login')
def calculateBill(request):
    return render(request,"calculate_Bill.html")

@login_required(login_url='login')
def billForm(request):
    return render(request, "bill_form.html")