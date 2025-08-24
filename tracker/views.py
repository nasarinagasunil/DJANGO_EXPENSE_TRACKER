from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from tracker.models import CurrentBalance, TrackingHistory

# Create your views here.
@login_required(login_url='/login')
def index(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        expense_type = 'CREDIT'
        if float(amount) < 0:
            expense_type = 'DEBIT'
        if float(amount) == 0:
            messages.success(request, "Amount cannot be zero")
            return redirect("/")
        current_balance, _ = CurrentBalance.objects.get_or_create(id=1)
        tracking_history = TrackingHistory.objects.create(
            current_balance=current_balance,
            expense_type=expense_type,
            amount=amount,
            description=description
        )
        current_balance.current_balance += float(tracking_history.amount)
        current_balance.save()

        return redirect("/")
    current_balance, _ = CurrentBalance.objects.get_or_create(id=1)
    income=0
    expense=0
    for transaction in TrackingHistory.objects.all():
        if transaction.expense_type == 'CREDIT' :
            income +=float(transaction.amount)
        else :
            expense += float(transaction.amount)
    context ={"transactions":TrackingHistory.objects.all(), "current_balance": current_balance, "income": income, "expense": expense}
    # Handle form submission here
    return render(request, "index.html", context)

@login_required(login_url='/login')
def delete_transaction(request, id):
    current_balance, _ = CurrentBalance.objects.get_or_create(id=1)
    transaction=TrackingHistory.objects.get(id=id)
    current_balance.current_balance -= float(transaction.amount)
    current_balance.save()
    transaction.delete()
    return redirect("/")

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("/login")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username = username)
        if not user.exists():
            messages.success(request, "User Name not found")
            return redirect("/login")
        user = authenticate(username=username, password=password)
        if not user:
            messages.success(request, "Invalid credentials/ Password is incorrect")
            return redirect("/login")
        login(request, user)
        messages.success(request, "Logged in successfully")
        return redirect("/")
    return render(request, "login.html")

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        user = User.objects.filter(username = username)
        if user.exists():
            messages.success(request, "User Name already exists. Create new User Name")
            return redirect("/register")
        user=User.objects.create(
            username=username, 
            first_name=first_name, 
            last_name=last_name
            )
        user.set_password(password)
        user.save()
        messages.success(request, "User created successfully. Please login.")
        return redirect("/login")
    return render(request, "register.html")