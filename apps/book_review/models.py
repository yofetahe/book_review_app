from django.db import models
from apps.login_reg.models import User

class ReviewManager(models.Manager):
    def validate_review(self, postData):
        errors = {}
        if len(postData['book_review']) == 0:
            errors['book_review'] = "Book review is required"
        return errors

class BookManager(models.Manager):
    def validate_book(self, postData):
        errors = {}
        if len(postData['title']) == 0:
             errors['title'] = "Book title is required"
        if len(postData['selected_author']) == 0 and len(postData['first_name']) == 0 and len(postData['last_name']) == 0:
            errors['selected_author'] = "Author is required"
        if len(postData['selected_author']) > 0 and len(postData['first_name']) > 0 and len(postData['last_name']) > 0:
            errors['selected_author'] = "Choose which Author you want"
        if len(postData['selected_author']) == 0 and (len(postData['first_name']) == 0 or len(postData['last_name']) == 0):
            errors['selected_author'] = "Author full name is required"
        if len(postData['review']) == 0:
            errors['review'] = "Book review is required"
        return errors
        

class Author(models.Model):
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=225)    
    author = models.ForeignKey(Author, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BookManager()

class Review(models.Model):
    review_content = models.TextField()
    rating = models.IntegerField(default=1)
    book = models.ForeignKey(Book, related_name="reviews")
    user = models.ForeignKey(User, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReviewManager() 
