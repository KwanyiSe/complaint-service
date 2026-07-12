from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import path
from .models import Complaint

class ComplaintAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'submission_office', 'school', 'course_code',
        'payment_status', 'is_submitted', 'created_at'
    ]
    list_filter = ['payment_status', 'is_submitted', 'school']
    search_fields = ['name', 'matricule', 'complaint_number', 'course_code']
    actions = ['verify_payment', 'submit_complaint_action']

    @admin.action(description='✅ Verify selected payments')
    def verify_payment(self, request, queryset):
        queryset.update(payment_status='verified')
        self.message_user(request, "Selected payments marked as verified.")

    @admin.action(description='📤 Submit complaint & upload snapshot')
    def submit_complaint_action(self, request, queryset):
        ids = ','.join(str(obj.id) for obj in queryset)
        return HttpResponseRedirect(f'submit-complaint/?ids={ids}')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('submit-complaint/', self.admin_site.admin_view(self.submit_complaint_view), name='submit-complaint'),
        ]
        return custom_urls + urls

    def submit_complaint_view(self, request):
        ids = request.GET.get('ids', '')
        if not ids:
            messages.error(request, "No complaints selected.")
            return HttpResponseRedirect('../')

        id_list = ids.split(',')
        complaints = Complaint.objects.filter(id__in=id_list)

        class SubmitForm(forms.Form):
            snapshot = forms.ImageField(required=True, label='Upload submitted form snapshot')
            notify_student = forms.BooleanField(
                required=False, initial=True,
                label='Send notification to student?'
            )

        if request.method == 'POST':
            form = SubmitForm(request.POST, request.FILES)
            if form.is_valid():
                snapshot = form.cleaned_data['snapshot']
                for complaint in complaints:
                    complaint.submitted_snapshot = snapshot
                    complaint.is_submitted = True
                    complaint.save()

                    # Send email to student if they provided an email
                    if complaint.email:
                        snapshot_url = request.build_absolute_uri(complaint.submitted_snapshot.url)
                        try:
                            from .notifications import send_student_email
                            send_student_email(complaint, snapshot_url)
                        except Exception as e:
                            print(f"Email to student failed: {e}")

                self.message_user(request, "Complaints submitted and snapshots uploaded. Emails sent.")
                return HttpResponseRedirect('../')
        else:
            form = SubmitForm()

        context = dict(
            self.admin_site.each_context(request),
            form=form,
            complaints=complaints,
        )
        return render(request, 'admin/submit_complaint.html', context)

admin.site.register(Complaint, ComplaintAdmin)