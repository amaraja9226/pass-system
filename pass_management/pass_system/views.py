from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import IssuePassForm
from .models import IssuePass
from get_new_pass.models import PassApplication


def validate_receipt(request):
    """
    PassApplication database se receipt_id validate karta hai
    Valid hone par student data return karta hai
    """
    if request.method == 'GET':
        receipt_id = request.GET.get('receipt_id', '').strip()
        print("🔍 Searching Receipt ID:", receipt_id)

        if not receipt_id:
            return JsonResponse({'valid': False, 'message': 'Please enter a receipt ID.'})

        try:
            # PassApplication database se data fetch karo
            application = PassApplication.objects.get(receipt_id=receipt_id)
        except PassApplication.DoesNotExist:
            print("❌ Invalid Receipt ID:", receipt_id)
            return JsonResponse({'valid': False, 'message': 'Invalid Receipt ID. Please check and try again.'})

        # ✅ Only approved applications allowed
        if application.status != "Approved":
            print("⚠️ Application not approved yet:", application.status)
            return JsonResponse({'valid': False, 'message': 'Application not approved yet.'})

        # Village ke basis par amount calculate karo
        amount = IssuePass.get_amount_for_village(application.village)
        print("✅ Application Found:", application.name)

        # ✅ Correct field names (not student_name / student_class)
        return JsonResponse({
            'valid': True,
            'data': {
                'student_name': application.name,
                'student_class': application.class_name,
                'department': application.department,
                'village': application.village,
                'amount': amount
            }
        })

    return JsonResponse({'valid': False, 'message': 'Invalid request method.'})


def create_pass(request):
    """
    Pass challan create karta hai
    Server-side validation: PassApplication database se data fetch karke IssuePass me save karta hai
    """
    if request.method == 'POST':
        receipt_id = request.POST.get('receipt_id', '').strip()
        print("📜 Searching receipt_id:", receipt_id)

        try:
            # PassApplication database se validate karo
            application = PassApplication.objects.get(receipt_id=receipt_id)
            print("✅ Application Found:", application.name)
        except PassApplication.DoesNotExist:
            messages.error(request, f'Invalid Receipt ID: {receipt_id}. Please verify and try again.')
            form = IssuePassForm()
            return render(request, 'create_pass.html', {'form': form})

        # ✅ Only approved applications allowed
        if application.status != "Approved":
            messages.error(request, "Application not approved yet.")
            return redirect('create_pass')

        # Village ke basis par amount calculate karo
        amount = IssuePass.get_amount_for_village(application.village)

        # IssuePass database me save karo
        issue_pass = IssuePass(
            receipt_id=application.receipt_id,
            student_name=application.name,
            student_class=application.class_name,
            department=application.department,
            village=application.village,
            amount=amount
        )
        issue_pass.save()

        messages.success(request, f'Pass Challan created successfully! Pass Number: {issue_pass.pass_number}')
        return redirect('create_pass')
    else:
        form = IssuePassForm()

    return render(request, 'create_pass.html', {'form': form})


def pass_list(request):
    """
    Sabhi issued passes ko display karta hai
    """
    passes = IssuePass.objects.all()
    return render(request, 'pass_list.html', {'passes': passes})
