# Generated by Django 5.1.1 on 2024-09-12 10:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_alter_policy_policy_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="policy",
            name="end_date",
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name="policy",
            name="start_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
