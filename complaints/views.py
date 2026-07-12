from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import ComplaintForm, PaymentForm
from .models import Complaint
from .notifications import send_admin_email   # new import

def home(request):
    """Landing page"""
    return render(request, 'complaints/home.html')

def complaint_form(request):
    """Student fills complaint form"""
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save()
            # Send email to admin
            try:
                send_admin_email(complaint)
            except:
                pass
            return redirect('payment', complaint_id=complaint.id)
    else:
        form = ComplaintForm()
    return render(request, 'complaints/complaint_form.html', {'form': form})

def payment(request, complaint_id):
    """Payment page where student uploads screenshot"""
    complaint = get_object_or_404(Complaint, pk=complaint_id)
    fee = settings.COMPLAINT_FEE
    momo_number = settings.MOMO_NUMBER
    context = {
        'complaint': complaint,
        'fee': fee,
        'momo_number': momo_number,
    }

    if complaint.payment_status in ['paid', 'verified']:
        context['payment_done'] = True
        return render(request, 'complaints/payment.html', context)

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES, instance=complaint)
        if form.is_valid():
            form.instance.payment_status = 'paid'
            form.save()
            context['payment_done'] = True
            return render(request, 'complaints/payment.html', context)
    else:
        form = PaymentForm()

    context['form'] = form
    return render(request, 'complaints/payment.html', context)

def status(request, complaint_id):
    """Track complaint status"""
    complaint = get_object_or_404(Complaint, pk=complaint_id)
    return render(request, 'complaints/status.html', {'complaint': complaint})

def track_complaint(request):
    """Search for complaint by ID"""
    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id', '').strip()
        try:
            complaint = Complaint.objects.get(id=complaint_id)
            return redirect('status', complaint_id=complaint.id)
        except Complaint.DoesNotExist:
            return render(request, 'complaints/track.html', {
                'error': 'Complaint not found. Please check your ID.'
            })
    return render(request, 'complaints/track.html')