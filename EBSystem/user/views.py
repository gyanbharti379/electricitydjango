from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
import logging 
from django.db.models.functions import ExtractMonth
import user.signals
from django.contrib.auth.forms import AuthenticationForm
                
from datetime import datetime
import calendar 
from django.conf import settings 
import pywhatkit as kit
import random
import qrcode
from django.shortcuts import render, HttpResponse
from io import BytesIO
from django.views.decorators.http import require_http_methods
import os
from django.core.mail import send_mail

from datetime import datetime
from dotenv import load_dotenv
from customer.models import Customer,Cus_Profile,  MeterInfo, ServiceCharge, bill,tax
 
from customer.forms import SendWAMessageForm, SendEmailForm, CalculateBillForm 
from django.contrib.auth.decorators import login_required
 
logger = logging.getLogger(__name__) 



@login_required(login_url='login')
def employeeDashboard(request):
         

        return render(request,"BackEnd_page/Employee_page.html",
                    {"Employee_name":request.session.get("Employee_Name"),
                    "Employee_bio":request.session.get("Employee_Bio"),
                    "Employee_phone":request.session.get("Employee_Phone"),
                    "Employee_address":request.session.get("Employee_Address"),
                    "Employee_status":request.session.get("Employee_Status")
                    })
        
def customerRegistrationForm(request):
        emp_name = request.session.get("Employee_Name")
        emp_bio = request.session.get("Employee_Bio")
        
        return render(request, "BackEnd_page/customer_registration.html", 
                    {"Employee_name":emp_name,
                    "Employee_bio":emp_bio,
                    })
@login_required(login_url='login')
def billingPage(request):
        emp_name = request.session.get("Employee_Name")
        emp_bio = request.session.get("Employee_Bio")
      
        return render(request, "BackEnd_page/bill_form.html",
                    {"Employee_name":emp_name,
                    "Employee_bio":emp_bio,
                    "Employee_name":request.session.get("Employee_Name"),
                    "Employee_bio":request.session.get("Employee_Bio"),
                    "Employee_phone":request.session.get("Employee_Phone"),
                    "Employee_address":request.session.get("Employee_Address"),
                    "Employee_status":request.session.get("Employee_Status")
                    })
@login_required(login_url='login')       
def billingPage_Form(request):
    
    if request.method =="POST":
                
        try:
            
            cus_meterno = request.POST.get('meterno') 
               
            setattr(settings,"emp_meterNo",cus_meterno)
                        
            search_profile = Cus_Profile.objects.get(meter_no = cus_meterno)
            bill_details = bill.objects.filter(meter_no = cus_meterno)
            
            return render(request, "BackEnd_page/bill_form.html",
                                    {'user_profiles': search_profile,
                                    'bill_details' : bill_details, 
                                    "Employee_name":request.session.get("Employee_Name"),
                                    "Employee_bio":request.session.get("Employee_Bio"),
                                    "Employee_phone":request.session.get("Employee_Phone"),
                                    "Employee_address":request.session.get("Employee_Address"),
                                    "Employee_status":request.session.get("Employee_Status")
                                   })
                        
        except Exception as e:
                    print(e)
                    return render(request, "BackEnd_page/bill_form.html/")
                                                   
    else:
                        messages.info(request,'Record not found')  
                        return render(request, "BackEnd_page/bill_form.html/")     
                    
@login_required(login_url='login')                    
def payBillForm(request):
    
    if request.method =="POST":
                
        try:
            
            cus_meterno = settings.emp_meterNo
            cus_month = request.POST.get('payBillMonth') 
            cus_amt = request.POST.get('billAmount') 
            
            #Save data to bill table
            bill_details = bill.objects.get(meter_no = cus_meterno,cus_month=cus_month)
            bill_details.cus_status = "Paid"
            bill_details.save()
            
            
            
            #QR code geberate for amount
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data('Pay amount Rs. ' + cus_amt)
            qr.make(fit=True)
            
            # Create an image from the QR Code instance
            img = qr.make_image(fill_color="red", back_color="white")

            # Create a unique filename based on the current time
            filename = f"qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(settings.MEDIA_ROOT, 'qr_codes', filename)

            # Save the image to the specified folder
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            img.save(filepath)

            # Render the template with the QR code URL
            qr_code_url = os.path.join(settings.MEDIA_URL, 'qr_codes', filename)
            return render(request, 'BackEnd_page/qrcode_page.html', {'qr_code_url': qr_code_url, 'data_month': cus_month,
                                                        "Employee_name":request.session.get("Employee_Name"),
                                                            "Employee_bio":request.session.get("Employee_Bio"),
                                                            "Employee_phone":request.session.get("Employee_Phone"),
                                                            "Employee_address":request.session.get("Employee_Address"),
                                                            "Employee_status":request.session.get("Employee_Status")
                                                        
                                                        })

        except Exception as e:
                    print(e)
                    return render(request, "BackEnd_page/bill_form.html/")
                                                   
    else:
            messages.info(request,'Record not found')  
            return render(request, "BackEnd_page/bill_form.html/") 
         
                       
@login_required(login_url='login')
def reminderForm(request):
        emp_name = request.session.get("Employee_Name")
        emp_bio = request.session.get("Employee_Bio")
        WAform = SendWAMessageForm()
        EmailForm = SendEmailForm()
        
         
        return render(request, "BackEnd_page/reminder.html",
                    {"Employee_name":emp_name,
                    "Employee_bio":emp_bio,
                    "Employee_name":request.session.get("Employee_Name"),
                    "Employee_bio":request.session.get("Employee_Bio"),
                    "Employee_phone":request.session.get("Employee_Phone"),
                    "Employee_address":request.session.get("Employee_Address"),
                    "Employee_status":request.session.get("Employee_Status"),
                    "RWAForm": WAform,
                    "EmailForm": EmailForm,
                     })
@login_required(login_url='login')        
def reminderFindCustomerPage_Form(request):
    
    if request.method =="POST":
                
        try:
            
            cus_meterno = request.POST.get('meterno') 
            form = SendWAMessageForm()
            EmailForm = SendEmailForm()
               
            setattr(settings,"emp_meterNo",cus_meterno)
                        
            search_profile = Cus_Profile.objects.get(meter_no = cus_meterno)
           
            
            return render(request, "BackEnd_page/reminder.html",
                                    {'user_profiles': search_profile,
                                     "Employee_name":request.session.get("Employee_Name"),
                                    "Employee_bio":request.session.get("Employee_Bio"),
                                    "Employee_phone":request.session.get("Employee_Phone"),
                                    "Employee_address":request.session.get("Employee_Address"),
                                    "Employee_status":request.session.get("Employee_Status"),
                                    "RWAForm": form,
                                    "EmailForm": EmailForm,
                                   })
                        
        except Exception as e:
                    print(e)
                    return render(request, "BackEnd_page/bill_form.html/")
                                                   
    else:
            messages.info(request,'Record not found')  
            return render(request, "BackEnd_page/bill_form.html/")        

@login_required(login_url='login')        
def sendWBmessage(request):
    
    if request.method =="POST":
                
        try:
            form = SendWAMessageForm(request.POST)
            if form.is_valid():
                cus_meterno = settings.emp_meterNo
                cus_phone = str(form.cleaned_data['phone'])
                cus_month = form.cleaned_data['reminderSelectMonth']
                cus_billAmount = form.cleaned_data['billAmount']
                cus_message = form.cleaned_data['message']
               
                #Save data to bill table
                bill_details = bill.objects.get(meter_no = cus_meterno,cus_month=cus_month)
                bill_details.reminder = "send"
                bill_details.save()
                
                phone_no = "+91"+cus_phone
                dt = datetime.now()
                time = dt.time()
                tt = str(time)

                hh = int(tt[0:2])
                mm = int(tt[3:5])
                mm += 1

                #set message content
                message = f"*This message is from Electricity Billing Management System*\n\nInformed you to pay *{cus_month}* month bill amount Rs. *{cus_billAmount}* pay your electricity bill before due date to avoid late payment charges\n\n*{cus_message}*"
                kit.sendwhats_image(phone_no,"icon/logo.jpg",message)
                msg = "send message successfully"
              
                
                return render(request, "BackEnd_page/reminder.html",
                                        {'show_message': msg,
                                        "Employee_name":request.session.get("Employee_Name"),
                                        "Employee_bio":request.session.get("Employee_Bio"),
                                        "Employee_phone":request.session.get("Employee_Phone"),
                                        "Employee_address":request.session.get("Employee_Address"),
                                        "Employee_status":request.session.get("Employee_Status"),
                                        
                                    })
            else:
                emp_name = request.session.get("Employee_Name")
                emp_bio = request.session.get("Employee_Bio")
                form = SendWAMessageForm()
                EmailForm = SendEmailForm()
         
                return render(request, "BackEnd_page/reminder.html",
                    {"Employee_name":emp_name,
                    "Employee_bio":emp_bio,
                    "Employee_name":request.session.get("Employee_Name"),
                    "Employee_bio":request.session.get("Employee_Bio"),
                    "Employee_phone":request.session.get("Employee_Phone"),
                    "Employee_address":request.session.get("Employee_Address"),
                    "Employee_status":request.session.get("Employee_Status"),
                    "RWAForm": form,
                    "EmailForm": EmailForm,
                     })            
        except Exception as e:
                    print(e)
                    return render(request, "BackEnd_page/reminder.html/")
                                                   
    else:
            messages.info(request,'Record not found')  
            return render(request, "BackEnd_page/reminder.html/") 

@login_required(login_url='login')        
def sendReminderEmail(request):
    
    if request.method =="POST":
                
        try:
            form = SendEmailForm(request.POST)
            if form.is_valid():
                
                cus_meterno = settings.emp_meterNo
                cus_email = form.cleaned_data['email']
                cus_month = form.cleaned_data['reminderSelectMonth']
                cus_billAmount = form.cleaned_data['billAmount']
                cus_subject = form.cleaned_data['subject'] 
                cus_message = form.cleaned_data['message'] 
                                        
                #Save data to bill table
                bill_details = bill.objects.get(meter_no = cus_meterno,cus_month=cus_month)
                bill_details.reminder = "send"
                bill_details.save()
                
                subject = cus_subject
                message =  f"This message is from Electricity Billing Management System*\n\nInformed you to pay {cus_month} month bill amount Rs. {cus_billAmount} pay your electricity bill before due date to avoid late payment charges\n\n{cus_message}"
                email_from = settings.DEFAULT_FROM_EMAIL
                recipient_list = [cus_email]
                
                send_mail(subject, message, email_from, recipient_list)
            
                msg = "send message successfully"
                
                return render(request, "BackEnd_page/reminder.html",
                                        {'show_message': msg,
                                        "Employee_name":request.session.get("Employee_Name"),
                                        "Employee_bio":request.session.get("Employee_Bio"),
                                        "Employee_phone":request.session.get("Employee_Phone"),
                                        "Employee_address":request.session.get("Employee_Address"),
                                        "Employee_status":request.session.get("Employee_Status")
                                    })
            else:    
                    emp_name = request.session.get("Employee_Name")
                    emp_bio = request.session.get("Employee_Bio")
                    form = SendWAMessageForm()
                    EmailForm = SendEmailForm()
            
                    return render(request, "BackEnd_page/reminder.html",
                        {"Employee_name":emp_name,
                        "Employee_bio":emp_bio,
                        "Employee_name":request.session.get("Employee_Name"),
                        "Employee_bio":request.session.get("Employee_Bio"),
                        "Employee_phone":request.session.get("Employee_Phone"),
                        "Employee_address":request.session.get("Employee_Address"),
                        "Employee_status":request.session.get("Employee_Status"),
                        "RWAForm": form,
                        "EmailForm":EmailForm,
                        })  
                        
        except Exception as e:
                    print(e)
                    return render(request, "BackEnd_page/reminder.html/")
                                                   
    else:
            messages.info(request,'Record not found')  
            return render(request, "BackEnd_page/reminder.html/")              
       
@login_required(login_url='login')    
def calculateBillForm(request):
        emp_name = request.session.get("Employee_Name")
        emp_bio = request.session.get("Employee_Bio")
        calform = CalculateBillForm()
        
        return render(request, "BackEnd_page/calculate_Bill.html",
                    {"Employee_name":emp_name,
                    "Employee_bio":emp_bio,
                    "calForm":calform,
                     })

@login_required(login_url='login')        
def calculate(request):
    try:
            form = CalculateBillForm(request.POST)
            if form.is_valid():
                cus_meterno = form.cleaned_data['meterno']
             
                search_profile = Cus_Profile.objects.get(meter_no = cus_meterno)
                bill_details = bill.objects.get(meter_no = cus_meterno)
                
                gen_month = form.cleaned_data['generateBillMonth']
                gen_unit =  form.cleaned_data['unit']
        
                search_tax = tax.objects.get(id = 1)
            
                tc = gen_unit * search_tax.cost_per_unit
               
                mr = (search_tax.meter_rent*tc)/100
                sc = (search_tax.service_charge * tc) / 100
                st = (search_tax.service_tax * tc) / 100
                sbc = (search_tax.swacch_bharat_cess * tc) / 100
                ft = (search_tax.fixed_tax * tc) / 100
                total_bill = mr+sc+st+sbc+ft
            
                return render(request, "BackEnd_page/show_generateBill_page.html",
                            {'user_profiles': search_profile,
                            'bill_details' : bill_details, 
                            "gen_month":gen_month,
                            "gen_unit_Consumed":gen_unit,
                            "gen_cost_per_unit": search_tax.cost_per_unit,
                            "gen_meter_rent": mr,
                            "gen_service_charge":sc,
                            "gen_service_tax":st,
                            "gen_swachh_bcess":sbc,
                            "gen_fix_tax":ft,
                            "gen_total_bill":total_bill,
                            
                            })
                
            else:
                calform = CalculateBillForm()
                messages.info(request,'Record not found')  
                return render(request, "BackEnd_page/customer_Details_page.html/",{
                    "calForm":calform,
                })
              
    except Exception as e:
        print(e)
        return render(request, "BackEnd_page/customer_Details_page.html/", {
                                    'user_profiles': search_profile,
                                     "Employee_name":request.session.get("Employee_Name"),
                                    "Employee_bio":request.session.get("Employee_Bio"),
                                    "Employee_phone":request.session.get("Employee_Phone"),
                                    "Employee_address":request.session.get("Employee_Address"),
                                    "Employee_status":request.session.get("Employee_Status")
                                })   


@login_required(login_url='login')
def get_next_month(current_month):
    # Define the current year, use 2024 as an example
    current_year = 2024

    # Parse the current month name to a datetime object
    current_date = datetime.strptime(current_month, "%B")

    # Get the next month number and year
    next_month_num = current_date.month % 12 + 1
    next_year = current_year + (current_date.month // 12)

    # Create a datetime object for the first day of the next month
    next_month_date = datetime(next_year, next_month_num, 1)

    # Get the month name of the next month
    next_month_name = next_month_date.strftime("%B")

    return next_month_name        
                
@login_required(login_url='login')     
def generateBillForm(request):
    

            if request.method =="POST":
                
                try:
                
                    #create
                    cus_bill = bill.objects.create(
                    meter_no = settings.emp_meterNo, 
                    cus_month = settings.bill_month,
                    units = getattr(settings,"cus_unit"),
                    total_bills = getattr(settings,"cus_bill_amount"),
                    )
                    cus_bill.save()
                
                    return render(request, "BackEnd_page/calculate_Bill.html", {'success':'Bill Generate Succfully'})
                
                except Exception as e:
                    print(e)
                    return render(request, "BackEnd_page/calculate_Bill.html/",  {'error': 'Record not found'})
                            
            else:
                  
                    return render(request, "BackEnd_page/calculate_Bill.html/",  {'error': 'Record not found'})
              
    
                
@login_required(login_url='login')   
def showAllCustomer(request):
        try:
                if request.method =="POST":
                        search_profile = Cus_Profile.objects.all() 
                        return render(request, "BackEnd_page/customer_registration.html/", {    
                                    'result': search_profile,
                                    "Employee_name":request.session.get("Employee_Name"),
                                    "Employee_bio":request.session.get("Employee_Bio"),
                                    "Employee_phone":request.session.get("Employee_Phone"),
                                    "Employee_address":request.session.get("Employee_Address"),
                                    "Employee_status":request.session.get("Employee_Status")
                                })
                                            
                else:
                        messages.info(request,'Record not found')  
                        return render(request, "BackEnd_page/customer_Details_page.html/")
              
        except Exception as e:
            print(e)
            return render(request, "BackEnd_page/DataNotFound.html/")
                                   
      
@login_required(login_url='login')   
def calFindCustomer(request):
   
            if request.method =="POST":
                
                try:
                    calform = CalculateBillForm()
                    form = CalculateBillForm(request.POST)
                    if form.is_valid():
            
                        cus_meterno = form.cleaned_data['meterno']
                        gen_month = form.cleaned_data['generateBillMonth']
                        gen_unit =  form.cleaned_data['unit']
                
                        setattr(settings,"emp_meterNo",cus_meterno)
                        setattr(settings,"bill_month",gen_month)
                        setattr(settings,"cus_unit",gen_unit)
                    
            
                        search_profile = Cus_Profile.objects.get(meter_no = cus_meterno)
                        bill_details = bill.objects.filter(meter_no = cus_meterno)
                        search_tax = tax.objects.get(id = 1)
                    
                        tc = gen_unit * search_tax.cost_per_unit
                    
                        mr = (search_tax.meter_rent*tc)/100
                        sc = (search_tax.service_charge * tc) / 100
                        st = (search_tax.service_tax * tc) / 100
                        sbc = (search_tax.swacch_bharat_cess * tc) / 100
                        ft = (search_tax.fixed_tax * tc) / 100
                        total_bill = mr+sc+st+sbc+ft
                        
                        setattr(settings,"cus_bill_amount",total_bill)
                        
                        return render(request, "BackEnd_page/calculate_Bill.html",
                                    {'user_profiles': search_profile,
                                    'bill_details' : bill_details, 
                                    "gen_month":gen_month,
                                    "gen_unit_Consumed":gen_unit,
                                    "gen_cost_per_unit": search_tax.cost_per_unit,
                                    "gen_meter_rent": mr,
                                    "gen_service_charge":sc,
                                    "gen_service_tax":st,
                                    "gen_swachh_bcess":sbc,
                                    "gen_fix_tax":ft,
                                    "gen_total_bill":total_bill,
                                    "Employee_name":request.session.get("Employee_Name"),
                                    "Employee_bio":request.session.get("Employee_Bio"),
                                    "Employee_phone":request.session.get("Employee_Phone"),
                                    "Employee_address":request.session.get("Employee_Address"),
                                    "Employee_status":request.session.get("Employee_Status"),
                                   "calForm":calform,
                                   })
                        
                except Exception as e:
                    print(e)
                    return render(request, "BackEnd_page/calculate_Bill.html/")
                                                   
            else:
                        messages.info(request,'Record not found')  
                        return render(request, "BackEnd_page/calculate_Bill.html/")
              
@login_required(login_url='login')        
def findCustomer(request):
        try:
            if request.method =="POST":
            
                cus_meterno = request.POST.get('meterno') 
                gen_month = request.POST.get('generateBill-type')
                gen_unit =  int(request.POST.get('unit'))
                
                settings.emp_meterNo = cus_meterno
                settings.bil_month = gen_month   
                settings.cus_unit = gen_unit
                settings.cus_bill_amount = 0
      
                search_profile = Cus_Profile.objects.get(meter_no = cus_meterno)
                bill_details = bill.objects.get(meter_no = cus_meterno)
                search_tax = tax.objects.get(id = 1)
            
                tc = gen_unit * search_tax.cost_per_unit
               
                mr = (search_tax.meter_rent*tc)/100
                sc = (search_tax.service_charge * tc) / 100
                st = (search_tax.service_tax * tc) / 100
                sbc = (search_tax.swacch_bharat_cess * tc) / 100
                ft = (search_tax.fixed_tax * tc) / 100
                total_bill = mr+sc+st+sbc+ft
                settings.cus_bill_amount = total_bill
            
                return render(request, "BackEnd_page/calculate_Bill.html",
                            {'user_profiles': search_profile,
                            'bill_details' : bill_details, 
                            "gen_month":gen_month,
                            "gen_unit_Consumed":gen_unit,
                            "gen_cost_per_unit": search_tax.cost_per_unit,
                            "gen_meter_rent": mr,
                            "gen_service_charge":sc,
                            "gen_service_tax":st,
                            "gen_swachh_bcess":sbc,
                            "gen_fix_tax":ft,
                            "gen_total_bill":total_bill,
                            "Employee_name":request.session.get("Employee_Name"),
                                "Employee_bio":request.session.get("Employee_Bio"),
                                "Employee_phone":request.session.get("Employee_Phone"),
                                "Employee_address":request.session.get("Employee_Address"),
                                "Employee_status":request.session.get("Employee_Status")
                            })
                                                        
            else:
                        messages.info(request,'Record not found')  
                        return render(request, "BackEnd_page/calculate_Bill.html/")
              
        except Exception as e:
                print(e)
                search_tax = tax.objects.get(id = 1)
            
                tc = gen_unit * search_tax.cost_per_unit
               
                mr = (search_tax.meter_rent*tc)/100
                sc = (search_tax.service_charge * tc) / 100
                st = (search_tax.service_tax * tc) / 100
                sbc = (search_tax.swacch_bharat_cess * tc) / 100
                ft = (search_tax.fixed_tax * tc) / 100
                total_bill = mr+sc+st+sbc+ft
            
                return render(request, "BackEnd_page/calculate_Bill.html",
                            {'user_profiles': search_profile,
                             
                            "gen_month":gen_month,
                            "gen_unit_Consumed":gen_unit,
                            "gen_cost_per_unit": search_tax.cost_per_unit,
                            "gen_meter_rent": mr,
                            "gen_service_charge":sc,
                            "gen_service_tax":st,
                            "gen_swachh_bcess":sbc,
                            "gen_fix_tax":ft,
                            "gen_total_bill":total_bill,
                            "Employee_name":request.session.get("Employee_Name"),
                            "Employee_bio":request.session.get("Employee_Bio"),
                            "Employee_phone":request.session.get("Employee_Phone"),
                            "Employee_address":request.session.get("Employee_Address"),
                            "Employee_status":request.session.get("Employee_Status")
                            })   

@login_required(login_url='login')            
def showCustomer(request):
        try:
                if request.method =="POST":
                        cus_meterno = request.POST.get('meterno') 
                        
                        search_profile = Cus_Profile.objects.get(meter_no = cus_meterno)
                        bill_details = bill.objects.get(meter_no = cus_meterno)
                                
                        return render(request, "BackEnd_page/customer_Details_page.html/", {
                                    'user_profiles': search_profile,
                                    'bill_details' : bill_details
                                })
                                            
                else:
                        messages.info(request,'Record not found')  
                        return render(request, "BackEnd_page/customer_Details_page.html/")
              
        except Exception as e:
            print(e)
            return render(request, "BackEnd_page/customer_Details_page.html/", {
                                    'user_profiles': search_profile,
                                     
                                })

@login_required(login_url='login')      
def updateProfile(request):
        try:
        
            if request.method == "POST":
                
                cus_phoneno = int(request.POST.get('phone_no'))
                cus_email = request.POST.get('email')
                cus_pass = request.POST.get('password')
               
                # update cutomer profile    
                new_profile = Cus_Profile.objects.get(cus_username = settings.emp_username)
                new_profile.phone_no = cus_phoneno
                new_profile.email = cus_email
                new_profile.save()
                
                #update customer login
                new_Cus_profile = Customer.objects.get(cus_username = settings.emp_username)
                new_Cus_profile.cus_password = cus_pass
                new_Cus_profile.save()
                
                messages.info(request,'Data update Successful')
                return render(request, "BackEnd_page/Employee_page.html")  
                        
                        
            else:  
                return render(request, "BackEnd_page/Employee_page.html") 
        
        except Exception as e:
            print(e)            
            
       
@login_required(login_url='login')            
def customerRegistration(request):
        try:
        
            if request.method == "POST":
                
                cus_fname = request.POST.get('customerFirstName')
                cus_lname = request.POST.get('customerLastName')
                cus_phoneno = request.POST.get('phonenumber')
                cus_email = request.POST.get('email')
                cus_address = request.POST.get('address')
                cus_city = request.POST.get('city')
                cus_state = request.POST.get('state')
                cus_status= request.POST.get('status')
                cus_date = request.POST.get('date')
                
                settings.emp_username = cus_email
                    
                last_login = datetime.datetime.now()
                settings.emp_phoneNo = cus_phoneno
                cus = Customer.objects.create(
                            cus_username = cus_email,
                            cus_password = cus_phoneno,
                            cus_last_login = last_login
                        )
                cus.save()
                            
                cus_profile = Cus_Profile.objects.create(
                                
                            cus_username= cus_email,
                            cus_fname = cus_fname,
                            cus_lname = cus_lname,
                            phone_no = cus_phoneno,
                            email = cus_email,
                            cus_doj = cus_date,
                            address = cus_address,
                            city =  cus_city,
                            state = cus_state,
                            cus_status =  cus_status
                            
                        )
                cus_profile.save()
                messages.info(request,'Data Saved Successful')
                return render(request, "BackEnd_page/customer_registration.html")  
                        
                        
            else:  
                return render(request, "BackEnd_page/registration/signup.html") 
        
        except Exception as e:
            print(e) 
            
    
@login_required(login_url='login')
def meterRegistration(request):
        try:
        
            if request.method == "POST":
                
                cus_meterno = int(request.POST.get('meterno'))
                cus_meterLocation = request.POST.get('meterlocation')
                cus_meterType = request.POST.get('metertype')
                cus_phaseCode = request.POST.get('phasecode')
                cus_billType = request.POST.get('biltype')
                cus_date = request.POST.get('cdate')
             
                date_obj = datetime.datetime.strptime(cus_date, '%Y-%m-%d')
                month_str = date_obj.strftime('%B')
           
                settings.emp_meterNo = cus_meterno
                settings.bill_month = month_str
             
                # update meter no in customer login table     
                new_profile = Cus_Profile.objects.get(cus_username = settings.emp_username)
                new_profile.meter_no = cus_meterno
                new_profile.save()
                
                print("User name ", new_profile.cus_username)
                
                #create new meter information in Meter infor table       
                cus_meterinfo = MeterInfo.objects.create(   
                            meter_no = cus_meterno,
                            meter_location = cus_meterLocation,
                            meter_type = cus_meterType,
                            phase_code = cus_phaseCode,
                            bill_type = cus_billType,
                            date_of_reg = cus_date       
                        )
                cus_meterinfo.save()
                messages.info(request,'Data Saved Successful')
                return render(request, "BackEnd_page/customer_registration.html")  
                        
                        
            else:  
                return render(request, "registration/signup.html") 
        
        except Exception as e:
            print(e)
             
@login_required(login_url='login')            
def serviceChargeRegistration(request):
        try:
        
            if request.method == "POST":
                
                cus_meterFileCharge = int(request.POST.get('Meter_File_Charge'))
                cus_meterCharge = int(request.POST.get('Meter_Charge'))
                cus_connCharge = int(request.POST.get('connection_Charge'))
                cus_labourCharge = int(request.POST.get('labour_charge'))
                cus_advtCharge = int(request.POST.get('advance_deposite'))
                cus_balance = int(request.POST.get('balance'))
                
                cus_SC = ServiceCharge.objects.create(
                        
                meter_no = settings.emp_meterNo,        
                meter_file_charge = cus_meterFileCharge,
                meter_charge = cus_meterCharge,
                con_charge = cus_connCharge,
                labour_charge = cus_labourCharge,
                adv_deposite = cus_advtCharge,
                balance = cus_balance
                            
                )
                cus_SC.save()
                
                messages.info(request,'Data Saved Successful')
                return render(request, "BackEnd_page/customer_registration.html")   
                        
                        
            else:  
                return render(request, "registration/signup.html") 
        
        except Exception as e:
            print(e) 
        
