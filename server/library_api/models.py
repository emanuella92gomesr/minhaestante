import uuid
from django.db import models
from datetime import datetime


class LibraryModel(models.Model):
    objects = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=400)
    author = models.CharField(max_length=400)
    publishing_company = models.CharField(max_length=100)
    pages = models.IntegerField()
    edition = models.IntegerField(null=True)
    # createdAt = models.DateTimeField(auto_now_add=True)
    # updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "library"
        ordering = ["id"]
