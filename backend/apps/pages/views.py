from django.shortcuts import render
from django.shortcuts import render
from .models import Contact
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect

def home(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

def privacy(request):
    return render(request, 'pages/privacy_policy.html')

def cookie(request):
    return render(request, 'pages/cookie.html')

def email_sender(request):
    return render(request, 'pages/email_sender.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')


        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        subject = f"New Contact Form Submission from {name}"
        message = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
        from_email = settings.EMAIL_HOST_USER  # Must match your SMTP user
        recipient_list = ["verify@alfalahcrafts.shop"]  # Where I want receive email

        # Send Mail
        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, "Your message has been sent successfully!")
            

            send_mail(
                subject="Thank you for contacting us",
                message=f"Hi {name},\n\nThank you for reaching out. We will get back to you soon.",
                from_email=from_email,
                recipient_list=[email],
                fail_silently=True
            )

            return redirect('contact')
        
        except Exception as e:
            print(e)
            messages.error(request, "Oops! Something went wrong. Please try again.")
   
    return render(request, 'pages/contact.html')

