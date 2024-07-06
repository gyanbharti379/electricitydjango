"""
URL configuration for EBSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as authentication_views

from EBSystem import views
from django.conf import settings
from django.conf.urls.static import static
from EBSystem.views import forgetpassword,user_login,user_logout, newuser
from user.views import employeeDashboard,employeeDashboard,customerRegistrationForm,billingPage,reminderForm,customerRegistration,meterRegistration,serviceChargeRegistration, calculateBillForm, calFindCustomer, updateProfile, generateBillForm, findCustomer,showAllCustomer,billingPage_Form, payBillForm,reminderFindCustomerPage_Form,sendWBmessage, sendReminderEmail
from customer.views import customerDashboard,AllUserLogin, cusSignUp, showCustomerDetails
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',user_login, name="login"),
    path('logout/',user_logout, name="logout"),
    
   
    # path('login/',authentication_views.LoginView.as_view(template_name="registration/login.html",), name="login"),
    # path('logout/',authentication_views.LogoutView.as_view(template_name="registration/logout.html"), name="logout"),
    # # path('profile/',profilepage, name='profile'),
    
# --------------website static page ----------------------------#
    path('',views.homepage,name="home"),
    path('about/', views.aboutUS, name="about"),
    path('conctact_us/',views.contactUs, name="contactus"),
    
     
    path('new_user/',newuser, name="signup"),
    path('forgetpass/',forgetpassword, name="forgetpass"),
   
# #----------------------Dynamic page ----------------------------------# 
# # ---------- App View -------------------  

    path('submitloginForm/', AllUserLogin, name="submitloginForm"),
    path('submitsignupForm/',cusSignUp, name="submitsignupForm"),

# ----------------Admin Dashboard -------------------------# 
    path('admin_page/',views.adminDashboard, name="admindash"),

# ----------------Employee Dashboard ----------------------# 
    path('employee_page/',employeeDashboard, name="empdash"),
    path('customer_regis_page/',customerRegistrationForm, name="cusReg"),
    path('customerbilling_page/',billingPage, name="billing"),
    path('billing_form/',billingPage_Form, name="billingForm"),
    path('paybillform/',payBillForm, name="paybillForm"),
    
    path('customerReminder_page/',reminderForm, name="reminder"),
    path('calculateBill_page/',calculateBillForm, name="calculateBill"),
    
    path('cal_find_customer/',calFindCustomer, name='cal_find_customer'),
    path('find_customer/',findCustomer, name='find_customer'),
    path('show_All_customer/',showAllCustomer, name='show_All_customer'),
   
    path('update_customer/',updateProfile, name='update_customer'),
    path('generate_bill_page/',generateBillForm, name='generate_bill'),
    
# -------------Reminder ------------------------------------------#
    path('reminder_find_page/',reminderFindCustomerPage_Form, name='reminder_find'),
    path('sendmsg_form/',sendWBmessage, name='sendmsg_form'),
    path('sendemail_form/',sendReminderEmail, name='sendemail_form'),
     
# ----------------Customer Dashboard ----------------------# 
    path('customer_page/',customerDashboard, name="custdash"),
    path('customer_billing_page/',showCustomerDetails, name="cus_bill_page"),
    
    path('customer_Registration_Form/',customerRegistration, name="Cus_Registration_Form" ),
    path('meter_Registration_Form/',meterRegistration, name="meter_Registration_Form" ),
    path('service_Charge_Form/',serviceChargeRegistration, name="service_Charge_Form" ),
     
    path('find/',views.find, name="find"),
    
    path('calculate_bill/',views.calculateBill,name="calculate"),
    path('billForm/',views.billForm,name="bill"),
     
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


