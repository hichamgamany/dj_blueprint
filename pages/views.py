from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail
from blog.models import Post


def home_view(request):
    queryset = Post.objects.filter(published=True).order_by('-created')
    title = 'Home Page'
    template_name = 'home.html'
    context = {
        'title': title,
        'posts': queryset
    }
    return render(request, template_name, context)


def contact_view(request):
    title = 'Contact page'
    template_name = 'contact.html'
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)

        # form validation
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # create record in database
            contact = Contact()
            contact.first_name = first_name
            contact.last_name = last_name
            contact.email = email
            contact.message = message
            contact.save()

            # notification
            messages.success(request, f'''
            Thank you, your message has been sent successfully.
            ''')

            # sending email
            subject = 'Message received'
            message = f'''
            Your message has been received, we will get back to you soon.\n
            -------------------------------------------------------------
            Your message: "{contact.message}"\n
                        '''
            from_email = 'no-reply@youremail.com'
            recipient_list = [contact.email]
            send_mail(subject, message, from_email, recipient_list)
            return redirect('contact_email_received')
        else:
            messages.error(request, f'''
            All the fields are required and must be valid ! please try again
            ''', extra_tags='danger')

    context = {
        'form': form,
        'title': title
    }
    return render(request, template_name, context)


def contact_email_received(request):
    title = 'Email Received'
    template_name = 'contact_form_email_received.html'
    context = {
        'title': title
    }
    return render(request, template_name, context)
