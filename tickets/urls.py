from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    # Dashboard et Tickets
    path("", views.dashboard, name="dashboard"),
    path("tickets/", views.ticket_list, name="ticket_list"),
    path("tickets/new/", views.ticket_create, name="ticket_create"),
    path("tickets/<int:pk>/", views.ticket_detail, name="ticket_detail"),
    path("tickets/<int:pk>/edit/", views.ticket_edit, name="ticket_edit"),
    path("tickets/<int:pk>/delete/", views.ticket_delete, name="ticket_delete"),
    path("tickets/<int:ticket_id>/comment/<int:comment_id>/delete/", views.comment_delete, name="comment_delete"),
    path("tickets/export/csv/", views.ticket_export_csv, name="ticket_export_csv"),
]
