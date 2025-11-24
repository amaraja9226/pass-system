from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

#home page 


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Signup Viewfrom django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Combined Login & Signup View
def auth_view(request):
    message = ""
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "signup":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")

            if password != password2:
                message = "Passwords do not match."
            elif User.objects.filter(username=username).exists():
                message = "Username already taken."
            elif User.objects.filter(email=email).exists():
                message = "Email already registered."
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # Auto-login after signup
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('home')
                else:
                    message = "Something went wrong. Please login manually."

        elif action == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = "Invalid credentials."

    return render(request, 'student/auth.html', {'message': message})

# Logout
def logout_view(request):
    logout(request)
    return redirect('auth_view')

# Home Page
@login_required(login_url='auth_view')
def home(request):
    if not request.user.is_authenticated:
        return redirect('auth_view')
    return render(request, 'home.html')


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from pass_system.models import IssuePass
from django.contrib.auth.decorators import login_required

# Admin login from modal
def admin_dashboard_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Fixed admin credentials
        if username == "komal" and password == "komal01":
            request.session['is_admin'] = True
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials!")
            return redirect('home')
    return redirect('home')


# Admin dashboard view
def admin_dashboard(request):
    if not request.session.get('is_admin'):
        messages.error(request, "Access denied!")
        return redirect('home')

    applications = IssuePass.objects.all().order_by('-id')
    return render(request, "admin_dashboard.html", {"applications": applications})

# home(request):
 #   return render(request, 'home.html')


from django.shortcuts import render
from datetime import datetime, timedelta
from django.core.mail import send_mail

from django.shortcuts import render
from datetime import date, timedelta
from  pass_system.models import IssuePass

def check_pass_expiry(request):
    message = None
    expiry_info = None

    if request.method == "POST":
        issue_date_str = request.POST.get("issue_date")
        email = request.POST.get("email")

        issue_date = date.fromisoformat(issue_date_str)
        # Assuming pass duration 1 month
        expiry_date = issue_date + timedelta(days=30)

        today = date.today()

        if today > expiry_date:
            message = f"Your pass is expired on {expiry_date.strftime('%d %b')}. Renew it!"
        else:
            days_left = (expiry_date - today).days
            message = f"Your pass will expire on {expiry_date.strftime('%d %b')} ({days_left} days left)."

        # For auto-fill in Renew section
        expiry_info = {
            "expiry_date": expiry_date.strftime('%d %b'),
            "is_expired": today > expiry_date
        }

    return render(request, "home.html", {
        "message": message,
        "expiry_info": expiry_info
    })


