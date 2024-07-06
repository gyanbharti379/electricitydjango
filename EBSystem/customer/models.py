from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import datetime

# Create your models here.

class Customer(models.Model):
    
    id = models.AutoField(primary_key=True)
    cus_utype = models.CharField(max_length=50, default="Customer")
    cus_username = models.CharField(max_length=150, unique=True)
    cus_password = models.CharField(max_length=128)
    cus_last_login = models.DateTimeField(default=timezone.now)
    #cus_last_login = models.DateTimeField(auto_now=False, auto_now_add=False, default="")
    
    def __str__(self):
        return self.cus_username
    
    def set_password(self,raw_password):
        self.cus_password = make_password(raw_password)
        
    def check_password(self,raw_password):
        return check_password(raw_password,self.cus_password)
         
    
class Cus_Profile(models.Model):
    
    id = models.AutoField(primary_key=True)
    cus_username = models.CharField(max_length=50, unique=True)
    meter_no = models.IntegerField(default=0)
    cus_fname = models.CharField(max_length=50, default="")
    cus_lname = models.CharField(max_length=50, default="")
    cus_doj = models.DateTimeField(default=timezone.now)
    #cus_doj = models.DateTimeField(auto_now=False, auto_now_add=False, default="")
    phone_no = models.CharField(max_length=50, unique=True)
    email = models.EmailField(default="abc@gmail.com")
    cus_bio = models.TextField(max_length=100)
    cus_profile_img = models.ImageField(default="media\icon\person-man.webp", upload_to="profile_img")
    address = models.TextField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    cus_status = models.CharField(max_length=50)
    
    def __str__(self):
        return self.cus_username
    
    @property
    def getFullName(self):
        return f"{self.cus_fname} {self.cus_lname}"
    
    @property
    def getMonth(self):
        
        d = f"{self.cus_doj}"
        date_obj = datetime.strptime(d, '%Y-%m-%d %H:%M:%S%z')
        month_str = date_obj.strftime('%B')
        
        print("Month",month_str)
        return month_str
    
class MeterInfo(models.Model):
    id = models.AutoField(primary_key=True)
    meter_no = models.IntegerField(default=0)
    meter_location = models.TextField(max_length=100)
    meter_type = models.CharField(max_length=50)
    phase_code = models.CharField(max_length=50)
    bill_type = models.CharField(max_length=50)
    date_of_reg = models.DateField()
    #date_of_reg = models.DateTimeField(auto_now=False, auto_now_add=False, default="")
    cus_status = models.TextField(max_length=100,  default="pending")
    
    def __str__(self):
        return self.meter_no
    
    
class ServiceCharge(models.Model):
    id = models.AutoField(primary_key=True)
    meter_no = models.IntegerField(default=0)
    meter_file_charge = models.IntegerField(default=0)
    meter_charge = models.IntegerField(default=0)
    con_charge = models.IntegerField(default=0)
    labour_charge = models.IntegerField(default=0)
    adv_deposite = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    
    def __str__(self):
        return self.id
    
class tax(models.Model):
    id = models.AutoField(primary_key=True)
    cost_per_unit = models.IntegerField(default=0)
    meter_rent = models.IntegerField(default=0)
    service_charge = models.IntegerField(default=0)
    service_tax = models.IntegerField(default=0)
    swacch_bharat_cess = models.IntegerField(default=0)
    fixed_tax = models.IntegerField(default=0)
    
    def __str__(self):
        return self.id
    
    
class bill(models.Model):
    id = models.AutoField(primary_key=True)
    meter_no = models.IntegerField(default=0)
    cus_month = models.CharField(max_length=20)
    units = models.IntegerField(default=0)
    total_bills = models.IntegerField(default=0)
    cus_status = models.CharField(max_length=50,  default="pending")
    reminder = models.TextField(max_length=100, default="not send")
    
    def __str__(self):
        return self.meter_no
    
class reminderWA(models.Model):
    id = models.AutoField(primary_key=True)
    meter_no = models.IntegerField(default=0)
    cus_username = models.CharField(max_length=50, unique=True)
    phone_no = models.CharField(max_length=50, unique=True)
    message = models.CharField(max_length=100)
    reminder_date = models.DateField()
    #reminder_date = models.DateTimeField(auto_now=False, auto_now_add=False, default="")
    cus_status = models.CharField(max_length=50,  default="pending")
    
    def __str__(self):
        return self.cus_username   
     
class reminderEmail(models.Model):
    id = models.AutoField(primary_key=True)
    meter_no = models.IntegerField(default=0)
    cus_username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50)
    message = models.CharField(max_length=100)
    reminder_date = models.DateField()
    #reminder_date = models.DateTimeField(auto_now=False, auto_now_add=False, default="")
    cus_status = models.CharField(max_length=50,  default="pending")
    
    def __str__(self):
        return self.cus_username  
    
class amountCollection(models.Model):
    id = models.AutoField(primary_key=True)
    meter_no = models.IntegerField(default=0)
    cus_year = models.IntegerField(default=0)
    cus_month = models.CharField(max_length=20)
    cus_amount = models.IntegerField(default=0)
    total_Collection = models.IntegerField(default=0)
    cus_status = models.CharField(max_length=50,  default="pending")

    def __str__(self):
        return self.meter_no       
    