from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 
from django.contrib.auth.views import PasswordResetView

urlpatterns = [
    path('',views.index1,name='index1'),
    path('base',views.base,name='base'),
    path('login',views.login,name='login'),
    path('dologin',views.dologin,name='dologin'),
    path('logout',views.logout,name='logout'),

    path('profile',views.profile,name='profile'),
    path('profile_update',views.profile_update,name='profile_update'),

    
    path('it_admin_home',views.it_admin_home,name='it_admin_home'),
    path('change_password',views.change_password,name='change_password'),
   
   
    path('add_department',views.add_department,name='add_department'),
    path('view_department',views.view_department,name='view_department'),
    path('edit_department/<str:id>',views.edit_department,name='edit_department'),
    path('update_department',views.update_department,name='update_department'),
    path('delete_department/<str:id>',views.delete_department,name='delete_department'),


    path('add_employee',views.add_employee,name='add_employee'),
    path('view_employee',views.view_employee,name='view_employee'),
    path('edit_employee/<str:id>',views.edit_employee,name='edit_employee'),
    path('update_employee',views.update_employee,name='update_employee'),
    path('delete_employee/<str:admin>',views.delete_employee,name='delete_employee'),


    path('add_hod',views.add_hod,name='add_hod'),
    path('view_hod',views.view_hod,name='view_hod'),
    path('edit_hod/<str:id>',views.edit_hod,name='edit_hod'),
    path('update_hod',views.update_hod,name='update_hod'),
    path('delete_hod/<str:admin>',views.delete_hod,name='delete_hod'),


    path('employee_home',views.employee_home,name='employee_home'),
    path('grievance',views.grievance,name='grievance'),
    path('grievance/<int:grievance_id>/', views.grievance_view, name='grievance_view'),


    path('hod_home',views.hod_home,name='hod_home'),
    path('view_grievance',views.view_grievance,name='view_grievance'),
    path('<int:grievance__id>/', views.full_message, name='full_message'),
    path('grievance_inprogress/<int:id>/', views.grievance_inprogress, name='grievance_inprogress'),
    path('grievance_solved/<int:id>/', views.grievance_solved, name='grievance_solved'),

    path('forward_grievance',views.forward_grievance,name='forward_grievance'),
    


]