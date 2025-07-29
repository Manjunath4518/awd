from django.shortcuts import render,redirect
from .forms import *
from django.conf import settings
from dataentry.utils import send_email_notification
from django.contrib import messages
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