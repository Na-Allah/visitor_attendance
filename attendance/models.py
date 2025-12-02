# attendance/models.py

from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File

class Organisation(models.Model):
    name = models.CharField(max_length=200)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    def save(self, *args, **kwargs):
        qr = qrcode.make(f"http://127.0.0.1:8000/visit/{self.id}/")
        buffer = BytesIO()
        qr.save(buffer, "PNG")
        self.qr_code.save(f"org-{self.id}.png", File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Visitor(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.organisation.name})"
