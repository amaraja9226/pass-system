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
from django.contrib import messages



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




from django.shortcuts import render
from .forms import PassApplicationForm

def create_application(request):
    if request.method == 'POST':
        form = PassApplicationForm(request.POST, request.FILES)  # ✅ Include request.FILES
        if form.is_valid():
            app = form.save(commit=False)
            app.status = 'Pending'
            app.save()
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


from django.urls import reverse
from django.urls import reverse

def send_to_admin(request, application_id):
    app = get_object_or_404(PassApplication, id=application_id)
    app.status = "Pending"
    app.save()

    home_url = reverse('home')  # change 'home' if your URL name is different

    return HttpResponse(f"""
        <html>
        <head>
            <meta http-equiv="refresh" content="2;url={home_url}" />
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light d-flex justify-content-center align-items-center" style="height:100vh;">
            <div class="text-center">
                <div class="alert alert-success shadow-lg p-4 rounded">
                    ✅ Application sent to Admin dashboard successfully!<br>
                    <small>Redirecting to home page...</small>
                </div>
            </div>
        </body>
        </html>
    """)

#application pending

# views.py


@login_required
def approve_application(request, app_id):
    app = get_object_or_404(PassApplication, id=app_id)

    # Update status
    app.status = "Approved"
    app.receipt_id = f"REC-{app.id}-{app.application_date.strftime('%Y%m%d')}"
    app.save()

    # Generate PDF
    html_content = render_to_string(
    'get_application_letter.html',
    {
        'app': app,
        'receipt_id': app.receipt_id,      # <-- ADD THIS LINE
        'admin_signature': 'Admin Name'
    }
)

    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(src=html_content, dest=pdf_buffer)

    if pisa_status.err:
        messages.error(request, "❌ PDF generation failed.")
        return redirect('home')

    pdf_buffer.seek(0)

    # Email
    email = EmailMessage(
        subject="Your Bus Pass Application Approved",
        body="Your application has been approved. Please find the attached PDF.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[app.email],
    )

    email.attach(
        f"BusPass_{app.receipt_id}.pdf",
        pdf_buffer.getvalue(),
        "application/pdf"
    )

    try:
        email.send()
        messages.success(request, f"✅ Application approved. Email sent to: {app.email}")
    except Exception as e:
        messages.error(request, f"❌ Email sending failed: {e}")

    # Redirect after message is set
    return redirect('home')


@login_required
def reject_application(request, app_id):
    app = get_object_or_404(PassApplication, id=app_id)

    app.status = "Rejected"
    app.save()

    subject = f"Bus Pass Application Rejected - ID {app.id}"
    body = f"""
Hello {app.name},

Your bus pass application (ID: {app.id}) has been rejected ❌.

Please meet us in the college.
"""

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[app.email],
    )

    try:
        email.send()
        messages.warning(request, f"⚠ Application rejected. Email sent to: {app.email}")
    except Exception as e:
        messages.error(request, f"❌ Failed to send email: {e}")

    # Redirect after message is created
    return redirect('home')
