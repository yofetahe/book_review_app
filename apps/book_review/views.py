from django.shortcuts import render, redirect
from .models import Author, Book, Review
from apps.login_reg.models import User
from django.contrib import messages

def book_index(request):

    if 'user' not in request.session:
        return redirect('../login/get_login_page')

    latest_books = Book.objects.all().order_by('-created_at')[:3]
    
    books = Book.objects.all()
    
    context = {
        "latest_books":latest_books,
        "books":books
    }

    return render(request, 'book_review/book_index.html', context)

def add_book_and_review(request):

    if 'user' not in request.session:
        return redirect('../login/get_login_page')

    authors = Author.objects.all()
    return render(request, 'book_review/add_form.html', {"authors":authors})

def save_book(request):

    if 'user' not in request.session:
        return redirect('../login/get_login_page')

    errors = Book.objects.validate_book(request.POST)

    # ----- validation ----
    if len(errors) > 0:
        for tag, value in errors.items():
            messages.error(request, value, extra_tags=tag)
        return redirect(add_book_and_review)

    user = User.objects.get(id=request.session['user_id'])
    
    if request.POST['selected_author']:
        author = Author.objects.get(id=request.POST['selected_author'])
    else:
        author = Author.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'])

    book = Book.objects.create(title=request.POST['title'], author=author)
    
    Review.objects.create(review_content=request.POST['review'], rating=request.POST['rating'], book=book, user=user)
    
    return redirect('get_book_review', book_id=book.id)

def get_book_review(request, book_id):

    if 'user' not in request.session:
        return redirect('../login/get_login_page')

    book = Book.objects.get(id = book_id)
    return render(request, 'book_review/book_detail.html', {"book":book})

def submit_review(request, book_id):

    if 'user' not in request.session:
        return redirect('../login/get_login_page')

    # ---- validation -------
    errors = Review.objects.validate_review(request.POST)
    if len(errors) > 0:
        for tag, value in errors.items():
            messages.error(request, value, extra_tags=tag)
        return redirect('get_book_review', book_id=book_id)

    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    Review.objects.create(review_content=request.POST['book_review'], rating=request.POST['rating'], book=book, user=user)
    return redirect('get_book_review', book_id = book_id)

def get_user_detail(request, user_id):

    if 'user' not in request.session:
        return redirect('../login/get_login_page')

    user = User.objects.get(id=user_id)
    return render(request, 'book_review/user_detail.html', {"user":user})

def delete_review(request, review_id, book_id):
    print(review_id)
    review = Review.objects.get(id=review_id)
    print(review) 
    if review.user.id == request.session['user_id']:
        review = Review.objects.get(id=review_id)
        review.delete()
    else:
        messages.error(request, "Sorry, the review is not yours", extra_tags="delete_review")
    return redirect('get_book_review', book_id)

def logout(request):
    request.session.pop('user')
    request.session.pop('user_id')
    return redirect(book_index)
