from collections import defaultdict
from decimal import Decimal
from .models import Reimbursement


def calculate_balances(group):
    """
    Returns:
      - user_balances: list of {'user': user, 'balance': Decimal}
      - guest_balances: list of {'guest': GuestMember, 'balance': Decimal} (always negative = owes)
    Positive balance = owed money. Negative = owes money.
    """
    balances = defaultdict(Decimal)
    user_map = {}
    guest_balances = defaultdict(Decimal)
    guest_map = {}

    for expense in group.expenses.prefetch_related('participants', 'guest_participants', 'custom_shares__user', 'custom_shares__guest').select_related('paid_by'):
        payer = expense.paid_by
        user_map[payer.id] = payer
        balances[payer.id] += expense.amount

        if expense.split_type == 'custom':
            # Répartition personnalisée
            for share in expense.custom_shares.all():
                if share.user:
                    user_map[share.user.id] = share.user
                    balances[share.user.id] -= share.amount
                elif share.guest:
                    guest_map[share.guest.id] = share.guest
                    guest_balances[share.guest.id] -= share.amount
        else:
            # Répartition égale (comportement par défaut)
            participants = list(expense.participants.all())
            guests = list(expense.guest_participants.all())
            total_count = len(participants) + len(guests)

            if total_count == 0:
                continue

            share = expense.amount / Decimal(total_count)

            for participant in participants:
                user_map[participant.id] = participant
                balances[participant.id] -= share

            for guest in guests:
                guest_map[guest.id] = guest
                guest_balances[guest.id] -= share

    # Apply reimbursements
    for r in group.reimbursements.select_related('from_user', 'from_guest', 'to_user').all():
        user_map[r.to_user.id] = r.to_user
        balances[r.to_user.id] -= r.amount  # creditor received money back

        if r.from_user:
            user_map[r.from_user.id] = r.from_user
            balances[r.from_user.id] += r.amount  # debtor paid
        elif r.from_guest:
            guest_map[r.from_guest.id] = r.from_guest
            guest_balances[r.from_guest.id] += r.amount  # guest paid

    user_result = [
        {'user': user_map[uid], 'balance': round(bal, 2)}
        for uid, bal in balances.items()
    ]
    guest_result = [
        {'guest': guest_map[gid], 'balance': round(bal, 2)}
        for gid, bal in guest_balances.items()
        if round(bal, 2) < -Decimal('0.01')
    ]
    return user_result, guest_result


def calculate_settlements(group):
    """
    Returns list of settlements. Each entry has:
      - 'from': {'type': 'user'|'guest', 'obj': user_or_guest}
      - 'to':   {'type': 'user', 'obj': user}
      - 'amount': Decimal
    """
    user_balances, guest_balances = calculate_balances(group)

    # Registered users who owe money
    debtors = [
        {'type': 'user', 'obj': b['user'], 'amount': -b['balance']}
        for b in user_balances if b['balance'] < -Decimal('0.01')
    ]
    # Guests always owe money
    debtors += [
        {'type': 'guest', 'obj': b['guest'], 'amount': -b['balance']}
        for b in guest_balances if b['balance'] < -Decimal('0.01')
    ]

    creditors = [
        {'type': 'user', 'obj': b['user'], 'amount': b['balance']}
        for b in user_balances if b['balance'] > Decimal('0.01')
    ]

    debtors.sort(key=lambda x: x['amount'], reverse=True)
    creditors.sort(key=lambda x: x['amount'], reverse=True)

    settlements = []
    i, j = 0, 0

    while i < len(debtors) and j < len(creditors):
        amount = min(debtors[i]['amount'], creditors[j]['amount'])
        amount = round(amount, 2)

        settlements.append({
            'from': debtors[i],
            'to': creditors[j],
            'amount': amount,
        })

        debtors[i]['amount'] -= amount
        creditors[j]['amount'] -= amount

        if debtors[i]['amount'] < Decimal('0.01'):
            i += 1
        if creditors[j]['amount'] < Decimal('0.01'):
            j += 1

    return settlements
