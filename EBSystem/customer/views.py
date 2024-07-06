from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Customer,Cus_Profile
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import datetime
import random
from django.conf import settings
from customer.models import Customer,Cus_Profile,  MeterInfo, ServiceCharge, bill,tax
from django.contrib.auth.models import User
from user.models import Profile
from EBSystem.forms import LoginForm, SignUpForm
 
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def customerDashboard(request):
    customer_name = request.session.get("Customer_Name")
    customer_meterno = request.session.get("Customer_MeterNo")
    customer_bio = request.session.get("Customer_Bio")
    customer_phone = request.session.get("Customer_Phone")
    customer_address = request.session.get("Customer_Address")
    customer_status = request.session.get("Customer_Status")
    
    
    
    return render(request,"BackEnd_page/Customer_page.html",
                  {"customer_name":customer_name,
                  "customer_meterno":customer_meterno,
                  "customer_bio":customer_bio,
                  "customer_phone":customer_phone,
                  "customer_address":customer_address,
                  "customer_status":customer_status}
                  
                  )



def AllUserLogin(request):
    
    form = LoginForm(request.POST)
    if form.is_valid():

    # -------------Area to get data from login form ---------------------#   
        
        utype = form.cleaned_data['userType']
        username = form.cleaned_data['userName']
        password = form.cleaned_data['password']
               
    # -------------Area to Employee user to corresponding page -------------------------------# 
    
        if utype =="Admin":
            pass
    
        elif utype =="Employee":
            try:
                print("Employee section")
                user = authenticate(request, username=username,password=password)
                if user is not None:
                    login(request,user)

                    emp_list = User.objects.get(username=username)
                    emp = get_object_or_404(User, username=username)
                    emp_profile = get_object_or_404(Profile, user=emp)

                    emp_Name = f"{emp_list.first_name} {emp_list.last_name}"
                    request.session["Employee_Name"]= emp_Name
                    request.session["Employee_Bio"]= emp_profile.user_bio
                    request.session["Employee_Phone"]= emp_profile.phone_no
                    address = f"{emp_profile.address}, {emp_profile.city}, {emp_profile.state}"
                    request.session["Employee_Address"]= address
                    request.session["Employee_Status"]= emp_profile.state
                                                
                    return redirect("empdash")
                else:
                    print("User not found")
                    return redirect('/login/')
            
            except User.DoesNotExist:
                    messages.info(request,"User Not Found!")
               
                    return redirect('/login/')
                            
            except User.MultipleObjectsReturned:
                    messages.info(request,"Multiple User found, please contact support.")
                  
                    return redirect('/login/')
                            
            except Exception as e:
                    messages.info(request,"invalid credentials!")
                    print(e)  
                    return redirect('/login/')
       
     # -------------Area to Customer user to corresponding page -------------------------------#   
                     
        else:
    
            try:
                cus_list = Customer.objects.get(cus_username=username,cus_password=password)
                if cus_list=="" or cus_list ==None:
                    messages.info(request,"No user Found!")
                    print("user not found")
                    return redirect('/login/')
                        
                else:
                    print(f" {cus_list.cus_username} and {cus_list.cus_password}")
                            
                    cus_profile =Cus_Profile.objects.get(cus_username=username)
                    cus_Name = f"{cus_profile.cus_fname} {cus_profile.cus_lname}"
                    request.session["Customer_Name"]= cus_Name
                    request.session["Customer_MeterNo"]= cus_profile.meter_no
                    request.session["Customer_Bio"]= cus_profile.cus_bio
                    request.session["Customer_Phone"]= cus_profile.phone_no
                    address = f"{cus_profile.address}, {cus_profile.city}, {cus_profile.state}"
                    request.session["Customer_Address"]= address
                    request.session["Customer_Status"]= cus_profile.state
                            
                    return redirect("custdash")
                        
                        
            except Cus_Profile.DoesNotExist:
                    messages.info(request,"Profile Not Found!")
                   
                            
            except Cus_Profile.MultipleObjectsReturned:
                    messages.info(request,"Multiple profiles found, please contact support.")
                  
                            
            except Exception as e:
                    messages.info(request,"invalid credentials!")
                    print(e)
                                 
    else:
        return render (request,"/login/")          

                             

# Create your views here.
def cusSignUp(request):
    
    sgnForm = SignUpForm(request.POST)
    if sgnForm.is_valid():
     
        fname = sgnForm.cleaned_data['f_name']
        lname = sgnForm.cleaned_data['l_name']
        phoneno = sgnForm.cleaned_data['phone_no']
        email = sgnForm.cleaned_data['email']   
        username = sgnForm.cleaned_data['username']
        password = sgnForm.cleaned_data['password']
        repassword = sgnForm.cleaned_data['repassword']
     
        last_login = datetime.datetime.now()
        date_joined = datetime.datetime.now()
            
        print("first name: "+fname)
        print("Last Name: "+lname)
        print("phone no:",phoneno)
        print("email: "+email)
        print("username: "+username)
        print("password "+password)
        print("last login: ",last_login)
        print("date_joined :",date_joined)
              
                
        if password == repassword :
                     
            if Customer.objects.filter(cus_username=username).exists():
                messages.info(request,'User Name exists, Try another username')
                return render(request, "registration/signup.html")  
                    
                    
            elif Cus_Profile.objects.filter(phone_no=phoneno).exists():
                print("Phone No "+phoneno)
                messages.info(request,'Phone No exists, Try another Phone No')
                return render(request, "registration/signup.html")  
                               
                    # elif Profile.objects.filter(email=email).exists():
                    #         messages.info(request,'Email Id exists, Try another Email Id')
                    #         return render(request, "registration/signup.html")  
                        
            else:   
                        
                cus = Customer.objects.create(
                    cus_username = username,
                    cus_password = password,
              
                 )
                cus.save()
                        
                cus_profile = Cus_Profile.objects.create(
                            
                cus_username=username,
                cus_fname=fname,
                cus_lname = lname,
                phone_no = phoneno
                            # email=email   
                            # last_login=last_login,
                            # date_joined=date_joined
                            
                )
                cus_profile.save()
                messages.info(request,'Registration Successful')
                return render(request, "registration/signup.html")  
                    
                        
        else:
            messages.info(request,'password not matched')
            print("password not match")
            return render(request, "registration/signup.html")  
                

    else:  
        form = SignUpForm()
        return render(request, "registration/signup.html",{"signupform":form}) 

@login_required(login_url='login')    
def showCustomerDetails(request):
        try:
                if request.method =="POST":
                        cus_meterno = request.session.get("Customer_MeterNo")
                    
                        
                        bill_details = bill.objects.filter(meter_no = cus_meterno)
                                
                        return render(request, "BackEnd_page/Customer_page.html/", {
                                    'bill_details' : bill_details,
                                    "customer_name": request.session.get("Customer_Name"),
                                    "customer_meterno":request.session.get("Customer_MeterNo"),
                                    "customer_bio":request.session.get("Customer_Bio"),
                                    "customer_phone":request.session.get("Customer_Phone"),
                                    "customer_address": request.session.get("Customer_Address"),
                                    "customer_status":request.session.get("Customer_Status")
                                })
                                            
                else:
                        messages.info(request,'Record not found')  
                        return render(request, "BackEnd_page/Customer_page.html/")
              
        except Exception as e:
            print(e)
            return render(request, "BackEnd_page/Customer_page.html/")  
        
        
                  