# Generated by Django 5.0.7 on 2024-10-01 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DPHapp', '0003_remove_service_duration_service_duration_hours_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='rejection_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], max_length=10),
        ),
    ]
