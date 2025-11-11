from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import PassApplicationForm
from .models import PassApplication
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
import base64
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PassApplication
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib.auth import logout


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'home.html', {'error': 'Invalid credentials'})
    return redirect('home')

@login_required
def admin_dashboard(request):
    applications = PassApplication.objects.all().order_by('-application_date')
    return render(request, 'admin_dashboard.html', {'applications': applications})
    

def custom_logout(request):
     logout(request)
     return redirect('home')

#aproves application

def approve_application(request, app_id):
    app = get_object_or_404(PassApplication, id=app_id)
    app.status = "Approved"
    app.save()
    
    # Optional: email send to student
    # send_email_to_student(app.email, "Your application is approved")
    
    return redirect('admin_dashboard')


#adm,in login with home page

# -----------------------------
# Step 1: Form submit → Preview
# -----------------------------
def create_application(request):
    if request.method == 'POST':
        form = PassApplicationForm(request.POST)
        if form.is_valid():
            app = PassApplication.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                department=form.cleaned_data['department'],
                class_name=form.cleaned_data['class_name'],
                village=form.cleaned_data['village'],
                reason=form.cleaned_data['reason'],
                pass_days=form.cleaned_data['pass_days'],
                application_date=form.cleaned_data['application_date'],
                application_time=form.cleaned_data['application_time'],
                status='Pending'
            )
            return render(request, 'get_application_letter.html', {'app': app})
    else:
        form = PassApplicationForm()
    return render(request, 'create_application.html', {'form': form})


# -----------------------------
# Step 2: Download PDF
# -----------------------------
def download_application_pdf(request, app_id):
    app = get_object_or_404(PassApplication, id=app_id)
    
    html_content = render_to_string('get_application_letter.html', {'app': app})
    result = BytesIO()
    pdf_status = pisa.CreatePDF(src=html_content, dest=result)
    pdf_data = result.getvalue()
    
    if pdf_status.err:
        return HttpResponse("❌ Error generating PDF")
    
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{app.name}_BusPassApplication.pdf"'
    return response


# -----------------------------
# Step 3: Send to Admin (New View)
# -----------------------------
  # reply from admin will go to studen
  #sednt ot he custom admin


def send_to_admin(request, application_id):
    # Corrected function
    app = get_object_or_404(PassApplication, id=application_id)
    
    # Set status so it shows up in admin dashboard
    app.status = "Pending"
    app.save()
    
    # Optional: redirect student back to dashboard
    return HttpResponse("✅ Application sent to Admin dashboard successfully!")

#application pending

# views.py


@login_required
def approve_application(request, app_id):
    # 1️⃣ Fetch the application
    app = get_object_or_404(PassApplication, id=app_id)

    # 2️⃣ Update status & generate receipt ID
    app.status = "Approved"
    app.receipt_id = f"REC-{app.id}-{app.application_date.strftime('%Y%m%d')}"
    app.save()

    # 3️⃣ Generate PDF of application letter
    html_content = render_to_string(
        'get_application_letter.html',
        {'app': app, 'admin_signature': 'Admin Name'}
    )
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(src=html_content, dest=pdf_buffer)

    if pisa_status.err:
        return HttpResponse("❌ Failed to generate PDF.")

    pdf_buffer.seek(0)

    # 4️⃣ Prepare email to student (via SMTP)
    subject = f"Bus Pass Approved - Receipt ID {app.receipt_id}"
    body = f"""
Hello {app.name},

Your bus pass application has been approved ✅
Receipt ID: {app.receipt_id}

Please find the attached PDF for your reference.

Regards,
Bus Admin
"""

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,  # Admin email
        to=[app.email],  # Student email
        cc=[settings.DEFAULT_FROM_EMAIL],        # Admin gets copy
    )

    # Attach PDF
    email.attach(f"BusPass_{app.receipt_id}.pdf", pdf_buffer.getvalue(), 'application/pdf')

    try:
        email.send(fail_silently=False)  # Will raise error if SMTP fails
    except Exception as e:
        return HttpResponse(f"❌ Failed to send email: {e}")

    return HttpResponse(f"✅ Application approved and email sent to {app.email} with PDF.")




#rejec code

@login_required
def reject_application(request, app_id):
    # 1️⃣ Fetch the application
    app = get_object_or_404(PassApplication, id=app_id)

    # 2️⃣ Update status to Rejected
    app.status = "Rejected"
    app.save()

    # 3️⃣ Prepare rejection email
    subject = f"Bus Pass Application Rejected - ID {app.id}"
    body = f"""
Hello {app.name},

We regret to inform you that your bus pass application (ID: {app.id}) has been rejected ❌.

Please meet us in the college regarding your pass.

Regards,
Admin Team
"""

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,  # Admin email
        to=[app.email],                           # Student email
        cc=[settings.DEFAULT_FROM_EMAIL],         # Admin gets copy
    )

    try:
        email.send(fail_silently=False)  # Will raise error if SMTP fails
    except Exception as e:
        return HttpResponse(f"❌ Failed to send rejection email: {e}")

    return HttpResponse(f"✅ Application rejected and email sent to {app.email}.")
