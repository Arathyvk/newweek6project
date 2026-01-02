from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.utils import timezone


@never_cache
def admin_login(request):
    error = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            error['field'] = "Both username and password are required"
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_staff:  
                user.last_login = timezone.now()
                user.save()
                login(request, user)
                return redirect('user_list')
            else:
                error['invalid'] = "Invalid credentials or not an admin"

    return render(request, 'admin_login.html', {'error': error})



@never_cache
def user_list(request):
    query=request.GET.get('q')
    users=User.objects.filter(is_staff=False)
    if query:
        users=users.filter(username__icontains=query)
    return render(request,'user_list.html',{'users':users})



@never_cache
def create_admin(request):
    error = {}

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")  

        
        if not username or not email or not password or not confirm_password:
            error["field"] = "All fields are required"

        if password != confirm_password:
            error["password"] = "Passwords do not match"

        if len(password) < 3:
            error["password"] = "Password must be at least 6 characters long"

        if User.objects.filter(username=username).exists():
            error["username"] = "Username already exists"

        if User.objects.filter(email=email).exists():
            error["email"] = "Email already exists"

        if not error:
            User.objects.create_user(username=username, email=email, password=password, is_staff=True)
            messages.success(request, "Admin created successfully")
            return redirect('user_list')

    return render(request, 'create.html', {'error': error})


@never_cache
def edit_admin(request, id=None):
    if id:
        user = get_object_or_404(User, id=id)
    else:
        user = None

    if request.method == "POST":
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

      
        if password and password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect(request.path)

        if user:  
            user.username = name
            user.email = email
            if password:  
                user.set_password(password)
            user.save()
            messages.success(request, "User updated successfully!")
        else:  
            if User.objects.filter(username=name).exists():
                messages.error(request, "Username already exists!")
            else:
                user = User.objects.create(username=name, email=email)
                if password:
                    user.set_password(password)
                user.save()
                messages.success(request, "User created successfully!")

        return redirect('create_admin')  

    return render(request, 'create.html', {'user': user})


@never_cache
def delete_admin(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":  
        user.delete()
        messages.success(request, "User deleted successfully!")
        return redirect('user_list')

    return render(request, "confirm_delete.html", {"user_obj": user})


