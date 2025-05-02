"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from mysite import views
from members import views as member_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    
    # Doctor and appointment URLs
    path('doctors/', member_views.search_doctors, name='search_doctors'),
    path('doctors/<int:doctor_id>/', member_views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:doctor_id>/book/', member_views.book_appointment, name='book_appointment'),
    path('appointments/', member_views.my_appointments, name='my_appointments'),
    path('appointments/<uuid:appointment_id>/cancel/', member_views.cancel_appointment, name='cancel_appointment'),
    path('appointments/<uuid:appointment_id>/update/', member_views.update_appointment, name='update_appointment'),
    
    # Hospital Admin URLs
    path('hospital-admin/', member_views.admin_dashboard, name='admin_dashboard'),
    path('hospital-admin/appointments/', member_views.admin_manage_appointments, name='admin_manage_appointments'),
    path('hospital-admin/appointments/<uuid:appointment_id>/', member_views.admin_appointment_detail, name='admin_appointment_detail'),
    path('hospital-admin/appointments/<uuid:appointment_id>/edit/', member_views.admin_edit_appointment, name='admin_edit_appointment'),
    path('hospital-admin/appointments/<uuid:appointment_id>/update/', member_views.admin_update_appointment, name='admin_update_appointment'),
    path('hospital-admin/appointments/<uuid:appointment_id>/status/', member_views.admin_update_appointment_status, name='admin_update_appointment_status'),
    path('hospital-admin/appointments/<uuid:appointment_id>/delete/', member_views.admin_delete_appointment, name='admin_delete_appointment'),
    path('hospital-admin/doctors/', member_views.admin_doctors_list, name='admin_doctors_list'),
    path('hospital-admin/doctors/add/', member_views.admin_add_doctor, name='admin_add_doctor'),
    path('hospital-admin/doctors/<int:doctor_id>/edit/', member_views.admin_edit_doctor, name='admin_edit_doctor'),
    path('hospital-admin/doctors/<int:doctor_id>/delete/', member_views.admin_delete_doctor, name='admin_delete_doctor'),
    path('hospital-admin/specialities/', member_views.admin_specialities, name='admin_specialities'),
    path('hospital-admin/specialities/add/', member_views.admin_add_speciality, name='admin_add_speciality'),
    path('hospital-admin/specialities/<int:speciality_id>/edit/', member_views.admin_edit_speciality, name='admin_edit_speciality'),
    path('hospital-admin/specialities/<int:speciality_id>/delete/', member_views.admin_delete_speciality, name='admin_delete_speciality'),
]
