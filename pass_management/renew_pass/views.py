# views.py
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from pass_system.models import IssuePass
from .forms import RenewPassForm
from .models import RenewPass

def renew_pass_view(request):
    receipt_id = request.GET.get('receipt_id')
    original_pass = None

    if receipt_id:
        original_pass = get_object_or_404(IssuePass, receipt_id=receipt_id)

    if request.method == 'POST':
        # ✅ request.FILES zaruri hai
        form = RenewPassForm(request.POST, request.FILES)
        if form.is_valid():
            new_renew = form.save(commit=False)
            # auto-generate receipt_id
            new_renew.receipt_id = f"REC-{RenewPass.objects.count()+1}-{timezone.now().strftime('%Y%m%d')}"
            
            # ✅ photo aur signature save honge
            new_renew.save()
            return redirect('renew_receipt', receipt_id=new_renew.receipt_id)
    else:
        initial_data = {}
        if original_pass:
            initial_data = {
                'original_receipt_id': original_pass.receipt_id,
                'name': getattr(original_pass, 'student_name', ''),
                'student_class': getattr(original_pass, 'student_class', ''),
                'department': getattr(original_pass, 'department', ''),
                'village': getattr(original_pass, 'village', ''),
                'month': timezone.now().strftime('%B-%Y'),
                'photo': getattr(original_pass, 'student_photo', None),        # ✅ student photo

                'amount': getattr(original_pass, 'amount', 0),
            }
        form = RenewPassForm(initial=initial_data)

    return render(request, 'renew_form.html', {'form': form})


def renew_receipt_view(request, receipt_id):
    renew_pass = get_object_or_404(RenewPass, receipt_id=receipt_id)
    try:
        original_pass = IssuePass.objects.get(receipt_id=renew_pass.original_receipt_id)
    except IssuePass.DoesNotExist:
        original_pass = None

    current_date = timezone.now().date()
    current_month = timezone.now().strftime("%B %Y")

    return render(
        request,
        'renew_receipt.html',
        {
            'renew_pass': renew_pass,
            'original_pass': original_pass,
            'current_date': current_date,
            'current_month': current_month
        }
    )





from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import RenewPass
from pass_system.models import IssuePass

def update_payment_status(request, receipt_id):
    """
    AJAX view: Update payment status to PAID
    """
    renew_pass = get_object_or_404(RenewPass, id=receipt_id)
    renew_pass.payment_status = "PAID"
    renew_pass.save()
    return JsonResponse({"status": "success"})


def pay_and_download_pdf(request, receipt_id):
    """
    Directly generate PDF after payment (optional, if you want server-side PDF)
    """
    renew_pass = get_object_or_404(RenewPass, id=receipt_id)
    try:
        original_pass = IssuePass.objects.get(receipt_id=renew_pass.original_receipt_id)
    except IssuePass.DoesNotExist:
        original_pass = None

    # Update payment status if not already
    if renew_pass.payment_status != "PAID":
        renew_pass.payment_status = "PAID"
        renew_pass.save()

    # Render HTML for PDF
    html = render_to_string("renew_receipt_pdf.html", {
        "receipt": renew_pass,
        "original_pass": original_pass
    })

    # Optional: return HTML (or integrate with xhtml2pdf / WeasyPrint for PDF)
    return render(request, "renew_receipt_pdf.html", {
        "receipt": renew_pass,
        "original_pass": original_pass
    })


from django.shortcuts import render, get_object_or_404
from .models import RenewPass
from pass_system.models import IssuePass

def renew_receipt_pdf(request, receipt_id):
    """
    Display the Renew Pass receipt page with download button
    """
    receipt = get_object_or_404(RenewPass, id=receipt_id)

    # Get original pass for admin/subadmin signature
    original_pass = None
    try:
        original_pass = IssuePass.objects.get(receipt_id=receipt.original_receipt_id)
    except IssuePass.DoesNotExist:
        original_pass = None

    context = {
        'receipt': receipt,
        'original_pass': original_pass
    }
    return render(request, 'renew_receipt_pdf.html', context)


from django.http import JsonResponse
from .models import RenewPass

def update_payment_status(request, renew_pass_id):
    if request.method == "GET":  # ya POST, jo bhi use kar rahe ho
        try:
            renew_pass = RenewPass.objects.get(id=renew_pass_id)
            renew_pass.payment_status = "PAID"
            renew_pass.save()  # IMPORTANT: ye save karna hai
            return JsonResponse({"status": "success"})
        except RenewPass.DoesNotExist:
            return JsonResponse({"status": "error", "message": "RenewPass not found"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request"})
