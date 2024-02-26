from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .forms import SignUpForm, RecordForm
from .models import Record

def home(request):
    records = Record.objects.all()
    query = request.GET.get('q', '')
    results = Record.objects.filter(first_name__icontains=query)

    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')  
       
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect('home')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('home')
            
        else:
            messages.error(request, "Invalid login credentials. Please try again.")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records, 'query': query, 'results': results})


def login_user(request):
    pass


def logout_user(request):
    logout(request)
    messages.success(request, "See you! ")
    return redirect('home')


def register_user(request):

    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered. Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    

    
def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You must login first.")
        return redirect('home')
    
def add_record(request):
    form = RecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record has been successfully added.")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.error(request, "You must login first.")
        return redirect('home')


def edit_record(request, pk):
    if request.user.is_authenticated:
        record = get_object_or_404(Record, pk=pk)
        if request.method == 'POST':
            form = RecordForm(request.POST, instance=record)
            if form.is_valid():
                form.save()
                messages.success(request, "Record has been successfully updated.")
                return redirect('home')
        else:
            form = RecordForm(instance=record)
        return render(request, 'edit_record.html', {'form': form, 'record': record})
    else:
        messages.success(request, "You must login first.")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record has been successfully deleted.")
        return redirect('home')
    else:
        messages.success(request, "You must login first.")
        return redirect('home')


