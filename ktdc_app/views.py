from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ktdc_app.models import User,Department,Employee,Hod,Grievance
from django.utils import timezone


# Create your views here.

def index1(request):
    return render(request,'index1.html')

def base(request):
    return render(request,'base.html')

def login(request):
    return render(request,'login.html')

def dologin(request):
    if request.method == 'POST':
        aadhar_id = request.POST.get('aadhar_id')
        password = request.POST.get('password')

        user = auth.authenticate(aadhar_id=aadhar_id,password=password)
        if user != None:
            auth.login(request,user)
            user_type = user.user_type
            if user_type == 'IT ADMIN':
                return redirect('it_admin_home')
            elif user_type == 'MANAGING DIRECTOR':
                pass
            elif user_type == 'DEPARTMENT HEAD':
                return redirect('hod_home')
            elif user_type == 'EMPLOYEE':
                return redirect('employee_home')
            else:
                messages.info(request,'Aadhar id or Password is Wrong')
                return redirect('login')
        else:
            messages.info(request,'Aadhar id or Password is Wrong')
            return redirect('login') 
    return render(request,'login.html')


def logout(request):
    auth.logout(request)
    return redirect('index1')


@login_required(login_url='/')
def it_admin_home(request):
    department = Department.objects.all()
    employee = Employee.objects.all()

    dept = Department.objects.all().count()
    hod = Hod.objects.all().count()
    emp = Employee.objects.all().count()
    grv = Grievance.objects.all().count()


    e = Employee.objects.all().order_by('-created_at')[:6]
    h = Hod.objects.all().order_by('-created_at')[:6]


    DEPTID = request.GET.get('department')
    if DEPTID:
        employee = Employee.objects.filter(department_id = DEPTID)
    else:    
        employee = Employee.objects.all()
    context = {
        'department':department,
        'employee':employee,
        'dept': dept,
        'hod': hod,
        'emp': emp,
        'grv': grv,
        'e': e,
        'h': h
    }
    return render(request,'it_admin/it_admin_home.html',context)

@login_required(login_url='/')
def profile(request):
    user = User.objects.get(id=request.user.id)
    context = {
        'user':user
    }
    return render(request,'profile.html',context)


@login_required(login_url='/')
def profile_update(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')

        try:
            user = User.objects.get(id=request.user.id)

            user.profile_pic = profile_pic
            if profile_pic != None and profile_pic != '':
                user.profile_pic = profile_pic
            user.save()
            messages.info(request,'Profile updated successfully')
            return redirect('profile')

        except:
            messages.info(request,'Failed to update profile pic')
            return redirect('it_admin_profile_update')    
    return render(request,'profile.html')


@login_required(login_url='/')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = User.objects.get(id=request.user.id)

        if user.check_password(current_password) and new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            return redirect("login")
        else:
            messages.info(request,"Pervious Password Not Match")
            return redirect("change_password")    

         
    return render(request,'change_password.html')


@login_required(login_url='/')
def add_department(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if Department.objects.filter(name=name).exists():
            messages.info(request,'Department Already Exist')
            return redirect('add_department')
        else:
            department = Department(
                name = name
            )
            department.save()
            messages.info(request,'Department added successfully')
            return redirect('add_department')
    return render(request,'it_admin/add_department.html')


@login_required(login_url='/')
def view_department(request):
    department = Department.objects.all()
    context = {
        'department':department
    }
    return render(request,'it_admin/view_department.html',context)


@login_required(login_url='/')
def edit_department(request,id):
    department = Department.objects.get(id=id)
    context = {
        'department':department
    }
    return render(request,'it_admin/edit_department.html',context)


@login_required(login_url='/')
def update_department(request):
    if request.method == 'POST':
        name = request.POST.get('name')  
        department_id = request.POST.get('department_id')

        department = Department.objects.get(id=department_id)
        if Department.objects.filter(name=name).exists():
            messages.info(request,'Department Already Exist')
            return redirect('update_department')
        else:

            department.name = name
            department.save()
            messages.info(request,'Department updated successfully')
            return redirect('view_department')
    return render(request,'it_admin/edit_department.html')


@login_required(login_url='/')
def delete_department(request,id):
    department = Department.objects.get(id=id)
    department.delete()
    messages.info(request,'Department successfully deleted')
    return redirect('view_department') 


@login_required(login_url='/')
def add_employee(request):
    department = Department.objects.all()
    context = {
        'department':department
    }

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name =  request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        aadhar_id = request.POST.get('aadhar_id')
        employee_id = request.POST.get('employee_id')
        gender = request.POST.get('gender')
        department_id = request.POST.get('department_id')
        mobile_no = request.POST.get('mobile_no')
        

        if User.objects.filter(aadhar_id=aadhar_id).exists():
            messages.info(request,'Aadhar ID is taken')
            return redirect('add_employee')
        elif User.objects.filter(employee_id=employee_id).exists():   
            messages.info(request,'Employee ID taken') 
            return redirect('add_employee') 
        elif User.objects.filter(mobile_no=mobile_no).exists():   
            messages.info(request,'Phone Number taken') 
            return redirect('add_employee')
        elif User.objects.filter(email=email).exists():   
            messages.info(request,'Email taken') 
            return redirect('add_employee')
        elif User.objects.filter(username=username).exists():   
            messages.info(request,'Username taken') 
            return redirect('add_employee')
        else:
            user = User(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                aadhar_id = aadhar_id,
                employee_id = employee_id,
                mobile_no = mobile_no,
                profile_pic = profile_pic,
                user_type = 'EMPLOYEE'
            )   
            user.set_password(password)
            user.save()

            department = Department.objects.get(id=department_id)
            employee = Employee(
                admin = user,
                department_id = department,
                
                gender = gender
            )
            employee.save()
            messages.info(request,'Details are successfully saved') 
            return redirect('add_employee')
                
                
    return render(request,'it_admin/add_employee.html',context)


def view_employee(request):
    department = Department.objects.all()
    employee = Employee.objects.all()

    DEPTID = request.GET.get('department')
    if DEPTID:
        employee = Employee.objects.filter(department_id = DEPTID)
    else:    
        employee = Employee.objects.all()
    context = {
        'department':department,
        'employee':employee
    }

  
    return render(request,'it_admin/view_employee.html',context)


@login_required(login_url='/')
def edit_employee(request,id):
    employee = Employee.objects.filter(id=id)
    department = Department.objects.all()
    context = {
        'employee':employee,
        'department':department
    }
    return render(request,'it_admin/edit_employee.html',context)



@login_required(login_url='/')
def update_employee(request):

    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name =  request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        aadhar_id = request.POST.get('aadhar_id')
        employee_id = request.POST.get('employee_id')
        gender = request.POST.get('gender')
        department_id = request.POST.get('department_id')
        mobile_no = request.POST.get('mobile_no')

        user = User.objects.get(id=emp_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.aadhar_id = aadhar_id
        user.employee_id = employee_id
        user.mobile_no = mobile_no
        if password != None and password !='':
            user.set_password(password)
        if profile_pic != None and profile_pic !='':
            user.profile_pic = profile_pic

        user.save()

        employee = Employee.objects.get(admin=emp_id)
        employee.gender = gender

        department = Department.objects.get(id=department_id)
        employee.department_id = department
        employee.save()
        messages.info(request,'Details updated successfully')
        return redirect('view_employee')

    return render(request,'it_admin/edit_employee.html')


@login_required(login_url='/')
def delete_employee(request,admin):
    employee = User.objects.get(id=admin)
    employee.delete()
    messages.info(request,'Details are successfully deleted')
    return redirect('view_employee')


@login_required(login_url='/')
def add_hod(request):
    department = Department.objects.all()
    context = {
        'department':department
    }

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name =  request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        aadhar_id = request.POST.get('aadhar_id')
        employee_id = request.POST.get('employee_id')
        gender = request.POST.get('gender')
        department_id = request.POST.get('department_id')
        mobile_no = request.POST.get('mobile_no')
        

        if User.objects.filter(aadhar_id=aadhar_id).exists():
            messages.info(request,'Aadhar ID is taken')
            return redirect('add_hod')
        elif User.objects.filter(employee_id=employee_id).exists():   
            messages.info(request,'Employee ID taken') 
            return redirect('add_hod') 
        elif User.objects.filter(mobile_no=mobile_no).exists():   
            messages.info(request,'Phone Number taken') 
            return redirect('add_hod')
        elif User.objects.filter(email=email).exists():   
            messages.info(request,'Email taken') 
            return redirect('add_hod')
        elif User.objects.filter(username=username).exists():   
            messages.info(request,'Username taken') 
            return redirect('add_hod')
        else:
            user = User(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                aadhar_id = aadhar_id,
                employee_id = employee_id,
                mobile_no = mobile_no,
                profile_pic = profile_pic,
                user_type = 'DEPARTMENT HEAD'
            )   
            user.set_password(password)
            user.save()

            department = Department.objects.get(id=department_id)
            hod = Hod(
                admin = user,
                department_id = department,
                
                gender = gender
            )
            hod.save()
            messages.info(request,'Details are successfully saved') 
            return redirect('add_hod')
    return render(request,'it_admin/add_hod.html',context)


@login_required(login_url='/')
def view_hod(request):
    hod = Hod.objects.all()
    context = {
        'hod':hod
    }
    return render(request,'it_admin/view_hod.html',context)


@login_required(login_url='/')
def edit_hod(request,id):
    hod = Hod.objects.filter(id=id)
    department = Department.objects.all()
    context = {
        'hod':hod,
        'department':department
    }
    return render(request,'it_admin/edit_hod.html',context)


@login_required(login_url='/')
def update_hod(request):
    if request.method == 'POST':
        hod_id = request.POST.get('hod_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name =  request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        aadhar_id = request.POST.get('aadhar_id')
        employee_id = request.POST.get('employee_id')
        gender = request.POST.get('gender')
        department_id = request.POST.get('department_id')
        mobile_no = request.POST.get('mobile_no')

        user = User.objects.get(id=hod_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.aadhar_id = aadhar_id
        user.employee_id = employee_id
        user.mobile_no = mobile_no
        if password != None and password !='':
            user.set_password(password)
        if profile_pic != None and profile_pic !='':
            user.profile_pic = profile_pic

        user.save()

        hod = Hod.objects.get(admin=hod_id)
        hod.gender = gender

        department = Department.objects.get(id=department_id)
        hod.department_id = department
        hod.save()
        messages.info(request,'Details updated successfully')
        return redirect('view_hod')
    return render(request,'it_admin/edit_hod.html')


@login_required(login_url='/')
def delete_hod(request,admin):
    hod = User.objects.get(id=admin)
    hod.delete()
    messages.info(request,'Details are successfully deleted')
    return redirect('view_hod')


def employee_home(request):
    e = Employee.objects.filter(admin=request.user.id).first()
    emp = Employee.objects.filter(admin=request.user.id)
    for i in emp:
       emp_id = i.id
       emp_grv_history = Grievance.objects.filter(employee=emp_id).order_by('-created_at')
       total_grv_count = emp_grv_history.count()
       pending_grv_count = emp_grv_history.filter(status=0).count()
       in_progress_grv_count = emp_grv_history.filter(status=1).count()
       solved_grv_count = emp_grv_history.filter(status=2).count()
       pending_grv_count1 = emp_grv_history.filter(status=0).order_by('-created_at')[:6]
       in_progress_grv_count1 = emp_grv_history.filter(status=1).order_by('-created_at')[:6]
       

       context = {
           'emp_grv_history':emp_grv_history,
           'total_grv_count':total_grv_count,
           'pending_grv_count':pending_grv_count,
           'in_progress_grv_count':in_progress_grv_count,
           'solved_grv_count':solved_grv_count,
           'pending_grv_count1':pending_grv_count1,
           'in_progress_grv_count1':in_progress_grv_count1,
           'e':e
           
       }
  
    return render(request,'Employee/employee_home.html',context)


def grievance(request):
   
   emp = Employee.objects.filter(admin=request.user.id)
   for i in emp:
       emp_id = i.id
       emp_grv_history = Grievance.objects.filter(employee=emp_id).order_by('-created_at')
       total_grv_count = emp_grv_history.count()
       context = {
           'emp_grv_history':emp_grv_history,
           'total_grv_count':total_grv_count,
       }
   
   if request.method == 'POST':
       subject = request.POST.get('subject')
       message = request.POST.get('message')
       
       pic = request.FILES.get('pic')
       pdf = request.FILES.get('pdf')
       voice_recorder = request.FILES.get('voice_recorder')
       employee = Employee.objects.get(admin=request.user.id)
       hod = Hod.objects.get(department_id=employee.department_id)

       grievance = Grievance(
           employee = employee,
           hod = hod,
           subject = subject,
           message = message,
           pic = pic,
           pdf = pdf,
           voice_recorder = voice_recorder
           

        )
       grievance.save()
       messages.info(request,'Grievance Successfully Send')
       return redirect('grievance')

    
   return render(request,'Employee/grievance.html',context)






def grievance_view(request,grievance_id):
    grievance = get_object_or_404(Grievance, id=grievance_id)
    context = {
        'grievance':grievance
    }
    return render(request, 'Employee/grievance_view.html', context)


def hod_home(request):
    h = Hod.objects.filter(admin=request.user.id).first()
    admin=request.user.id
    hod = Hod.objects.get(admin=admin)
    grievance = hod.head_grievances.order_by('-created_at')
    grv = hod.head_grievances.order_by('-created_at')[:6]
    total_grievances = grievance.count()

    grievance.status = 0
    grievance.status = 1
    grievance.status = 2
    
    pending_count = grievance.filter(status=0).count()
    inprogress_count = grievance.filter(status=1).count()
    solved_count = grievance.filter(status=2).count()
    pend_count = grievance.filter(status=0).order_by('-created_at')[:6]
    inpog_count = grievance.filter(status=1).order_by('-created_at')[:6]
    
    

    context = {
        'grievance': grievance,
        'total_grievances': total_grievances,
        'inprogress_count':inprogress_count,
        'pending_count':pending_count,
        'solved_count':solved_count,
        'grv':grv,
        'pend_count':pend_count,

        'inpog_count':inpog_count,
        'h':h

    }
    return render(request,'Hod/hod_home.html',context)


'''def view_grievance(request):
    admin=request.user.id
    hod = Hod.objects.get(admin=admin)
    grievance = hod.head_grievances.order_by('-created_at')

     
    pending = grievance.filter(status=0)
    inprogress = grievance.filter(status=1)
    solved = grievance.filter(status=2)
    
    context = {
        'grievance':grievance,
        'inprogres':inprogress,
        'pending':pending,
        'solved':solved,
        
    }
    return render(request,'Hod/view_grievance.html',context)'''



def view_grievance(request):
    admin=request.user.id
    hod = Hod.objects.get(admin=admin)
    grievance = hod.head_grievances.order_by('-created_at')

    status_filter = request.GET.get('status', 'all')
    if status_filter == 'pending':
        grievance = grievance.filter(status=0)
    elif status_filter == 'inprogress':
        grievance = grievance.filter(status=1)
    elif status_filter == 'solved':
        grievance = grievance.filter(status=2)

    context = {
        'grievance':grievance,
        'status_filter': status_filter,
    }
    return render(request,'Hod/view_grievance.html',context)








'''def full_message(request,grievance__id):
    grievance = Grievance.objects.get(id=grievance__id)

    if request.method == 'POST':
       grv_id = request.POST.get('grv_id')
       message_reply = request.POST.get('message_reply') 

       msg_reply = Grievance.objects.get(id=grv_id)
       msg_reply.message_reply = message_reply
       msg_reply.save()
       messages.info(request,'Reply Successfully Send')
       return redirect('view_grievance')

    context = {
        'grievance':grievance
    }
    return render(request,'Hod/full_message.html',context) '''


def full_message(request,grievance__id):
    grievance = Grievance.objects.get(id=grievance__id)
    hod = Hod.objects.exclude(id=request.user.hod.id)

    if request.method == 'POST':
       grv_id = request.POST.get('grv_id')
       message_reply = request.POST.get('message_reply') 
       msg_reply = Grievance.objects.get(id=grv_id)
       msg_reply.message_reply = message_reply
       msg_reply.message_reply_time = timezone.now()
       msg_reply.save()
       messages.info(request,'Reply Successfully Send')
       return redirect('view_grievance')

    context = {
        'grievance':grievance,
        'hod':hod
    }
    return render(request,'Hod/full_message.html',context)

def grievance_inprogress(request, id):
    grievance = Grievance.objects.get(id=id)
    grievance.status = 1
    grievance.save()
    return redirect('view_grievance')


def grievance_solved(request, id):
    grievance = Grievance.objects.get(id=id)
    grievance.status = 2
    grievance.save()
    return redirect('view_grievance')


def forward_grievance(request):
    return render(request,'HOD/forward_grievance.html')
    





   
   
