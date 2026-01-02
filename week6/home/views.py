from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.utils import timezone



@login_required(login_url='login_view')
def homes(request):
    return render(request, 'homes.html')


@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('homes')

    error = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            error['field'] = "Both username and password are required"
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                user.last_login = timezone.now()
                user.save()
                login(request, user)
                return redirect('homes')
            else:
                error['invalid'] = "Invalid username or password"

    return render(request, 'login.html', {'error': error})


@never_cache
def signup_view(request):
    error = {}

    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not fullname or not username or not password or not password2:
            error['field'] = "All fields are required"

        if password != password2:
            error['password'] = "Passwords do not match"

        if len(password) < 3:
            error['password'] = "Password must be at least 6 characters"

        if User.objects.filter(username=username).exists():
            error['username'] = "Username already exists"

       
        if not error:
            user = User.objects.create_user(username=username, password=password, first_name=fullname)
            login(request, user)
            return redirect('homes')

    return render(request, 'signup.html', {'error': error})



def logout_view(request):
    logout(request)
    return redirect('login_view')



