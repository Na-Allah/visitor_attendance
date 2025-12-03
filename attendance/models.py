# attendance/models.py

from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings

class Organisation(models.Model):
    name = models.CharField(max_length=200)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    def save(self, *args, **kwargs):
        # First save → ensures self.id exists
        creating = self.pk is None
        super().save(*args, **kwargs)

        # Generate QR only when created OR if no QR exists
        if creating or not self.qr_code:
            qr_url = f"{settings.BASE_URL}/visit/{self.id}/"
            qr = qrcode.make(qr_url)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            file_name = f"org-{self.id}.png"

            self.qr_code.save(file_name, File(buffer), save=False)
            super().save(update_fields=["qr_code"])

    def __str__(self):
        return self.name


class Visitor(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.organisation.name})"

class Attendance(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.visitor.name} → {self.organisation.name} ({self.check_in})"

