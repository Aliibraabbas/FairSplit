import csv
from io import StringIO
from django.http import HttpResponse
from balances.services import calculate_balances, calculate_settlements


def export_group_to_csv(group):
    """Exporte toutes les données d'un groupe en CSV (format Excel français)"""
    output = StringIO()
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    currency_symbol = group.get_currency_symbol()
    
    # En-tête du fichier
    writer.writerow(['EXPORT GROUPE FAIRSPLIT'])
    writer.writerow([f'Groupe: {group.name}'])
    writer.writerow([f'Description: {group.description}'])
    writer.writerow([f'Devise: {group.get_currency_display()}'])
    writer.writerow([f'Cree le: {group.created_at.strftime("%d/%m/%Y")}'])
    writer.writerow([])
    
    # Membres inscrits
    writer.writerow(['MEMBRES INSCRITS'])
    writer.writerow(['ID', 'Nom utilisateur', 'Email'])
    for member in group.members.all():
        writer.writerow([member.id, member.username, member.email])
    writer.writerow([])
    
    # Invités
    writer.writerow(['INVITES'])
    writer.writerow(['ID', 'Nom'])
    for guest in group.guest_members.all():
        writer.writerow([guest.id, guest.name])
    writer.writerow([])
    
    # Dépenses
    writer.writerow(['DEPENSES'])
    writer.writerow([
        'ID', 'Titre', f'Montant ({currency_symbol})', 'Paye par', 'Date', 
        'Categorie', 'Type de repartition', 'Description'
    ])
    for expense in group.expenses.select_related('paid_by').all():
        writer.writerow([
            expense.id,
            expense.title,
            f'{float(expense.amount):.2f}',
            expense.paid_by.username,
            expense.date.strftime('%d/%m/%Y'),
            expense.get_category_display(),
            'Egale' if expense.split_type == 'equal' else 'Personnalisee',
            expense.description or ''
        ])
    writer.writerow([])
    
    # Participants par dépense
    writer.writerow(['PARTICIPANTS PAR DEPENSE'])
    writer.writerow(['Depense ID', 'Depense', 'Participant', 'Type', f'Part ({currency_symbol})'])
    for expense in group.expenses.prefetch_related(
        'participants', 'guest_participants', 'custom_shares__user', 'custom_shares__guest'
    ).all():
        if expense.split_type == 'custom':
            for share in expense.custom_shares.all():
                participant_name = share.user.username if share.user else share.guest.name
                participant_type = 'Membre' if share.user else 'Invite'
                writer.writerow([
                    expense.id,
                    expense.title,
                    participant_name,
                    participant_type,
                    f'{float(share.amount):.2f}'
                ])
        else:
            participants = list(expense.participants.all())
            guests = list(expense.guest_participants.all())
            total_count = len(participants) + len(guests)
            if total_count > 0:
                share_amount = float(expense.amount) / total_count
                for participant in participants:
                    writer.writerow([
                        expense.id,
                        expense.title,
                        participant.username,
                        'Membre',
                        f'{share_amount:.2f}'
                    ])
                for guest in guests:
                    writer.writerow([
                        expense.id,
                        expense.title,
                        guest.name,
                        'Invite',
                        f'{share_amount:.2f}'
                    ])
    writer.writerow([])
    
    # Soldes
    writer.writerow(['SOLDES'])
    writer.writerow(['Participant', 'Type', f'Solde ({currency_symbol})'])
    user_balances, guest_balances = calculate_balances(group)
    for balance in user_balances:
        writer.writerow([
            balance['user'].username,
            'Membre',
            f'{float(balance["balance"]):.2f}'
        ])
    for balance in guest_balances:
        writer.writerow([
            balance['guest'].name,
            'Invite',
            f'{float(balance["balance"]):.2f}'
        ])
    writer.writerow([])
    
    # Remboursements suggérés
    writer.writerow(['REMBOURSEMENTS SUGGERES'])
    writer.writerow(['De', 'Type debiteur', 'A', f'Montant ({currency_symbol})'])
    settlements = calculate_settlements(group)
    for settlement in settlements:
        from_name = settlement['from']['obj'].username if settlement['from']['type'] == 'user' else settlement['from']['obj'].name
        to_name = settlement['to']['obj'].username
        writer.writerow([
            from_name,
            'Membre' if settlement['from']['type'] == 'user' else 'Invite',
            to_name,
            f'{float(settlement["amount"]):.2f}'
        ])
    writer.writerow([])
    
    # Remboursements effectués
    writer.writerow(['REMBOURSEMENTS EFFECTUES'])
    writer.writerow(['De', 'Type', 'A', f'Montant ({currency_symbol})', 'Date'])
    for reimbursement in group.reimbursements.select_related('from_user', 'from_guest', 'to_user').all():
        from_name = reimbursement.from_user.username if reimbursement.from_user else reimbursement.from_guest.name
        from_type = 'Membre' if reimbursement.from_user else 'Invite'
        writer.writerow([
            from_name,
            from_type,
            reimbursement.to_user.username,
            f'{float(reimbursement.amount):.2f}',
            reimbursement.created_at.strftime('%d/%m/%Y %H:%M')
        ])
    
    return output.getvalue()
