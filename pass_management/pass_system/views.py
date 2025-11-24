from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from get_new_pass.models import PassApplication
from .models import IssuePass
from .forms import IssuePassForm
import os
from datetime import date



# --------------------------------------------------------------------
# VALIDATE RECEIPT
# --------------------------------------------------------------------
def validate_receipt(request):
    receipt_id = request.GET.get('receipt_id', '').strip()

    if not receipt_id:
        return JsonResponse({'valid': False, 'message': 'Receipt ID required!'})

    try:
        application = PassApplication.objects.get(receipt_id=receipt_id)
    except PassApplication.DoesNotExist:
        return JsonResponse({'valid': False, 'message': 'Invalid Receipt ID!'})

    if application.status != "Approved":
        return JsonResponse({'valid': False, 'message': 'Application not approved yet!'})

    # Amount based on village
    amount = IssuePass.get_amount_for_village(application.village)

    # Student signature from PassApplication
    student_signature_url = (
        request.build_absolute_uri(application.student_signature.url)
        if application.student_signature else ''
    )

    return JsonResponse({
        'valid': True,
        'data': {
            'student_name': application.name,
            'student_class': application.class_name,
            'department': application.department,
            'village': application.village,
            'amount': amount,
            'month': application.month,
            'student_signature_url': student_signature_url,
        }
    })


# --------------------------------------------------------------------
# CREATE PASS (AUTO SAVE)
#se:
from django.shortcuts import render, redirect, get_object_or_404
from .forms import IssuePassForm
from get_new_pass.models import PassApplication

def create_pass(request):
    if request.method == 'POST':
        receipt_id = request.POST.get('receipt_id')
        application = get_object_or_404(PassApplication, receipt_id=receipt_id)

        # form me POST + FILES dono pass kare
        form = IssuePassForm(request.POST, request.FILES)
        if form.is_valid():
            issue_pass = form.save(commit=False)

            # AUTO COPY SIGNATURE FROM PassApplication ➝ IssuePass
            issue_pass.student_signature = application.student_signature

            issue_pass.save()
            return redirect('view_receipt', receipt_id=issue_pass.receipt_id)
    else:
        form = IssuePassForm()

    return render(request, 'create_pass.html', {'form': form})



# --------------------------------------------------------------------
# VIEW RECEIPT
# --------------------------------------------------------------------
def view_receipt(request, receipt_id):
    issue_pass = get_object_or_404(IssuePass, receipt_id=receipt_id)
    return render(request, 'receipt.html', {
        'receipt': issue_pass,
        'current_date': date.today()
    })


# --------------------------------------------------------------------
# PASS LIST
# --------------------------------------------------------------------
def pass_list(request):
    passes = IssuePass.objects.all()
    return render(request, 'pass_list.html', {'passes': passes})


#send money 


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit  # pip install pdfkit
from .models import IssuePass
from django.utils.timezone import now

# Receipt View


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.timezone import now
import pdfkit
from .models import IssuePass


def view_receipt(request, receipt_id):
    # get last created receipt if duplicates exist
    receipt = IssuePass.objects.filter(receipt_id=receipt_id).last()

    if not receipt:
        raise Http404("Receipt not found")

    return render(request, "receipt.html", {
        "receipt": receipt,
        "current_date": now()
    })


def fake_payment(request, receipt_id):
    receipt = get_object_or_404(IssuePass, receipt_id=receipt_id)
    receipt.payment_status = "PAID"
    receipt.save()
    return redirect("view_receipt", receipt_id=receipt_id)


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from .models import IssuePass
from datetime import datetime


def download_receipt_pdf(request, receipt_id):
    # 1. Get the receipt record
    receipt = get_object_or_404(IssuePass, receipt_id=receipt_id)

    # 2. Render HTML page for PDF
    html = render_to_string("receipt_pdf.html", {
        "receipt": receipt,
        "current_date": datetime.now(),
    })

    # 3. Convert HTML → PDF
    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_file)

    if pisa_status.err:
        return HttpResponse("❌ PDF generation error")

    # 4. Return PDF file for download
    response = HttpResponse(pdf_file.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=Receipt_{receipt.receipt_id}.pdf"
    return response
