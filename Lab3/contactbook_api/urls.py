from django.contrib import admin
from django.urls import path

from .views import ContactList, ContactDetail, ContactCreate, EditContact, DeleteContact

urlpatterns = [
    path('list/', ContactList.as_view()),
    path('create/', ContactCreate.as_view()),
    path('<int:pk>', ContactDetail.as_view()),
    path('update/<int:pk>', EditContact.as_view()),
    path('delete/<int:pk>', DeleteContact.as_view())
]