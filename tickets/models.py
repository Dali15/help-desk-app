from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ("LOW", "Faible"),
        ("MED", "Moyenne"),
        ("HIGH", "Élevée"),
    ]

    STATUS_CHOICES = [
        ("OPEN", "Ouvert"),
        ("IN_PROGRESS", "En cours"),
        ("RESOLVED", "Résolu"),
        ("CLOSED", "Fermé"),
    ]

    CATEGORY_CHOICES = [
        ("BUG", "Bug"),
        ("FEATURE", "Demande de fonctionnalité"),
        ("SUPPORT", "Support"),
        ("OTHER", "Autre"),
    ]

    title = models.CharField(max_length=120)
    description = models.TextField()
    priority = models.CharField(max_length=4, choices=PRIORITY_CHOICES, default="MED")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="OPEN")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="SUPPORT")
    requester_name = models.CharField(max_length=80)
    requester_email = models.EmailField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    assigned_to = models.CharField(max_length=80, blank=True, null=True)
    resolution_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    is_urgent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['priority', '-created_at']),
        ]

    def __str__(self):
        return f"#{self.id} {self.title}"

    def get_status_color(self):
        colors = {
            'OPEN': 'danger',
            'IN_PROGRESS': 'warning',
            'RESOLVED': 'info',
            'CLOSED': 'success'
        }
        return colors.get(self.status, 'secondary')


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=80)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Commentaire par {self.author_name} sur #{self.ticket.id}"


class Attachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='tickets/attachments/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Attachment {self.id} for Ticket #{self.ticket.id}"


