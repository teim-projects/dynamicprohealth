from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path , include
from DPHapp import views

urlpatterns = [
    path('', views.index),
    path('admin_login', views.admin_login),
    path('login', views.login_view),
    path('signup', views.signup),
    path('check-username/', views.check_username, name='check_username'),  # Add this line


    # path('service_provider_login', views.service_provider_login),
    # path('service_provider_signup', views.service_provider_signup),
     path('dashboard', views.service_provider_dashboard, name='service_provider_dashboard'),
    path('manage-services', views.manage_services, name='manage_services'),
    path('manage-appointments', views.manage_appointments, name='manage_appointments'),
    path('manage-payments', views.manage_payments, name='manage_payments'),
    path('view-feedback', views.view_feedback, name='view_feedback'),
    path('create-profile', views.create_service_provider_profile, name='create_service_provider_profile'),
    path('service_provider_profile', views.profile_view, name='profile_view'),
    # path('customer_login/', views.customer_login, name='customer_login'),
    # path('customer_signup/', views.customer_signup, name='customer_signup'), 
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('manage_profile/', views.customer_manage_profile, name='customer_manage_profile'),
    path('search_services/', views.customer_search_services, name='customer_search_services'),
    path('book_appointments/', views.customer_book_appointments, name='customer_book_appointments'),
    path('make_payments/', views.customer_make_payments, name='customer_make_payments'),
    path('submit_reviews/', views.customer_submit_reviews, name='customer_submit_reviews'),
    path('delete-service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('health', views.health_services, name='health_services'),
    path('diet', views.diet_services, name='diet_services'),
    path('fitness', views.fitness_services, name='fitness_services'),
    path('book-appointment/<int:service_id>/', views.book_appointment, name='book_appointment'),
    path('accept-appointment/<int:appointment_id>/', views.accept_appointment, name='accept_appointment'),
    path('reject-appointment/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),


]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)