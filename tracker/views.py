from django.contrib import messages
from django.shortcuts import redirect, render

from tracker.models import CurrentBalance, TrackingHistory

# Create your views here.
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


def delete_transaction(request, id):
    current_balance, _ = CurrentBalance.objects.get_or_create(id=1)
    transaction=TrackingHistory.objects.get(id=id)
    current_balance.current_balance -= float(transaction.amount)
    current_balance.save()
    transaction.delete()
    return redirect("/")