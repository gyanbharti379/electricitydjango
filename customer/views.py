from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Customer,Cus_Profile
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import datetime
import random
from django.conf import settings
from customer.models import Customer,Cus_Profile,  MeterInfo, ServiceCharge, bill,tax
from django.contrib.auth.models import User
from user.models import Profile

# Create your views here.
def newCustomer(request):
    #form = RegrationForm()
    return render(request, "registration/signup.html") 


def customerDashboard(request):
    customer_name = request.session.get("Customer_Name")
    customer_meterno = request.session.get("Customer_MeterNo")
    customer_bio = request.session.get("Customer_Bio")
    customer_phone = request.session.get("Customer_Phone")
    customer_address = request.session.get("Customer_Address")
    customer_status = request.session.get("Customer_Status")
    
    
    
    return render(request,"Customer_page.html",
                  {"customer_name":customer_name,
                  "customer_meterno":customer_meterno,
                  "customer_bio":customer_bio,
                  "customer_phone":customer_phone,
                  "customer_address":customer_address,
                  "customer_status":customer_status}
                  
                  )



def customerLogin(request):
    
        #authform = AuthenticationForm()
        if request.method=="POST":
              
    # -------------Area to get data from login form ---------------------#   
        
                utype = request.POST.get('opt')
                username = request.POST.get('username')
                password = request.POST.get('password')
               
    # -------------Area to Employee user to corresponding page -------------------------------# 
    
                if utype =="Employee":
                    try:
        
                        #emp_list = Customer.objects.get(cus_username=username,cus_password=password)
                        emp_list = User.objects.get(username=username)
                        emp = get_object_or_404(User, username=username)
                        emp_profile = get_object_or_404(Profile, user=emp)
                                
                        if emp_list=="" or emp_list ==None:
                        
                            messages.info(request,"No user Found!")
                            print("user not found")
                            return redirect('/login/')
                                        
                        else:
                                        
                            emp_Name = f"{emp_list.first_name} {emp_list.last_name}"
                            request.session["Employee_Name"]= emp_Name
                            request.session["Employee_Bio"]= emp_profile.user_bio
                            request.session["Employee_Phone"]= emp_profile.phone_no
                            address = f"{emp_profile.address}, {emp_profile.city}, {emp_profile.state}"
                            request.session["Employee_Address"]= address
                            request.session["Employee_Status"]= emp_profile.state
                                            
                            return redirect("empdash")
                            
                    except User.DoesNotExist:
                            messages.info(request,"User Not Found!")
                            print(e)
                            
                    except User.MultipleObjectsReturned:
                            messages.info(request,"Multiple User found, please contact support.")
                            print(e)
                            
                    except Exception as e:
                            messages.info(request,"invalid credentials!")
                            print(e)  
       
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
                            print(e)
                            
                    except Cus_Profile.MultipleObjectsReturned:
                            messages.info(request,"Multiple profiles found, please contact support.")
                            print(e)
                            
                    except Exception as e:
                            messages.info(request,"invalid credentials!")
                            print(e)
                                 
        else:
            return render (request,"/login/")          
                                

# Create your views here.
def cusSignUp(request):
    
        if request.method == "POST":
            
                fname = request.POST.get('f_name')
                lname = request.POST.get('l_name')
                phoneno = request.POST.get('phone_no')
                email = request.POST.get('email')
                
                username = request.POST.get('username')
                password = request.POST.get('password')
                repassword = request.POST.get('repassword')
                
                last_login = datetime.datetime.now()
                date_joined = datetime.datetime.now()
                
                print("first name: "+fname)
                print("Last Name: "+lname)
                print("phone no:"+phoneno)
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
                            cus_password = password
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
            return render(request, "registration/signup.html") 
    
def showCustomerDetails(request):
        try:
                if request.method =="POST":
                        cus_meterno = request.session.get("Customer_MeterNo")
                    
                        
                        bill_details = bill.objects.filter(meter_no = cus_meterno)
                                
                        return render(request, "Customer_page.html/", {
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
                        return render(request, "Customer_page.html/")
              
        except Exception as e:
            print(e)
            return render(request, "Customer_page.html/")  
        
        
                  