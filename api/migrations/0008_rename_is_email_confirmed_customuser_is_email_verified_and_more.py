# Generated by Django 5.0.3 on 2024-03-15 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_emailconfimationtoken'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='is_email_confirmed',
            new_name='is_email_verified',
        ),
        migrations.DeleteModel(
            name='EmailConfimationToken',
        ),
    ]