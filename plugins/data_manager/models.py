from django.db import models
from django.contrib.auth.models import User


class DataUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    db_name = models.CharField(max_length=255)


class DataTable(models.Model):
    data_upload = models.ForeignKey(DataUpload, on_delete=models.CASCADE)
    table_name = models.CharField(max_length=255)
    source_name = models.CharField(max_length=255)


class UserFile(models.Model):
    user = models.CharField(max_length=255)
    db_file = models.CharField(max_length=255)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    edition_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "db_file")
