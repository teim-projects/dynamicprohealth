from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import User

# Service Provider Profile Model
class ServiceProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    expertise_area = models.CharField(max_length=100)
    bio = models.TextField()
    availability = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

# Service Model
class Service(models.Model):
    service_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_hours = models.IntegerField()
    duration_minutes = models.IntegerField()
    provider = models.ForeignKey(ServiceProviderProfile, on_delete=models.CASCADE)

# Appointment Model
class Appointment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(
        max_length=10, 
        choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')],
        default='Pending'  # Set the default status to 'Pending'
    )
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer.username} - {self.service.service_name} - {self.status}"


# Payment Model
class Payment(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.appointment}"

# Feedback Model
class Feedback(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField()

    def __str__(self):
        return f"Feedback by {self.appointment.customer.username} for {self.appointment.service.service_name}"



class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other profile fields as needed

class CustomerService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Add other service fields as needed

class CustomerAppointment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(CustomerService, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    # Add other appointment fields as needed

class CustomerPayment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    # Add other payment fields as needed

class CustomerReview(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(CustomerService, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField()