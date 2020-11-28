from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

from .models import Contact

def contacts(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        user_id = request.POST['user_id']
        phone = request.POST['phone']
        message = request.POST['message']

        realtor_email = request.POST['realtor_email']

        #checking the user
        if request.user.is_authenticated:
            #user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquery for this listing')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing_id=listing_id, listing=listing, name=name, email=email, user_id=user_id, phone=phone, message=message)
        contact.save()

        #sending mail
        send_mail(
            'Property Inquiry request',
            'There has been an inquiry made for '+listing+'. Please login to admin area for more details',
            'santosh.physics.ss@gmail.com',
            [realtor_email, 'santoshsai233@gmail.com'],
            fail_silently=True
        )

        messages.success(request, 'Your enquery form submitted successfully')
        return redirect('/listings/'+listing_id)