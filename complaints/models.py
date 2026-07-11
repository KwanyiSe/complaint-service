from django.db import models

class Complaint(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid - Awaiting Verification'),
        ('verified', 'Payment Verified'),
    ]

    # Student Information
    name = models.CharField(max_length=200, verbose_name="Full Name")
    matricule = models.CharField(max_length=50, verbose_name="Matricule Number")
    level = models.CharField(
        max_length=50,
        verbose_name="Level",
        help_text="e.g., 100, 200, 300, 400, Masters"
    )
    semester = models.CharField(
        max_length=20,
        verbose_name="Semester",
        help_text="e.g., First Semester, Second Semester"
    )
    school = models.CharField(max_length=200, verbose_name="School/Faculty")
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number (for updates)")

    # Complaint Details
    complaint_number = models.CharField(max_length=100, verbose_name="Complaint Number")
    submission_office = models.CharField(
        max_length=300,
        verbose_name="Which office should we submit this to?",
        help_text="e.g., Dean's Office, Department of Physics, Exams and Records"
    )
    complaint_text = models.TextField(
        verbose_name="What is your complaint about?",
        help_text="Describe your issue clearly"
    )

    # Academic Details
    course = models.CharField(max_length=200, verbose_name="Course Title")
    course_code = models.CharField(max_length=50, verbose_name="Course Code")
    ca_mark = models.CharField(max_length=50, verbose_name="CA Mark")
    exam_mark = models.CharField(max_length=50, verbose_name="Exam Mark")

    # Uploads
    proof = models.FileField(
        upload_to='proofs/',
        verbose_name="Supporting Document/Proof",
        help_text="Upload any relevant document or screenshot"
    )
    payment_screenshot = models.ImageField(
        upload_to='payment_proofs/',
        blank=True, null=True,
        verbose_name="Payment Screenshot",
        help_text="Upload screenshot of your MoMo payment confirmation"
    )

    # Status Tracking
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending',
        verbose_name="Payment Status"
    )
    is_submitted = models.BooleanField(
        default=False,
        verbose_name="Submitted to Office?"
    )
    submitted_snapshot = models.ImageField(
        upload_to='submitted_forms/',
        blank=True, null=True,
        verbose_name="Submitted Form Snapshot"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Complaint"
        verbose_name_plural = "Complaints"

    def __str__(self):
        return f"#{self.id} - {self.name} - {self.course_code}"