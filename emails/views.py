from django.shortcuts import render,redirect, get_object_or_404
from .forms import *
from django.conf import settings
from dataentry.utils import send_email_notification
from django.contrib import messages
from django.db.models import Sum
from .models import *
from .tasks import *

# Create your views here.


def send_email(request):
    if request.method=='POST':
        email_form = EmailForm(request.POST,request.FILES)
        if email_form.is_valid():
            email = email_form.save()
            # Send an email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            # to_email = settings.DEFAULT_TO_EMAIL
            email_list = email.email_list
            
            subscribers = Subscriber.objects.filter(email_list=email_list)

            to_email = [email.email_address for email in subscribers]
            
            if email.attachment:
                attachment = email.attachment.path
            else:
                attachment = None
            send_email_task.delay(mail_subject,message, to_email,attachment)
            
                
            
            messages.success(request,"Email sent succesfully!")
            return redirect('send_email')
    else:
        email_form = EmailForm()
        context = {
            'email_form':email_form
        }
    return render(request,'emails/send-email.html',context)

def track_click(request):
    return

def track_open(request):
    return

def track_dashboard(request):
    emails = Email.objects.all().annotate(total_sent=Sum('sent__total_sent')).order_by('-sent_at')
    
    context = {
        'emails': emails,
    }
    return render(request, 'emails/track_dashboard.html', context)

def track_stats(request, pk):
    email = get_object_or_404(Email, pk=pk)
    sent = Sent.objects.get(email=email)
    context = {
        'email': email,
        'total_sent': sent.total_sent,
    }
    return render(request, 'emails/track_stats.html', context)