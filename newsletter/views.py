# subscribers/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mass_mail
from blog.models import Subscriber
from .forms import NewsletterForm
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt




from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_active and u.is_superuser)(view_func)

@admin_required
def send_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = 'youremail@example.com'  # update this

            recipient_list = list(Subscriber.objects.values_list('email', flat=True))
            if recipient_list:
                messages_to_send = [(subject, message, from_email, [email]) for email in recipient_list]
                send_mass_mail(messages_to_send, fail_silently=False)
                messages.success(request, 'Newsletter sent successfully.')
            else:
                messages.warning(request, 'No subscribers found.')
            return redirect('send_newsletter')
    else:
        form = NewsletterForm()
    return render(request, 'newsletter/send_newsletter.html', {'form': form})
