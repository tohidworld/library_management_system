"""
URL configuration for library_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from library_management import views as v

urlpatterns = [
    path('', v.home, name='home'),
    path('all-books/', v.all_books, name='all-books'),
    path('all-members/', v.all_members, name='all-members'),
    path('import-books/', v.import_books, name='import-books'),
    path('delete-book/<int:id>', v.delete_book, name="delete-book"),
    path('edit-book/<int:id>', v.edit_book, name="edit-book"),
    path('delete-member/<int:id>', v.delete_member, name="delete-member"),
    path('edit-member/<int:id>', v.edit_member, name="edit-member"),
    path('add-book/', v.add_book, name="add-book"),
    path('add-member/', v.add_member, name="add-member"),
    path('issue-book/', v.issue_book, name="issue-book"),
    path('return-book/', v.return_book, name="return-book"),
    path('search-book/', v.search_book, name="search-book"),
    path('all-transactions/', v.all_transactions, name="all-transactions"),
    path('admin/', admin.site.urls),
]
