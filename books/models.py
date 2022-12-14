from django.db import models
from Ebookify.enums import BOOK_CATEGORY
import uuid


class Book(models.Model):
    book_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=225, null=False, blank=False)
    book_category = models.CharField(max_length=50, null=False, choices=BOOK_CATEGORY, default=BOOK_CATEGORY[0][0])
    author = models.CharField(max_length=201, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    book_image = models.FileField(upload_to='book-images/', null=False)
    isbn = models.CharField(max_length=100, blank=False, null=False)
    date_created = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
