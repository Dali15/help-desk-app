from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from .models import Ticket, Comment, Attachment
from .forms import TicketForm, TicketEditForm, CommentForm, TicketFilterForm, LoginForm, RegistrationForm


def register(request):
    """Inscription d'un nouvel utilisateur"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Inscription réussie! Veuillez vous connecter.')
            return redirect('login')
    else:
        form = RegistrationForm()
    
    context = {'form': form}
    return render(request, 'auth/register.html', context)


def login_view(request):
    """Connexion utilisateur"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {user.first_name}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Identifiants invalides.')
    else:
        form = LoginForm()
    
    context = {'form': form}
    return render(request, 'auth/login.html', context)


def logout_view(request):
    """Déconnexion"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté.')
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    """Affiche le dashboard avec statistiques"""
    user = request.user
    
    # Admin voir tous les tickets
    if user.is_staff:
        tickets = Ticket.objects.all()
    else:
        # Utilisateurs normaux voient que leurs propres tickets
        tickets = Ticket.objects.filter(user=user)
    
    total_tickets = tickets.count()
    open_tickets = tickets.filter(status='OPEN').count()
    in_progress = tickets.filter(status='IN_PROGRESS').count()
    resolved = tickets.filter(status='RESOLVED').count()
    closed = tickets.filter(status='CLOSED').count()
    urgent_tickets = tickets.filter(is_urgent=True, status__in=['OPEN', 'IN_PROGRESS']).count()
    
    # Top priorités
    high_priority = tickets.filter(priority='HIGH').count()
    medium_priority = tickets.filter(priority='MED').count()
    low_priority = tickets.filter(priority='LOW').count()
    
    # Tickets récents
    recent_tickets = tickets.all()[:5]
    
    context = {
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'in_progress': in_progress,
        'resolved': resolved,
        'closed': closed,
        'urgent_tickets': urgent_tickets,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
        'recent_tickets': recent_tickets,
        'is_admin': user.is_staff,
    }
    return render(request, 'tickets/dashboard.html', context)


@login_required(login_url='login')
def ticket_list(request):
    """Affiche la liste des tickets avec filtres et recherche"""
    user = request.user
    
    # Admin voir tous les tickets
    if user.is_staff:
        tickets = Ticket.objects.all()
    else:
        # Utilisateurs normaux voient que leurs propres tickets
        tickets = Ticket.objects.filter(user=user)
    
    form = TicketFilterForm(request.GET)
    
    # Recherche
    search = request.GET.get('search', '')
    if search:
        tickets = tickets.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(requester_name__icontains=search) |
            Q(id__icontains=search)
        )
    
    # Filtres
    status = request.GET.get('status', '')
    if status:
        tickets = tickets.filter(status=status)
    
    priority = request.GET.get('priority', '')
    if priority:
        tickets = tickets.filter(priority=priority)
    
    category = request.GET.get('category', '')
    if category:
        tickets = tickets.filter(category=category)
    
    # Tri
    sort = request.GET.get('sort', '-created_at')
    if sort in ['-created_at', 'created_at', '-priority', 'priority', '-status', 'status']:
        tickets = tickets.order_by(sort)
    
    # Pagination
    paginator = Paginator(tickets, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tickets': page_obj.object_list,
        'form': form,
        'search': search,
        'total_count': tickets.count(),
        'is_admin': user.is_staff,
    }
    return render(request, 'tickets/ticket_list.html', context)


@login_required(login_url='login')
def ticket_detail(request, pk):
    """Affiche les détails d'un ticket avec commentaires"""
    ticket = get_object_or_404(Ticket, pk=pk)
    user = request.user
    
    # Vérifier les permissions
    if not user.is_staff and ticket.user != user:
        messages.error(request, 'Vous n\'avez pas accès à ce ticket.')
        return redirect('ticket_list')
    
    comments = ticket.comments.all()
    
    if request.method == 'POST' and 'add_comment' in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.save()
            return redirect('ticket_detail', pk=ticket.id)
    elif request.method == 'POST' and 'add_attachment' in request.POST:
        files = request.FILES.getlist('attachments')
        created = 0
        for f in files:
            Attachment.objects.create(ticket=ticket, file=f)
            created += 1
        if created:
            messages.success(request, f'{created} fichier(s) téléchargé(s) avec succès.')
        return redirect('ticket_detail', pk=ticket.id)
    else:
        form = CommentForm()
    
    context = {
        'ticket': ticket,
        'comments': comments,
        'form': form,
        'is_admin': user.is_staff,
    }
    return render(request, 'tickets/ticket_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def ticket_create(request):
    """Crée un nouveau ticket"""
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            # handle attachments (multiple)
            files = request.FILES.getlist('attachments')
            for f in files:
                Attachment.objects.create(ticket=ticket, file=f)
            messages.success(request, 'Ticket créé avec succès!')
            return redirect('ticket_detail', pk=ticket.id)
    else:
        form = TicketForm()
    
    context = {'form': form, 'title': 'Créer un nouveau Ticket', 'is_admin': request.user.is_staff}
    return render(request, 'tickets/ticket_form.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def ticket_edit(request, pk):
    """Édite un ticket existant"""
    ticket = get_object_or_404(Ticket, pk=pk)
    user = request.user
    
    # Vérifier les permissions (admin ou propriétaire)
    if not user.is_staff and ticket.user != user:
        messages.error(request, 'Vous n\'avez pas accès à ce ticket.')
        return redirect('ticket_list')
    
    if request.method == 'POST':
        form = TicketEditForm(request.POST, instance=ticket)
        if form.is_valid():
            if form.cleaned_data['status'] == 'CLOSED' and not ticket.resolved_at:
                ticket.resolved_at = timezone.now()
            ticket = form.save()
            messages.success(request, 'Ticket modifié avec succès!')
            return redirect('ticket_detail', pk=ticket.id)
    else:
        form = TicketEditForm(instance=ticket)
    
    context = {'form': form, 'ticket': ticket, 'title': f'Éditer Ticket #{ticket.id}', 'is_admin': user.is_staff}
    return render(request, 'tickets/ticket_form.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def ticket_delete(request, pk):
    """Supprime un ticket"""
    ticket = get_object_or_404(Ticket, pk=pk)
    user = request.user
    
    # Vérifier les permissions (admin ou propriétaire)
    if not user.is_staff and ticket.user != user:
        messages.error(request, 'Vous n\'avez pas accès à ce ticket.')
        return redirect('ticket_list')
    
    ticket.delete()
    messages.success(request, 'Ticket supprimé avec succès!')
    return redirect('ticket_list')


@login_required(login_url='login')
@require_http_methods(["POST"])
def comment_delete(request, ticket_id, comment_id):
    """Supprime un commentaire"""
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    comment = get_object_or_404(Comment, pk=comment_id, ticket=ticket)
    
    # Vérifier les permissions
    if not request.user.is_staff and ticket.user != request.user:
        messages.error(request, 'Vous n\'avez pas accès à ce ticket.')
        return redirect('ticket_list')
    
    comment.delete()
    messages.success(request, 'Commentaire supprimé!')
    return redirect('ticket_detail', pk=ticket_id)


@login_required(login_url='login')
def ticket_export_csv(request):
    """Exporte les tickets en CSV"""
    import csv
    from django.http import HttpResponse
    
    user = request.user
    
    # Admin exporte tous les tickets
    if user.is_staff:
        tickets = Ticket.objects.all()
    else:
        # Utilisateurs normaux exportent que leurs propres tickets
        tickets = Ticket.objects.filter(user=user)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tickets.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Titre', 'Demandeur', 'Catégorie', 'Priorité', 'Statut', 'Urgent', 'Date création', 'Date modif'])
    
    for ticket in tickets:
        writer.writerow([
            ticket.id,
            ticket.title,
            ticket.requester_name,
            ticket.get_category_display(),
            ticket.get_priority_display(),
            ticket.get_status_display(),
            'Oui' if ticket.is_urgent else 'Non',
            ticket.created_at.strftime('%d/%m/%Y %H:%M'),
            ticket.updated_at.strftime('%d/%m/%Y %H:%M'),
        ])
    
    return response


