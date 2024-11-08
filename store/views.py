from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Category, Profile
from cart.models import UserCart
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UpdateProfileForm
import json

def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

def category(request, slug):
    cat = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=cat)
    return render(request, 'category.html', {'products': products, 'category': cat})

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            r = request.POST.get('r', 'home')
            login(request, user=user)
            messages.success(request, "Logged in successfully")
            return redirect(r)
        else:
            messages.error(request, 'Failed to log in')
            return render(request, 'login.html', {'r': request.POST.get('r', 'home')})
    
    return render(request, 'login.html', {'r': request.GET.get('r', 'home')})

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "User info updated successfully")
            return redirect('update_user')
    
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        return redirect('home')

def update_user_info(request):
    if request.user.is_authenticated:
        current_profile = Profile.objects.get(user__id=request.user.id)
        profile_form = UpdateProfileForm(request.POST or None, instance=current_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile info updated successfully")
            return redirect('update_user_info')
    
        return render(request, 'update_user_info.html', {'profile_form': profile_form})
    else:
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been successfully updated")
                user = authenticate(request, username=current_user.username, password=request.POST.get('new_password1'))
                login(request, user)
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    
    return redirect('home')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        r = request.POST.get('r', 'update_user_info')
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            cart = request.session.get('session_key')
            user_cart = UserCart.objects.create(user=User.objects.get(id=request.user.id), cart=json.dumps(cart))
            user_cart.save()

            messages.success(request, 'Registered Successfully!!')
            return redirect(r)
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return render(request, 'register.html', {'form': form, 'r': r})
            
    form = SignUpForm()
    return render(request, 'register.html', {'form': form, 'r': request.GET.get('r', 'update_user_info')})


def search(request):
    s = request.GET.get('s')
    if s is None:
        return render(request, 'search.html', {'s': ''})
    results = Product.objects.filter(name__contains=s) | Product.objects.filter(description__icontains=s)
    return render(request, 'search.html', {'results': results, 's': s})