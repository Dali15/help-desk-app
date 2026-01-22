#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hd.settings')
django.setup()

from tickets.models import Ticket, Attachment

print("=== Checking Attachments in Database ===\n")

# Check if any attachments exist
all_attachments = Attachment.objects.all()
print(f"Total attachments in DB: {all_attachments.count()}")

for att in all_attachments:
    print(f"\nAttachment ID: {att.id}")
    print(f"  Ticket: #{att.ticket.id}")
    print(f"  File: {att.file.name}")
    print(f"  File path: {att.file.path if hasattr(att.file, 'path') else 'N/A'}")
    print(f"  File URL: {att.file.url}")
    print(f"  File exists: {att.file.storage.exists(att.file.name)}")
    print(f"  Uploaded at: {att.uploaded_at}")

# Check tickets with attachments
print("\n=== Tickets with Attachments ===")
tickets_with_att = Ticket.objects.filter(attachments__isnull=False).distinct()
for ticket in tickets_with_att:
    att_count = ticket.attachments.count()
    print(f"Ticket #{ticket.id}: {att_count} attachment(s)")

# Check media directory
print("\n=== Media Directory Check ===")
media_root = 'media'
if os.path.exists(media_root):
    print(f"✓ Media directory exists: {os.path.abspath(media_root)}")
    for root, dirs, files in os.walk(media_root):
        level = root.replace(media_root, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{sub_indent}{file}")
else:
    print(f"✗ Media directory does not exist: {os.path.abspath(media_root)}")

print("\n=== Done ===")
