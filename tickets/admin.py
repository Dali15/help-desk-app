from django.contrib import admin
from .models import Ticket, Comment


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "priority", "status", "requester_name", "assigned_to", "is_urgent", "created_at")
    list_filter = ("priority", "status", "category", "is_urgent", "created_at")
    search_fields = ("title", "description", "requester_name")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "resolved_at")
    fieldsets = (
        ("Informations", {
            "fields": ("title", "description", "category")
        }),
        ("Demandeur", {
            "fields": ("requester_name", "requester_email")
        }),
        ("Priorité et Statut", {
            "fields": ("priority", "status", "is_urgent")
        }),
        ("Gestion", {
            "fields": ("assigned_to", "resolution_notes")
        }),
        ("Dates", {
            "fields": ("created_at", "updated_at", "resolved_at"),
            "classes": ("collapse",)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "author_name", "created_at")
    list_filter = ("created_at", "ticket")
    search_fields = ("author_name", "content", "ticket__title")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

