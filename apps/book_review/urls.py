from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^book_index$', views.book_index, name="book_index"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^add_book_and_review$', views.add_book_and_review, name="add_book_and_review"),
    url(r'^save_book$', views.save_book, name="save_book"),
    url(r'^get_book_review/(?P<book_id>\d+)$', views.get_book_review, name="get_book_review"),
    url(r'^submit_review/(?P<book_id>\d+)$', views.submit_review, name="submit_review"),
    url(r'^get_user_detail/(?P<user_id>\d+)$', views.get_user_detail, name="get_user_detail"),
    url(r'^delete_review/(?P<review_id>\d+)/(?P<book_id>\d+)$', views.delete_review, name="delete_review"),
]