from django.shortcuts import redirect, render

from tracker.models import CurrentBalance, TrackingHistory

# Create your views here.
def index(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        expense_type = 'DEBIT' if float(amount) < 0 else 'CREDIT'
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

     
    # Handle form submission here
    return render(request, "index.html")
