from django.db import models
from django.contrib.auth.models import AbstractUser
from . manager import UserManager
from django.core.validators import RegexValidator

# Create your models here.

aadhar_id_validator = RegexValidator(
    '^[2-9]{1}[0-9]{3}\\s[0-9]{4}\\s[0-9]{4}$',
    'Enter as shown in your aadhar card'
)



class User(AbstractUser):

    USER = (
        ('IT ADMIN','IT ADMIN'),
        ('MANAGING DIRECTOR','MANAGING DIRECTOR'),
        ('DEPARTMENT HEAD','DEPARTMENT HEAD'),
        ('EMPLOYEE','EMPLOYEE')
    )


    aadhar_id = models.CharField(max_length=20,unique=True,validators=[aadhar_id_validator])
    user_type = models.CharField(choices=USER,max_length=50,default='IT ADMIN')
    profile_pic = models.ImageField(upload_to='media/images')
    employee_id = models.CharField(max_length=50,unique=True)
    mobile_no = models.CharField(max_length=30)


    USERNAME_FIELD = 'aadhar_id'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Department(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    

class Employee(models.Model):
    admin = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=100)
    department_id = models.ForeignKey(Department,on_delete=models.CASCADE)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    
    def __str__(self):
        return self.admin.first_name + ' ' + self.admin.last_name
    

class Hod(models.Model):
    admin = models.OneToOneField(User,on_delete=models.CASCADE)
    
    gender = models.CharField(max_length=100)
    department_id = models.ForeignKey(Department,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.admin.first_name + ' ' + self.admin.last_name   


class Grievance(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)   
    hod =  models.ForeignKey(Hod,on_delete=models.CASCADE,related_name='head_grievances')
    forwarded_to = models.ForeignKey(Hod,on_delete=models.CASCADE,related_name='forwarded_grievances',null=True,blank=True)
    remarks = models.TextField(null=True, blank=True)
    subject = models.CharField(max_length=400)
    message = models.TextField()
    message_reply = models.TextField(null=True)
    message_reply_time = models.DateTimeField(null=True)
    pic = models.ImageField(upload_to='pic')
    pdf = models.FileField(upload_to='pdf', null=True, blank=True)
    voice_recorder = models.FileField(upload_to='voice_recording', null=True, blank=True)
    
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    

    def __str__(self):
        
        return self.employee.admin.first_name + ' ' + self.employee.admin.last_name  







