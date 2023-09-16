from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import requests
from datetime import date


# Create your views here.


def home(request):
    return render(request, "index.html")

def all_books(request):
    books = Book.objects.order_by('created_at').reverse()
    return render(request, "all-books.html", {'books': books})

def all_members(request):
    members = Member.objects.order_by('created_at').reverse()
    return render(request, "all-members.html", {'members': members})

def all_transactions(request):
    transactions = Transaction.objects.order_by('created_at').reverse()
    return render(request, "all-transactions.html", {'transactions': transactions})



def import_books(request):
    if(request.POST):
        number_of_books = int(request.POST.get('number_of_books', 1))
        title = request.POST.get('title', None)
        authors = request.POST.get('authors', None)
        isbn = request.POST.get('isbn', None)
        publisher = request.POST.get('publisher', None)
        params = ''
        if title:
            params += '&title={}'.format(title)
        if authors:
            params += '&authors={}'.format(authors)
        if isbn:
            params += '&isbn={}'.format(isbn)
        if publisher:
            params += '&publisher={}'.format(publisher)

        books = []
        page = 1
        prev_lenght = len(books)
        while len(books) < number_of_books:
            response = requests.get('https://frappe.io/api/method/frappe-library?page={}&{}'.format(page, params))
            books.extend(response.json()['message'])
            if prev_lenght == len(books):
                break
            else:
                prev_lenght = len(books)
            page += 1

        books = books[:number_of_books]
        for book in books:
            Book.objects.create(
                title=book['title'],
                authors=book['authors'],
                isbn=book['isbn'],
                publisher=book['publisher'],
                num_pages=book['  num_pages']
            )
        messages.add_message(request, messages.SUCCESS, str(len(books))+' Books Imported Successfully')
        return redirect(import_books)
    return render(request, "import-books.html")
    
def delete_book(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    messages.add_message(request, messages.SUCCESS, 'Book Deleated Successfully')
    return redirect(all_books)


def delete_member(request, id):
    member = Member.objects.get(id=id)
    member.delete()
    messages.add_message(request, messages.SUCCESS, 'Member Deleated Successfully')
    return redirect(all_members)

def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        authors = request.POST.get('authors')
        isbn = request.POST.get('isbn')
        publisher = request.POST.get('publisher')
        num_pages = request.POST.get('num_pages')

        book = Book(
            title=title,
            authors=authors,
            isbn=isbn,
            publisher=publisher,
            num_pages=num_pages
        )
        book.save()
        messages.add_message(request, messages.SUCCESS, 'Books Added Successfully')
        return redirect(add_book)
    return render(request, "book.html")
    
def add_member(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        member = Member(
            name=name,
            email=email,
        )
        member.save()
        messages.add_message(request, messages.SUCCESS, 'Member Added Successfully')
        return redirect(add_member)
    return render(request, "member.html")
    
def edit_book(request, id):
    book = Book.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST.get('title')
        authors = request.POST.get('authors')
        isbn = request.POST.get('isbn')
        publisher = request.POST.get('publisher')
        num_pages = request.POST.get('num_pages')

        book.title = title
        book.authors = authors
        book.isbn = isbn
        book.publisher = publisher
        book.num_pages = num_pages
        book.save()
        messages.add_message(request, messages.SUCCESS, 'Book Updated Successfully')
        return redirect(all_books)
    else:
        return render(request, 'book.html', {'book': book})
    
def edit_member(request, id):
    member = Member.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        outstanding_debt = request.POST.get('outstanding_debt')

        member.name = name
        member.email = email
        member.outstanding_debt = outstanding_debt
        member.save()
        messages.add_message(request, messages.SUCCESS, 'Member Updated Successfully')
        return redirect(all_members)
    else:
        return render(request, 'member.html', {'member': member})
    
def issue_book(request):
    if request.method == 'POST':
        member = Member.objects.get(id=request.POST.get('member-id'))
        if member.outstanding_debt > 500:
            messages.add_message(request, messages.ERROR, "Cannot Issue Book, Member's Debt is more than 500")
        else:
            book = Book.objects.get(id=request.POST.get('book-id'))
            if(book.available):  
                transaction = Transaction(
                    book=book,
                    member=member,
                )
                transaction.book.available = False
                transaction.book.save()
                transaction.save()
                messages.add_message(request, messages.SUCCESS, 'Books Issued successfully')
            else:
                messages.add_message(request, messages.ERROR, 'Books Is Already Issued To Member Id: '+str(member.id))
        return redirect(issue_book)
    return render(request, "issue-book.html")

def return_book(request):
    if request.method == 'POST':
        try:
            transaction = Transaction.objects.get(book=request.POST.get('book-id'),return_date=None)
            transaction.return_date = date.today()
            transaction.fine = request.POST.get('fine')
            transaction.member.outstanding_debt+=int(request.POST.get('fine'))
            transaction.book.available = True
            transaction.book.save()
            transaction.member.save()
            transaction.save()
            messages.add_message(request, messages.SUCCESS, 'Books Returned')
        except Transaction.DoesNotExist:
            messages.add_message(request, messages.ERROR, "Book Hasn't been Issued Yet")
        return redirect(return_book)
    return render(request, "return-book.html")

def search_book(request):
    if request.method == 'POST':
        if(request.POST.get('title')=='' and request.POST.get('author')!='' ):
            books = Book.objects.filter(authors=request.POST.get('author'))
        elif(request.POST.get('author')=='' and request.POST.get('title')!='' ):
            books = Book.objects.filter(title=request.POST.get('title'))
        else:
            books = Book.objects.filter(title=request.POST.get('title')).filter(authors=request.POST.get('author'))
            print("both or none")
        if(len(books)==0):
            messages.add_message(request, messages.ERROR, str(len(books))+" Results Found")
        else:
            messages.add_message(request, messages.SUCCESS, str(len(books))+" Results Found")
        return render(request, "search-book.html", {'books': books})
    return render(request, "search-book.html")