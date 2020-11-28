from django.shortcuts import render, redirect
from django.contrib import messages, auth
from contacts.models import Contact
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':

        #get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #username validation
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken! Please use different one')
            return redirect('register')
        else:
            #email validation
            if User.objects.filter(email=email).exists():
                messages.error(request, 'email is already registered! Please use different one')
                return redirect('register')
            else:
                #password validation
                if password != password2:
                    messages.error(request, 'passwords do not match')
                    return redirect('register')
                else:
                    #creating user
                    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                    
                    '''#login after register
                    auth.login(request, user)
                    messages.success(request, 'you are logged successfully')
                    return redirect('index')'''

                    user.save()
                    messages.success(request, 'Registration is successful')
                    return redirect('login')

    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Logged out')
        return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }

    return render(request, 'accounts/dashboard.html', context)