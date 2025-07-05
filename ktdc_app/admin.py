from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin

class UserModel(UserAdmin):
    list_display = ['aadhar_id','username','employee_id','user_type','mobile_no']

admin.site.register(User,UserModel)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Hod)
admin.site.register(Grievance)