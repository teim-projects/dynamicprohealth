from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout , admin



# Create your views here.


def index(request):
    return render(request, 'index.html')


def admin_login(request):

    if request.method=="GET":
        return render(request ,'admin_login.html')
    
    else:
        uname=request.POST['uname']
        upass=request.POST['upass']

        u=authenticate(username = uname , password = upass)

        if u is not None:

            login(request,u)
            return render(request , "index.html")
            

        else:

            context ={}
            context ['msg1'] ='Wrong Username Or Password'
            return render(request , "admin_login.html" , context)
     

from django.contrib.auth.models import Group

def create_groups():
    groups = ["Customer", "Service Provider"]
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)

# Call this function when the app starts or in your signup view
create_groups()


from django.http import JsonResponse
from django.contrib.auth.models import User

def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username=username).exists()
    }
    return JsonResponse(data)



from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages

def signup(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        uemail = request.POST.get('uemail')
        upass = request.POST.get('upass')
        cpass = request.POST.get('cpass')
        user_type = request.POST.get('user_type')


         # Check if username already exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return render(request, "signup.html")

        # Check if passwords match
        if upass != cpass:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        # Create user
        user = User.objects.create_user(username=uname, email=uemail, password=upass)

        # Assign user to the appropriate group based on selection
        if user_type == "customer":
            group = Group.objects.get(name="Customer")
        elif user_type == "service_provider":
            group = Group.objects.get(name="Service Provider")

        # Add user to the group
        user.groups.add(group)
        messages.success(request, "Signup successful. You can now log in.")
        return redirect("/login")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        uname = request.POST['uname']
        upass = request.POST['upass']

        # Handle hardcoded admin login
        if uname == 'admin1' and upass == '123':
            # Check if the admin user exists in the database
            admin_user = User.objects.filter(username=uname).first()
            if admin_user:
                # Log in the admin user
                login(request, admin_user)
                return render(request, "admin_dashboard.html")
            else:
                # Create the admin user if it doesn't exist
                admin_user = User.objects.create_superuser(username=uname, email='admin@example.com', password=upass)
                login(request, admin_user)
                return render(request, "admin_dashboard.html")

        # Handle customer or service provider login
        user = authenticate(username=uname, password=upass)
        if user:
            # Check if user is a customer or service provider
            if user.groups.filter(name="Customer").exists():
                login(request, user)
                return render(request, "customer_dashboard.html")
            elif user.groups.filter(name="Service Provider").exists():
                login(request, user)
                return render(request, "service_provider_dashboard.html")
        else:
            return render(request, 'login.html', {'msg1': 'Wrong Username Or Password'})

    return render(request, 'login.html')






from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ServiceProviderProfile, Service, Appointment, Payment, Feedback

from django.db.models import Sum

def service_provider_dashboard(request):
    profile = ServiceProviderProfile.objects.get(user=request.user)
    services = Service.objects.filter(provider=profile)
    appointments = Appointment.objects.filter(service__provider=profile)
    payments = Payment.objects.filter(appointment__service__provider=profile)
    feedbacks = Feedback.objects.filter(appointment__service__provider=profile)

    # Calculate total earnings
    total_earnings = payments.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'profile': profile,
        'services': services,
        'appointments': appointments,
        'payments': payments,
        'feedbacks': feedbacks,
        'total_earnings': total_earnings,
    }
    return render(request, 'service_provider_dashboard.html', context)




from datetime import timedelta
def manage_services(request):
    try:
        profile = ServiceProviderProfile.objects.get(user=request.user)
        services = Service.objects.filter(provider=profile).all()  # Update here
    except ServiceProviderProfile.DoesNotExist:
        services = []  # If the profile does not exist

    errors = []
    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        hours = request.POST.get('hours')
        minutes = request.POST.get('minutes')

        if service_name and description and price:
            Service.objects.create(
                service_name=service_name,
                description=description,
                price=price,
                duration_hours=hours,
                duration_minutes=minutes,
                provider=profile  # Update here
            )
            return redirect('manage_services')

        errors.append("All fields are required.")

    return render(request, 'manage_services.html', {'services': services, 'errors': errors})



from django.shortcuts import get_object_or_404, redirect
from .models import Service

def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == "POST":
        service.delete()
        return redirect('manage_services')  # Replace with the URL name to redirect after deletion
    return render(request, 'manage_services.html', {'service': service})



def manage_appointments(request):
    profile = ServiceProviderProfile.objects.get(user=request.user)
    appointments = Appointment.objects.all()  # Fetch all appointments
    return render(request, 'manage_appointments.html', {'appointments': appointments})

def manage_payments(request):
    profile = ServiceProviderProfile.objects.get(user=request.user)
    payments = Payment.objects.filter(appointment__service__provider=profile)
    return render(request, 'manage_payments.html', {'payments': payments})

def view_feedback(request):
    profile = ServiceProviderProfile.objects.get(user=request.user)
    feedbacks = Feedback.objects.filter(appointment__service__provider=profile)
    return render(request, 'view_feedback.html', {'feedbacks': feedbacks})

from django.shortcuts import render, redirect, get_object_or_404
from .models import ServiceProviderProfile

def create_service_provider_profile(request):
    if request.method == 'POST':
        # Handle file upload and other form data
        profile_picture = request.FILES.get('profile_picture')
        expertise_area = request.POST.get('expertise_area')
        bio = request.POST.get('bio')
        availability = request.POST.get('availability')
        contact_info = request.POST.get('contact_info')

        # Check if profile exists for the current user
        profile, created = ServiceProviderProfile.objects.get_or_create(user=request.user)
        
        # Update or create profile with new data
        profile.profile_picture = profile_picture if profile_picture else profile.profile_picture
        profile.expertise_area = expertise_area
        profile.bio = bio
        profile.availability = availability
        profile.contact_info = contact_info
        profile.save()

        return redirect('profile_view')  # Redirect to profile view after saving
    else:
        # Display the profile creation form
        return render(request, 'service_provider_create_profile.html')

def profile_view(request):
    # Fetch the current user's profile
    profile = get_object_or_404(ServiceProviderProfile, user=request.user)
    return render(request, 'service_provider_profile.html', {'profile': profile})






from .models import CustomerProfile, CustomerService, CustomerAppointment, CustomerPayment, CustomerReview
from django.utils import timezone




# @login_required
def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')

# @login_required
def customer_manage_profile(request):
    profile = CustomerProfile.objects.get(user=request.user)
    if request.method == 'POST':
        # Handle profile update here
        pass
    return render(request, 'customer_manage_profile.html', {'profile': profile})

# @login_required
def customer_search_services(request):
    services = CustomerService.objects.all()
    return render(request, 'customer_search_services.html', {'services': services})

# @login_required
def customer_book_appointments(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        appointment_date = request.POST.get('appointment_date')
        service = CustomerService.objects.get(id=service_id)
        CustomerAppointment.objects.create(customer=request.user, service=service, appointment_date=appointment_date)
        return redirect('customer_dashboard')
    services = CustomerService.objects.all()
    return render(request, 'customer_book_appointments.html', {'services': services})

# @login_required
def customer_make_payments(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        CustomerPayment.objects.create(customer=request.user, amount=amount, payment_date=timezone.now())
        return redirect('customer_dashboard')
    return render(request, 'customer_make_payments.html')

# @login_required
def customer_submit_reviews(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')
        service = CustomerService.objects.get(id=service_id)
        CustomerReview.objects.create(customer=request.user, service=service, review_text=review_text, rating=rating)
        return redirect('customer_dashboard')
    services = CustomerService.objects.all()
    return render(request, 'customer_submit_reviews.html', {'services': services})





from django.shortcuts import render, get_object_or_404
from .models import Service  # Assuming you have a Service model

def health_services(request):
    services = Service.objects.filter(service_name='Health')
    return render(request, 'health.html', {'services': services})

def diet_services(request):
    services = Service.objects.filter(service_name='Diet')
    return render(request, 'diet.html', {'services': services})

def fitness_services(request):
    services = Service.objects.filter(service_name='Fitness')
    return render(request, 'fitness.html', {'services': services})


def book_appointment(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        # Validate appointment_date as needed
        
        # Create an appointment
        Appointment.objects.create(
            customer=request.user,
            service=service,
            date_time=appointment_date,
            status='Pending'
        )
        messages.success(request, "Appointment booked successfully.")
        return redirect('customer_dashboard')  # Redirect to dashboard or another success page
    return render(request, 'book_appointment.html', {'service': service})




from django.views.decorators.http import require_POST
from .models import Appointment

@require_POST
def accept_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.status = "Accepted"
    appointment.save()
    return redirect('manage_appointments')

@require_POST
def reject_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    reason = request.POST.get('reason')
    # You can save the reason for rejection here if needed
    appointment.status = "Rejected"
    appointment.save()
    return redirect('manage_appointments')