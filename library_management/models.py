from django.db import models


# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    outstanding_debt = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13)
    publisher = models.CharField(max_length=255)
    num_pages = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    fine = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.member.name+" "+self.book.title
