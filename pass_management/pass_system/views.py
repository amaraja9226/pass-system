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
            'student_signature_url': student_signature_url,
        }
    })


# --------------------------------------------------------------------
# CREATE PASS (AUTO SAVE)
#se:
def create_pass(request):
    if request.method == 'POST':
        receipt_id = request.POST.get('receipt_id')
        application = PassApplication.objects.get(receipt_id=receipt_id)

        form = IssuePassForm(request.POST)
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
