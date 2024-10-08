# Generated by Django 5.1.1 on 2024-09-12 12:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_alter_policy_coverage_amount_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="policy",
            name="is_accepted",
        ),
        migrations.AlterField(
            model_name="policy",
            name="status",
            field=models.CharField(
                choices=[
                    ("quoted", "Quoted"),
                    ("accepted", "Accepted"),
                    ("active", "Active"),
                    ("expired", "Expired"),
                    ("cancelled", "Cancelled"),
                ],
                default="quoted",
                max_length=10,
            ),
        ),
    ]
