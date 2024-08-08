from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.core.mail import send_mail
from librarymanagement.settings import EMAIL_HOST_USER
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import IssuedBookForm
from .models import StudentExtra, IssuedBook
from django.core.paginator import Paginator
from django.db.models import Q

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')

#for showing signup/login button for teacher
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/adminclick.html')

def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'library/adminsignup.html',{'form':form})


def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'library/adminafterlogin.html')
    else:
        return render(request,'library/studentafterlogin.html')
    
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    #now it is empty book form for sending to html
    form=forms.BookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.BookForm(request.POST)
        if form.is_valid():
            user=form.save()
            return render(request,'library/bookadded.html')
    return render(request,'library/addbook.html',{'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books = models.Book.objects.all()
    
    # Get filter and search parameters from the query string
    category = request.GET.get('category', '')
    search_isbn = request.GET.get('search_isbn', '')
    
    # Filter books based on category and search_isbn
    if category:
        books = books.filter(category=category)
    if search_isbn:
        books = books.filter(isbn__icontains=search_isbn)
    
    # Get the items_per_page parameter from the query string
    items_per_page = request.GET.get('items_per_page', 10)  # Default to 10 items per page
    try:
        items_per_page = int(items_per_page)
    except ValueError:
        items_per_page = 10
    
    paginator = Paginator(books, items_per_page)  # Show `items_per_page` books per page
    page_number = request.GET.get('page')
    books_page = paginator.get_page(page_number)
    
    categories = models.Book.catchoice
    
    return render(request, 'library/viewbook.html', {
        'books': books_page,
        'items_per_page': items_per_page,
        'category': category,
        'search_isbn': search_isbn,
        'categories': categories,
    })


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    if request.method == 'POST':
        form = IssuedBookForm(request.POST)
        if form.is_valid():
            obj = IssuedBook()
            obj.Kelas = form.cleaned_data['kelas2']
            obj.isbn = form.cleaned_data['isbn2']
            obj.save()
            return render(request, 'library/bookissued.html')
    else:
        form = IssuedBookForm()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        kelas = request.GET.get('kelas')
        students = StudentExtra.objects.filter(Kelas=kelas).values('id', 'user__first_name')
        return JsonResponse(list(students), safe=False)

    kelas_list = StudentExtra.objects.values_list('Kelas', flat=True).distinct()
    return render(request, 'library/issuebook.html', {'form': form, 'kelas_list': kelas_list})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def end_issue_early_view(request, pk):
    issued_book = get_object_or_404(models.IssuedBook, pk=pk)
    issued_book.delete()
    return HttpResponseRedirect('/viewissuedbook')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks = models.IssuedBook.objects.all()
    li = []

    for ib in issuedbooks:
        issdate = f"{ib.issuedate.day}-{ib.issuedate.month}-{ib.issuedate.year}"
        expdate = f"{ib.expirydate.day}-{ib.expirydate.month}-{ib.expirydate.year}"

        # Calculate fine
        days_overdue = (date.today() - ib.expirydate).days
        fine = days_overdue * 2000 if days_overdue > 0 else 0

        books = list(models.Book.objects.filter(isbn=ib.isbn))
        students = list(models.StudentExtra.objects.filter(Kelas=ib.Kelas))

        for i in range(min(len(books), len(students))):
            t = (
                students[i].get_name,
                students[i].Kelas,
                books[i].name,
                books[i].author,
                issdate,
                expdate,
                fine,
                ib.pk  # Add primary key here
            )
            li.append(t)

    return render(request, 'library/viewissuedbook.html', {'li': li})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students = models.StudentExtra.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(user__first_name__icontains=search_query) | 
            Q(user__last_name__icontains=search_query)
        )
    
    # Filter by Kelas
    kelas_filter = request.GET.get('kelas', '')
    if kelas_filter:
        students = students.filter(Kelas=kelas_filter)
    
    # Sort functionality
    sort_by = request.GET.get('sort_by', 'Kelas')
    if sort_by:
        students = students.order_by(sort_by)
    
    # Pagination
    items_per_page = request.GET.get('items_per_page', 10)  # Default to 10 items per page
    try:
        items_per_page = int(items_per_page)
    except ValueError:
        items_per_page = 10
    
    paginator = Paginator(students, items_per_page)  # Show `items_per_page` students per page
    page_number = request.GET.get('page')
    students_page = paginator.get_page(page_number)
    
    # Get distinct Kelas values for the filter dropdown
    kelas_list = models.StudentExtra.objects.values_list('Kelas', flat=True).distinct()
    
    return render(request, 'library/viewstudent.html', {
        'students': students_page,
        'items_per_page': items_per_page,
        'search_query': search_query,
        'sort_by': sort_by,
        'kelas_list': kelas_list,
        'kelas_filter': kelas_filter,
    })


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(Kelas=student[0].Kelas)

    li1=[]
    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].Kelas,student[0].branch,book.name,book.author)
            li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)

    return render(request,'library/viewissuedbookbystudent.html',{'li1':li1,'li2':li2})


def aboutus_view(request):
    return render(request,'library/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, EMAIL_HOST_USER, ['wapka1503@gmail.com'], fail_silently = False)
            return render(request, 'library/contactussuccess.html')
    return render(request, 'library/contactus.html', {'form':sub})
