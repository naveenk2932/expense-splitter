from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from .models import Group, Member, Expense


# =========================
# AUTHENTICATION VIEWS
# =========================

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('group_list')

    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        login(request, form.save())
        return redirect('group_list')

    return render(request, 'auth/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('group_list')

    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('group_list')

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# =========================
# GROUP VIEWS
# =========================

@login_required
def group_list(request):
    groups = Group.objects.filter(created_by=request.user)
    return render(request, 'splitter/group_list.html', {'groups': groups})


@login_required
def group_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Group.objects.create(
                name=name,
                created_by=request.user
            )
            return redirect('group_list')

    return render(request, 'splitter/group_add.html')


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id, created_by=request.user)

    members = group.members.all()
    expenses = group.expenses.all()

    balances = calculate_balances(group)
    settlements = calculate_settlements(balances)

    return render(request, 'splitter/group_detail.html', {
        'group': group,
        'members': members,
        'expenses': expenses,
        'balances': balances,
        'settlements': settlements,
    })


# =========================
# MEMBER VIEWS
# =========================

@login_required
def member_add(request, group_id):
    group = get_object_or_404(Group, id=group_id, created_by=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Member.objects.create(name=name, group=group)
            return redirect('group_detail', group_id=group.id)

    return render(request, 'splitter/member_form.html', {'group': group})


@login_required
def member_edit(request, member_id):
    member = get_object_or_404(
        Member,
        id=member_id,
        group__created_by=request.user
    )

    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            member.name = name
            member.save()
            return redirect('group_detail', group_id=member.group.id)

    return render(request, 'splitter/member_form.html', {'member': member})


@login_required
def member_delete(request, member_id):
    member = get_object_or_404(
        Member,
        id=member_id,
        group__created_by=request.user
    )
    group_id = member.group.id
    member.delete()
    return redirect('group_detail', group_id=group_id)


# =========================
# EXPENSE VIEWS
# =========================

@login_required
def expense_add(request, group_id):
    group = get_object_or_404(Group, id=group_id, created_by=request.user)
    members = group.members.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        paid_by_id = request.POST.get('paid_by')

        if title and amount and paid_by_id:
            paid_by = get_object_or_404(Member, id=paid_by_id, group=group)
            Expense.objects.create(
                title=title,
                amount=Decimal(amount),
                paid_by=paid_by,
                group=group
            )
            return redirect('group_detail', group_id=group.id)

    return render(request, 'splitter/expense_form.html', {
        'group': group,
        'members': members
    })


@login_required
def expense_edit(request, expense_id):
    expense = get_object_or_404(
        Expense,
        id=expense_id,
        group__created_by=request.user
    )
    members = expense.group.members.all()

    if request.method == 'POST':
        expense.title = request.POST.get('title')
        expense.amount = Decimal(request.POST.get('amount'))
        expense.paid_by = get_object_or_404(
            Member,
            id=request.POST.get('paid_by'),
            group=expense.group
        )
        expense.save()
        return redirect('group_detail', group_id=expense.group.id)

    return render(request, 'splitter/expense_form.html', {
        'expense': expense,
        'members': members
    })


@login_required
def expense_delete(request, expense_id):
    expense = get_object_or_404(
        Expense,
        id=expense_id,
        group__created_by=request.user
    )
    group_id = expense.group.id
    expense.delete()
    return redirect('group_detail', group_id=group_id)


# =========================
# BUSINESS LOGIC
# =========================

def calculate_balances(group):
    members = group.members.all()
    expenses = group.expenses.all()

    total_expense = sum(e.amount for e in expenses)
    member_count = members.count()

    balances = {}

    if member_count == 0:
        return balances

    share = total_expense / member_count

    for member in members:
        paid = sum(e.amount for e in expenses if e.paid_by == member)
        balances[member] = paid - share

    return balances


def calculate_settlements(balances):
    payers = []
    receivers = []

    for member, balance in balances.items():
        if balance < 0:
            payers.append([member, -balance])
        elif balance > 0:
            receivers.append([member, balance])

    settlements = []
    i = j = 0

    while i < len(payers) and j < len(receivers):
        payer, pay_amt = payers[i]
        receiver, recv_amt = receivers[j]

        amt = min(pay_amt, recv_amt)

        settlements.append({
            'from': payer,
            'to': receiver,
            'amount': amt
        })

        payers[i][1] -= amt
        receivers[j][1] -= amt

        if payers[i][1] == 0:
            i += 1
        if receivers[j][1] == 0:
            j += 1

    return settlements
