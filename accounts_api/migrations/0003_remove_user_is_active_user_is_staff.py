# Generated by Django 4.1.3 on 2023-01-22 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts_api", "0002_alter_user_date_added"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_active",
        ),
        migrations.AddField(
            model_name="user",
            name="is_staff",
            field=models.BooleanField(default=True),
        ),
    ]
